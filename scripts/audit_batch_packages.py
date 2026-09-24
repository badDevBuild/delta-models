"""Read current geometry/sliced archives and their assembly references for a batch."""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from datetime import datetime, timezone
from model_catalog import MODELS, ROOT
from slicing_evidence import check_slicing


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect(asset_id):
    asset = ROOT / 'assets' / asset_id
    directory = asset / 'print'
    source_hash = sha((asset / 'source' / f'{asset_id}.blend').read_bytes())
    manifest = json.loads((directory / 'manifest.json').read_text())
    validation = json.loads((directory / 'validation.json').read_text())
    assert manifest['source_sha256'] == source_hash
    assert validation['passed'] and len(manifest['parts']) == validation['part_count']
    plates = json.loads((directory / 'plates.json').read_text())['plates']
    parts = manifest['parts']
    names = sorted(p['name'] for p in parts)
    assert names == sorted(p['name'] for plate in plates for p in plate['parts'])
    required = ['manifest.json', 'validation.json', 'plates.json', 'PRINTING.md',
                'ASSEMBLY.md', 'assembly-reference.png', 'assembly-map.svg', 'assembly-table.tsv']
    required += [p[k] for p in parts for k in ['stl', '3mf']]
    required += [p['file'] for p in plates]
    geometry = directory / f'{asset_id}-print.zip'
    with zipfile.ZipFile(geometry) as archive:
        assert archive.testzip() is None
        assert set(required).issubset(archive.namelist())
        for name in required:
            assert archive.read(name) == (directory / name).read_bytes(), f'Geometry archive differs: {name}'
        assert archive.read('assembly-reference.png') == (asset / 'renders/side.png').read_bytes()
        assembly = archive.read('ASSEMBLY.md').decode()
        for target in re.findall(r'\]\(([^)]+)\)', assembly):
            assert target in archive.namelist(), f'Missing assembly reference: {target}'
        for part in parts:
            assert f"`{Path(part['stl']).name}`" in assembly, f'Missing pairing entry: {part["name"]}'
        table = list(csv.DictReader(io.StringIO(archive.read('assembly-table.tsv').decode()), delimiter='\t'))
        assert sorted(row['piece'] for row in table) == names
        for segment in {p['segment'] for p in parts}:
            pair = [p for p in parts if p['segment'] == segment]
            assert len(pair) == 2 and {p['assembly_side'] for p in pair} == {'left', 'right'}
    archive_record = json.loads((directory / 'archive-validation.json').read_text())
    assert archive_record['zip_sha256'] == sha(geometry.read_bytes())
    slicing = check_slicing(asset)
    assert slicing['passed'], slicing['errors']
    sliced = directory / f'{asset_id}-sliced.zip'
    sliced_record = json.loads((directory / 'sliced-package-validation.json').read_text())
    assert sliced_record['sha256'] == sha(sliced.read_bytes())
    assert sliced_record['report_sha256'] == sha((directory / 'slice-validation.json').read_bytes())
    with zipfile.ZipFile(sliced) as archive:
        assert archive.testzip() is None
        assert archive.read('slice-validation.json') == (directory / 'slice-validation.json').read_bytes()
        for profile in slicing['report']['profiles']:
            actual = ROOT / profile['file']
            assert archive.read('profiles/' + actual.name) == actual.read_bytes()
        for name in ['ASSEMBLY.md', 'assembly-reference.png', 'assembly-map.svg']:
            assert archive.read(name) == (directory / name).read_bytes(), f'Sliced assembly differs: {name}'
        for project in slicing['report']['native_projects']:
            actual = directory / project['file']
            assert archive.read(actual.name) == actual.read_bytes(), f'Sliced native project differs: {actual.name}'
    for path in [asset / 'SOURCE_NOTES.md', ROOT / 'scripts' / f'build_{asset_id}.py']:
        assert path.is_file(), f'Missing source documentation: {path}'
    return {'id': asset_id, 'passed': True, 'source_sha256': source_hash,
            'pieces': len(parts), 'plates': len(plates), 'geometry_zip_sha256': sha(geometry.read_bytes()),
            'sliced_zip_sha256': sha(sliced.read_bytes()), 'all_archive_files_match_current_files': True,
            'assembly_links_and_pairs_verified': True}


def audit(batch):
    ids = [m['id'] for m in MODELS if m['batch'] == batch]
    assert ids and 'm7' not in ids, 'This audit expects fused left/right sculpture pairs, not the special M7 layout'
    rows = []
    for asset_id in ids:
        try:
            rows.append(inspect(asset_id))
        except Exception as error:
            rows.append({'id': asset_id, 'passed': False, 'error': f'{type(error).__name__}: {error}'})
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'batch': batch,
              'scope': 'Read actual archive bytes and current source identities; no physical or visual claim.',
              'passed': all(row['passed'] for row in rows), 'models': rows}
    output = ROOT / 'reports' / f'batch{batch}-archive-readback.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': result['passed'], 'models': len(rows), 'report': str(output),
                      'failures': [row for row in rows if not row['passed']]}))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=int, required=True)
    args = parser.parse_args()
    if not audit(args.batch)['passed']:
        raise SystemExit(1)
