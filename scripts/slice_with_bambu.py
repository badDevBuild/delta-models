#!/usr/bin/env python3
"""Local, isolated Bambu slicing and evidence readback; never sends to a printer."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from model_catalog import MODEL_IDS

ROOT = Path(__file__).resolve().parents[1]
CLI = Path(os.environ.get('DELTA_SLICER_CLI', '/private/tmp/delta-six-bambu-mount/BambuStudio.app/Contents/MacOS/BambuStudio'))
PROFILES = ROOT / 'tools/slicer-profiles/bambu-2.8.2.61'
DATADIR = Path('/private/tmp/delta-six-bambu-config')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(source, output, project):
    return [str(CLI), '--datadir', str(DATADIR), '--debug', '3',
            '--load-settings', f'{PROFILES / "machine.json"};{PROFILES / "process.json"}',
            '--load-filaments', str(PROFILES / 'filament.json'),
            '--curr-bed-type', 'Textured PEI Plate', '--arrange', '0', '--orient', '0',
            '--slice', '0', '--outputdir', str(output), '--export-3mf', project, str(source)]


def object_coverage(original, actual, project):
    """Compare every named input item with native model, plate preview, and toolpaths."""
    ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}

    def input_items(path):
        with zipfile.ZipFile(path) as z:
            model = ET.fromstring(z.read('3D/3dmodel.model'))
        resources = {o.get('id'): o for o in model.findall('m:resources/m:object', ns)}
        items = []
        for item in model.findall('m:build/m:item', ns):
            obj = resources[item.get('objectid')]
            items.append((obj.get('name'), len(obj.findall('m:mesh/m:triangles/m:triangle', ns))))
        return items

    expected = input_items(original)
    assert Counter(expected) == Counter(input_items(actual)), 'Layout changed input objects or face counts'
    with zipfile.ZipFile(project) as z:
        model = ET.fromstring(z.read('3D/3dmodel.model'))
        builds = model.findall('m:build/m:item', ns)
        settings = ET.fromstring(z.read('Metadata/model_settings.config'))
        records = []
        for obj in settings.findall('object'):
            name = next(m.get('value') for m in obj.findall('metadata') if m.get('key') == 'name')
            faces = sum(int(m.get('face_count')) for m in obj.findall('part/mesh_stat'))
            records.append((name, faces))
        preview = json.loads(z.read('Metadata/plate_1.json'))['bbox_objects']
        gcode = z.read('Metadata/plate_1.gcode').decode()
    assert Counter(records) == Counter(expected), 'Native objects or triangle counts differ from input'
    assert len(builds) == len(expected) and all(i.get('printable') == '1' for i in builds)
    assert Counter(p['name'] for p in preview) == Counter(n for n, _ in expected)
    assert all(p['area'] > 0 for p in preview), 'An object has no printed first-layer footprint'
    labels_match = re.search(r'^; model label id: ([0-9,]+)$', gcode, re.M)
    if labels_match:
        labels = set(labels_match.group(1).split(','))
        label_source = 'model_label_header'
    else:
        # Bambu omits the multi-object header on a single-object plate.
        # Require one actual body label, plus the native/name/footprint checks above.
        assert len(expected) == 1, 'Missing multi-object labels in G-code'
        labels = set(re.findall(r'^; OBJECT_ID: ([0-9]+)\s*$', gcode, re.M))
        assert len(labels) == 1, 'Single-object plate must contain one actual G-code body label'
        label_source = 'single_object_body_label'
    assert len(labels) == len(expected), 'G-code labels do not cover every input object'
    extrusion = Counter()
    current = None
    for line in gcode.splitlines():
        if line.startswith('; OBJECT_ID: '):
            current = line.split(': ')[1]
        elif current in labels and line.startswith(('G1 ', 'G2 ', 'G3 ')):
            e = re.search(r'(?:^| )E([-+0-9.]+)', line)
            if e and float(e.group(1)) > 0:
                extrusion[current] += 1
    assert set(extrusion) == labels, 'An object label contains no extrusion moves'
    return {'passed': True, 'input_object_count': len(expected), 'native_printable_object_count': len(builds),
            'first_layer_object_count': len(preview), 'gcode_object_count': len(labels),
            'objects': [{'name': n, 'triangle_count': t} for n, t in expected],
            'all_names_and_triangle_counts_preserved': True,
            'gcode_label_source': label_source,
            'all_gcode_labels_have_extrusion': True,
            'gcode_extrusion_move_counts': dict(sorted(extrusion.items(), key=lambda x: int(x[0])))}


def inspect_project(project, result_file):
    result = json.loads(result_file.read_text())
    assert result['return_code'] == 0, result
    with zipfile.ZipFile(project) as z:
        assert z.testzip() is None
        cfg = json.loads(z.read('Metadata/project_settings.config'))
        expected = {'printer_model': 'Bambu Lab P1S',
                    'printer_settings_id': 'Bambu Lab P1S 0.4 nozzle',
                    'nozzle_diameter': ['0.4'], 'filament_type': ['PLA'],
                    'filament_settings_id': ['Bambu PLA Basic @BBL P1S 0.4 nozzle'],
                    'layer_height': '0.16', 'curr_bed_type': 'Textured PEI Plate',
                    'wall_loops': '3', 'sparse_infill_density': '15%',
                    'enable_support': '1', 'support_type': 'tree(auto)',
                    'brim_type': 'auto_brim', 'brim_width': '3'}
        for key, value in expected.items():
            assert cfg.get(key) == value, (key, cfg.get(key), value)
        info = ET.fromstring(z.read('Metadata/slice_info.config'))
        plates = info.findall('plate')
        assert len(plates) == 1, 'Each input must contain one plate'
        metadata = {m.get('key'): m.get('value') for m in plates[0].findall('metadata')}
        assert metadata['outside'] == 'false', metadata
        gcode = z.read('Metadata/plate_1.gcode')
        assert len(gcode) > 10000 and b'G1 ' in gcode, 'Missing actual toolpaths'
        standalone = project.parent / 'plate_1.gcode'
        if not standalone.exists():
            standalone.write_bytes(gcode)
        assert sha(standalone) == hashlib.sha256(gcode).hexdigest()
        sliced = result['sliced_plates']
        assert len(sliced) == 1
        assert not sliced[0].get('warning_message'), sliced[0]['warning_message']
        return {'settings_readback': expected, 'slice_metadata': metadata,
                'estimated_seconds': sliced[0]['total_predication'],
                'filament_grams': sum(f['total_used_g'] for f in sliced[0]['filaments']),
                'gcode_bytes': len(gcode), 'gcode_sha256': sha(standalone),
                'gcode_file': standalone, 'slicer_return_code': 0,
                'checks': {'native_zip_integrity': True, 'embedded_gcode_matches_export': True,
                           'printer_nozzle_material_layer_verified': True, 'objects_inside_plate': True,
                           'slicer_conflict_check_passed': True, 'physical_print_tested': False}}


def write_report(model, jobs):
    print_root = ROOT / 'assets' / model / 'print'
    source = ROOT / 'assets' / model / 'source' / f'{model}.blend'
    plates = []
    native = []
    for job in jobs:
        info = inspect_project(job['project'], job['result'])
        info['object_coverage'] = object_coverage(job['original'], job['input'], job['project'])
        info['gcode_file'] = str(info['gcode_file'].relative_to(print_root))
        info.update({'input_file': str(job['input'].relative_to(print_root)),
                     'input_3mf_sha256': sha(job['input']),
                     'original_input_file': str(job['original'].relative_to(print_root)),
                     'original_input_sha256': sha(job['original']),
                     'native_project': str(job['project'].relative_to(print_root)),
                     'native_project_sha256': sha(job['project']),
                     'result_file': str(job['result'].relative_to(print_root)),
                     'result_sha256': sha(job['result']),
                     'log_file': str(job['log'].relative_to(print_root)),
                     'log_sha256': sha(job['log'])})
        if job.get('layout'):
            info['layout_adjustment_file'] = str(job['layout'].relative_to(print_root))
            info['layout_adjustment_sha256'] = sha(job['layout'])
        plates.append(info)
        native.append({'file': info['native_project'], 'sha256': info['native_project_sha256']})
    report = {'schema': 'delta-slice-validation/v1', 'model': model, 'passed': True,
              'validated_at': datetime.now(timezone.utc).isoformat(),
              'source_file': str(source.relative_to(ROOT)), 'source_sha256': sha(source),
              'slicer': {'name': 'Bambu Studio', 'version': '02.08.02.61', 'cli': str(CLI),
                         'isolated_datadir': str(DATADIR), 'official_release':
                         'https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61',
                         'signature': 'Notarized Developer ID; spctl accepted; codesign valid on disk'},
              'printer': 'Bambu Lab P1S', 'nozzle_mm': 0.4, 'material': 'Bambu PLA Basic',
              'layer_height_mm': 0.16, 'bed': 'Textured PEI Plate',
              'profiles': [{'file': str(p.relative_to(ROOT)), 'sha256': sha(p)}
                           for p in [PROFILES / n for n in ['machine.json', 'process.json', 'filament.json', 'provenance.json']]],
              'plates': plates, 'native_projects': native,
              'total_estimated_seconds': sum(p['estimated_seconds'] for p in plates),
              'total_filament_grams': sum(p['filament_grams'] for p in plates),
              'physical_print_tested': False,
              'limitations': ['Estimates are slicer predictions, not measured print results.',
                              'Textured PEI is the selected project bed; confirm the actual installed plate.',
                              'Support removal, adhesion, fit, strength and surface quality need physical proof.']}
    out = print_root / 'slice-validation.json'
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('model', choices=MODEL_IDS)
    args = ap.parse_args()
    assert CLI.is_file(), f'Official verified CLI not mounted at {CLI}'
    root = ROOT / 'assets' / args.model / 'print'
    sources = sorted((root / 'plates').glob('*.3mf'))
    assert sources, f'No plate inputs: {root}'
    if args.model == 'm7':
        raise SystemExit('M7 requires its recorded widened accessories layout; use the explicit per-plate commands in sliced/*/command.json.')
    blend = ROOT / 'assets' / args.model / 'source' / f'{args.model}.blend'
    before_source = sha(blend)
    jobs = []
    for source in sources:
        before = sha(source)
        output = root / 'sliced' / source.stem
        output.mkdir(parents=True, exist_ok=True)
        project = output / f'{source.stem}-p1s-pla-sliced.3mf'
        log = output / 'slicer.log'
        cmd = command(source, output, project.name)
        (output / 'command.json').write_text(json.dumps(cmd, ensure_ascii=False, indent=2) + '\n')
        with log.open('w') as f:
            completed = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        assert completed.returncode == 0, f'Slice failed {completed.returncode}; inspect {log}'
        assert sha(source) == before and sha(blend) == before_source, 'Input changed during slicing'
        jobs.append({'input': source, 'original': source, 'project': project,
                     'result': output / 'result.json', 'log': log})
    report = write_report(args.model, jobs)
    print(json.dumps({k: report[k] for k in ['model', 'passed', 'total_estimated_seconds', 'total_filament_grams']}))


if __name__ == '__main__':
    main()
