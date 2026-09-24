"""Read saved Blender PBR inputs and compare the actual exported GLB factors.

Run through Blender MCP. Linked/procedural inputs require an explicit manual
review rather than silently counting the unlinked default as the material.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import struct
import sys
import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from model_catalog import MODELS


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_batch(batch):
    rows = []
    for spec in [m for m in MODELS if m['batch'] == batch]:
        asset_id = spec['id']
        asset = ROOT / 'assets' / asset_id
        source = asset / 'source' / f'{asset_id}.blend'
        glb = asset / 'web' / f'{asset_id}.glb'
        source_hash, glb_hash = digest(source), digest(glb)
        data = glb.read_bytes()
        assert data[:4] == b'glTF' and struct.unpack_from('<I', data, 4)[0] == 2
        size, kind = struct.unpack_from('<II', data, 12)
        assert kind == 0x4E4F534A
        document = json.loads(data[20:20 + size])
        bpy.ops.wm.open_mainfile(filepath=str(source))
        used_names = {m.name for o in bpy.context.scene.objects if o.type == 'MESH'
                      and any(p.name.startswith('part_') for p in [o.parent] if p)
                      for m in o.data.materials if m}
        records = []
        for exported in document.get('materials', []):
            name = exported.get('name', '')
            assert name in used_names, f'{asset_id}: unexpected exported material {name}'
            material = bpy.data.materials[name]
            nodes = material.node_tree.nodes if material.use_nodes else []
            shaders = [node for node in nodes if node.type == 'BSDF_PRINCIPLED']
            assert len(shaders) == 1, f'{asset_id}/{name}: manual shader review required'
            shader = shaders[0]
            source_values = {
                'baseColorFactor': list(shader.inputs['Base Color'].default_value),
                'metallicFactor': shader.inputs['Metallic'].default_value,
                'roughnessFactor': shader.inputs['Roughness'].default_value,
            }
            pbr = exported.get('pbrMetallicRoughness', {})
            exported_values = {'baseColorFactor': pbr.get('baseColorFactor', [1, 1, 1, 1]),
                               'metallicFactor': pbr.get('metallicFactor', 1),
                               'roughnessFactor': pbr.get('roughnessFactor', 1)}
            linked = [key for key in ['Base Color', 'Metallic', 'Roughness', 'Normal']
                      if shader.inputs[key].is_linked]
            differences = []
            for key, actual in exported_values.items():
                expected = source_values[key]
                a = actual if isinstance(actual, list) else [actual]
                b = expected if isinstance(expected, list) else [expected]
                if any(abs(x - y) > 1e-5 for x, y in zip(a, b)):
                    differences.append(key)
            records.append({'name': name, 'passed': not differences and not linked,
                            'source': source_values, 'exported': exported_values,
                            'linked_inputs_requiring_review': linked, 'different_factors': differences})
        assert digest(source) == source_hash and digest(glb) == glb_hash
        rows.append({'id': asset_id, 'source_sha256': source_hash, 'glb_sha256': glb_hash,
                     'passed': bool(records) and all(m['passed'] for m in records), 'materials': records})
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'batch': batch,
              'scope': 'Actual saved Blender material inputs and GLB PBR JSON; no browser lighting claim.',
              'passed': bool(rows) and all(r['passed'] for r in rows),
              'models': rows, 'material_count': sum(len(r['materials']) for r in rows)}
    report = ROOT / 'reports' / f'batch{batch}-material-review.json'
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return {'passed': result['passed'], 'models': len(rows), 'materials': result['material_count'],
            'report': str(report), 'review_required': [r['id'] for r in rows if not r['passed']]}
