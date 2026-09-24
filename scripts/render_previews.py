"""Render small catalog previews from the editable 3D masters, without saving them."""
from pathlib import Path
import hashlib
import json
import sys
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from model_catalog import MODEL_IDS

def render_all(asset_ids=None):
    results=[]
    for asset_id in (asset_ids if asset_ids is not None else MODEL_IDS):
        asset=ROOT/'assets'/asset_id
        source=asset/'source'/(asset_id+'.blend')
        before=hashlib.sha256(source.read_bytes()).hexdigest()
        bpy.ops.wm.open_mainfile(filepath=str(source))
        scene=bpy.context.scene
        roots=[o for o in scene.objects if o.type=='EMPTY' and o.name.startswith('part_')]
        coords=[]
        for group in roots:
            visible=bool(group.get('default_visible',True))
            for child in group.children_recursive:
                child.hide_render=not visible
                if child.type=='MESH' and visible:
                    coords.extend(child.matrix_world@Vector(v) for v in child.bound_box)
        lo=Vector([min(v[i] for v in coords) for i in range(3)])
        hi=Vector([max(v[i] for v in coords) for i in range(3)])
        center=(lo+hi)/2;size=hi-lo
        camera=scene.camera
        camera.location=center+Vector((-size.x*.20,-size.x*1.8,size.x*.32))
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.type='ORTHO';camera.data.ortho_scale=max(size.x,size.z*1.667)*1.23
        camera.data.clip_end=5000
        scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=True
        scene.render.resolution_x=600;scene.render.resolution_y=360;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG';scene.render.image_settings.compression=80
        destination=asset/'renders/catalog.png';scene.render.filepath=str(destination)
        bpy.ops.render.render(write_still=True)
        if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise RuntimeError('Source modified')
        results.append({'id':asset_id,'source_sha256':before,'png_bytes':destination.stat().st_size,
                        'preview_sha256':hashlib.sha256(destination.read_bytes()).hexdigest()})
    report_path=ROOT/'reports/catalog-renders.json'
    existing={r['id']:r for r in json.loads(report_path.read_text())} if report_path.exists() else {}
    existing.update({r['id']:r for r in results})
    report_path.write_text(json.dumps([existing[id] for id in MODEL_IDS if id in existing],indent=2)+'\n')
    return results

if __name__=='__main__':result={'renders':render_all()}
