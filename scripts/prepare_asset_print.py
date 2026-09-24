"""Fuse default exterior art into one miniature, then cut planar glue pieces.

Run in a separate Blender process with -- --asset akm. The source is read-only.
This creates STL and geometry 3MF, not machine instructions or printer jobs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import zipfile
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from print_common import (descendant_meshes, copy_evaluated_meshes, append_support_boxes,
    voxel_union, mesh_bounds, cut_keep, crop_bounds, connected_meshes,
    normalized_triangles, write_stl, write_3mf)
from validate_print import validate_directory
from model_catalog import MODEL_IDS


def convert(asset_id, voxel=.22):
    asset = ROOT / 'assets' / asset_id
    source = asset / 'source' / (asset_id + '.blend')
    output = asset / 'print'
    for folder in ['stl', '3mf']:
        (output / folder).mkdir(parents=True, exist_ok=True)
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(source))
    original = bpy.context.scene
    original.view_layers[0].update()
    explicit_breaks=original.get('print_segment_breaks_x_mm')
    if isinstance(explicit_breaks,str):explicit_breaks=json.loads(explicit_breaks)
    if explicit_breaks is not None:
        explicit_breaks=sorted(float(x) for x in explicit_breaks)
        if any(not math.isfinite(x) for x in explicit_breaks) or len(set(explicit_breaks))!=len(explicit_breaks):
            raise ValueError('Explicit glue planes must be unique finite X coordinates')
    deps = bpy.context.evaluated_depsgraph_get()
    roots = sorted((o for o in original.objects if o.type == 'EMPTY' and o.name.startswith('part_')),
                   key=lambda o: o.name)
    if not roots:
        raise ValueError('No exterior component groups in active scene')
    work = bpy.data.scenes.new('PRINT_EXTERIOR_COPY')
    work.unit_settings.system = 'METRIC'
    work.unit_settings.scale_length = .001
    base_meshes = []
    reinforcements = []
    base_groups = []
    digital_accessories = []
    for root in roots:
        if not bool(root.get('default_visible', True)):
            digital_accessories.append(root.name)
            continue
        if root.get('print_skip', False):
            continue
        sources = descendant_meshes(root)
        if not sources:
            raise ValueError('Empty component: ' + root.name)
        base_meshes.extend(sources)
        base_groups.append(root.name)
        supports=root.get('print_reinforcements')
        if supports:
            reinforcements.extend(json.loads(supports) if isinstance(supports,str) else supports)
    if not base_meshes:
        raise ValueError('No default-visible exterior geometry')
    obj=copy_evaluated_meshes(base_meshes,deps,work,'part_display_body')
    copies=[('part_display_body',obj,{'label':'整装外观雕塑','visible':True,
                                     'bounds':None,'supports':reinforcements})]
    bpy.context.window.scene = work
    manifest = {
        'schema': 'delta-six-print-manifest/v1', 'asset_id': asset_id,
        'purpose': 'Inert miniature exterior sculpture; solid parts and custom decorative glue seams',
        'source_blend': f'../source/{asset_id}.blend', 'source_sha256': source_hash,
        'coordinate_unit': 'millimeter', 'voxel_size_mm': voxel,
        'geometry_3mf_only': True, 'physical_print_tested': False,
        'sliced': False, 'slicing_status_scope': 'The sliced=false flag describes these geometry-only exports. Current slicing evidence is recorded separately in slice-validation.json.',
        'parts': [], 'discarded_tiny_fragments': [],
        'print_construction':'All default exterior groups fused before planar cuts; no overlapping component solids.',
        'source_groups':base_groups,'digital_only_accessories':digital_accessories,
        'explicit_segment_breaks_x_mm':explicit_breaks,
        'assembly': 'Glue left/right halves and adjacent length segments on matching flat cuts. Web components are separate presentation groups.',
    }
    for name, obj, spec in copies:
        print('PREPARING', asset_id, name, flush=True)
        append_support_boxes(obj, spec['supports'])
        merged = voxel_union(obj, voxel)
        crop_bounds(merged, spec['bounds'])
        for island_number, island in enumerate(connected_meshes(merged), 1):
            volume = abs(island.calc_volume(signed=True))
            if volume < .05:
                manifest['discarded_tiny_fragments'].append({'group': name, 'volume_mm3': volume})
                island.free()
                continue
            bounds = mesh_bounds(island)
            width = bounds['max'][0] - bounds['min'][0]
            segment_count = max(1, math.ceil(width / 200))
            if explicit_breaks is not None:
                edges=[bounds['min'][0]]+[x for x in explicit_breaks if bounds['min'][0]<x<bounds['max'][0]]+[bounds['max'][0]]
                if any(b-a>200.001 for a,b in zip(edges,edges[1:])):
                    raise ValueError('Explicit glue plane leaves a segment longer than 200 mm')
            else:
                edges=[bounds['min'][0]+width*i/segment_count for i in range(segment_count+1)]
            segment_count=len(edges)-1
            for segment in range(segment_count):
                x0,x1=edges[segment:segment+2]
                piece = island.copy()
                if segment_count > 1:
                    cut_keep(piece, (-1, 0, 0), (x0, 0, 0))
                    cut_keep(piece, (1, 0, 0), (x1, 0, 0))
                split_y = bounds['min'][1] < -.35 and bounds['max'][1] > .35
                sides = [('left', 1), ('right', -1)] if split_y else [('whole', 1)]
                for side, sign in sides:
                    half = piece.copy()
                    if split_y:
                        cut_keep(half, (0, sign, 0), (0, 0, 0))
                    if not half.faces:
                        half.free()
                        continue
                    for fragment, solid in enumerate(connected_meshes(half), 1):
                        if abs(solid.calc_volume(signed=True)) < .05:
                            manifest['discarded_tiny_fragments'].append({'group': name, 'stage': 'cut', 'volume_mm3': abs(solid.calc_volume(signed=True))})
                            solid.free()
                            continue
                        assembled_bounds = mesh_bounds(solid)
                        # Rotation (det=+1) puts a custom glue face on the plate.
                        for vertex in solid.verts:
                            x, y, z = vertex.co
                            vertex.co = (x, sign*z, -sign*y)
                        pre_normalize = mesh_bounds(solid)['min']
                        vertices, triangles = normalized_triangles(solid)
                        stem = f'{name[5:]}_{island_number:02}_{segment+1:02}_{side}_{fragment:02}'
                        stl, mf = Path('stl')/(stem+'.stl'), Path('3mf')/(stem+'.3mf')
                        write_stl(output/stl, vertices, triangles)
                        write_3mf(output/mf, stem, vertices, triangles)
                        manifest['parts'].append({
                            'name': stem, 'label': spec['label'], 'source_group': name,
                            'accessory': not spec['visible'], 'assembly_side': side,
                            'segment': segment+1, 'segment_count': segment_count,
                            'stl': stl.as_posix(), '3mf': mf.as_posix(),
                            'orientation': 'custom_split_face_down' if split_y else 'side_down_review_supports',
                            'source_bounds_mm': assembled_bounds,
                            'print_normalization_offset_mm': pre_normalize,
                            'print_rotation_sign': sign, 'triangles': len(triangles),
                            'reinforcements': spec['supports'],
                        })
                        solid.free()
                    half.free()
                piece.free()
            island.free()
        merged.free()
        bpy.data.objects.remove(obj, do_unlink=True)
    if hashlib.sha256(source.read_bytes()).hexdigest() != source_hash:
        raise RuntimeError('Read-only source changed')
    (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    report = validate_directory(output)
    (output/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('PRINT_RESULT', json.dumps({'asset':asset_id,'passed':report['passed'],'pieces':report['part_count']}), flush=True)
    if not report['passed']:
        raise RuntimeError('Exported geometry failed independent readback; inspect validation.json')
    return manifest


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset',required=True,choices=[id for id in MODEL_IDS if id!='m7'])
    parser.add_argument('--voxel',type=float,default=.22)
    config=parser.parse_args(args)
    if not .18 <= config.voxel <= .30:
        raise ValueError('Miniature voxel resolution must be 0.18–0.30 mm')
    convert(config.asset, config.voxel)
