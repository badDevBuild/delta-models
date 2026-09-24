"""Open final Blender masters read-only and compare saved scene data to manifests.

Invoke through Blender MCP in a background process; never saves the opened files.
"""
from pathlib import Path
import hashlib
import json
import sys
from datetime import datetime, timezone
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from model_catalog import MODELS


def audit_batch(batch):
    rows = []
    for spec in [m for m in MODELS if m['batch'] == batch]:
        asset_id = spec['id']
        asset = ROOT / 'assets' / asset_id
        source = asset / 'source' / f'{asset_id}.blend'
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        manifest = json.loads((asset / 'manifest.json').read_text())
        bpy.ops.wm.open_mainfile(filepath=str(source))
        scene = bpy.context.scene
        scene.view_layers[0].update()
        assert scene.unit_settings.system == 'METRIC'
        assert abs(scene.unit_settings.scale_length - .001) < 1e-8
        roots = {o.name: o for o in scene.objects if o.type == 'EMPTY' and o.name.startswith('part_')}
        assert set(roots) == {p['id'] for p in manifest['parts']}, asset_id
        base_coords = []
        count = 0
        parts = []
        for item in manifest['parts']:
            group = roots[item['id']]
            assert group.get('label') == item['label']
            assert bool(group.get('default_visible', True)) == item['default_visible']
            meshes = [o for o in group.children_recursive if o.type == 'MESH']
            assert len(meshes) == item['meshes'] and meshes
            assert all(o.data.vertices and o.data.polygons for o in meshes)
            count += len(meshes)
            if item['default_visible']:
                base_coords += [o.matrix_world @ Vector(corner) for o in meshes for corner in o.bound_box]
            parts.append({'id': group.name, 'meshes': len(meshes), 'default_visible': item['default_visible']})
        length = max(p.x for p in base_coords) - min(p.x for p in base_coords)
        assert abs(length - manifest['display_length_mm']) < .01
        assert count == manifest['mesh_count']
        assert hashlib.sha256(source.read_bytes()).hexdigest() == before, 'Source changed during read-only audit'
        rows.append({'id': asset_id, 'passed': True, 'source_sha256': before,
                     'active_scene': scene.name, 'scale_length': scene.unit_settings.scale_length,
                     'base_length_mm': length, 'editable_meshes': count, 'parts': parts})
    assert rows
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'batch': batch, 'passed': True,
              'scope': 'Actual saved Blender scenes opened by Blender MCP; no sources saved or rendered.', 'models': rows}
    output = ROOT / 'reports' / f'batch{batch}-blender-readback.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return {'passed': True, 'models': len(rows), 'report': str(output)}
