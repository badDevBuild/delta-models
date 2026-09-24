"""Export a read-only Blender master with one mesh per logical exterior group.

Materials remain separate primitives inside each mesh. The editable master and
all print geometry stay untouched; only the display GLB is replaced.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import bpy

ROOT=Path(__file__).resolve().parents[1]

def export(asset_id):
    asset=ROOT/'assets'/asset_id
    source=asset/'source'/(asset_id+'.blend')
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(source))
    original=bpy.context.scene
    original.view_layers[0].update()
    deps=bpy.context.evaluated_depsgraph_get()
    roots=[o for o in original.objects if o.type=='EMPTY' and o.name.startswith('part_')]
    target=bpy.data.scenes.new('WEB_DISPLAY_EXPORT')
    target.unit_settings.system='METRIC';target.unit_settings.scale_length=.001
    count=0
    for root in roots:
        name=root.name
        root.name='source__'+name
        group=bpy.data.objects.new(name,None);target.collection.objects.link(group)
        for key,value in root.items():group[key]=value
        vertices=[];faces=[];materials=[];indices=[];smooth=[]
        for child in root.children_recursive:
            if child.type!='MESH':continue
            evaluated=child.evaluated_get(deps);mesh=evaluated.to_mesh()
            offset=len(vertices)
            vertices.extend(tuple(child.matrix_world@v.co) for v in mesh.vertices)
            material_map=[]
            for material in mesh.materials:
                if material not in materials:materials.append(material)
                material_map.append(materials.index(material))
            for poly in mesh.polygons:
                faces.append(tuple(offset+i for i in poly.vertices))
                indices.append(material_map[poly.material_index] if material_map else 0)
                smooth.append(poly.use_smooth)
            evaluated.to_mesh_clear()
        mesh=bpy.data.meshes.new(asset_id+'_'+name+'_geometry');mesh.from_pydata(vertices,[],faces);mesh.update()
        for material in materials:mesh.materials.append(material)
        for index,poly in enumerate(mesh.polygons):
            poly.material_index=indices[index];poly.use_smooth=smooth[index]
        obj=bpy.data.objects.new('surface_'+name[5:],mesh);target.collection.objects.link(obj);obj.parent=group
        count+=1
    bpy.context.window.scene=target
    bpy.ops.object.select_all(action='DESELECT')
    for obj in target.objects:obj.select_set(True)
    destination=asset/'web'/(asset_id+'.glb')
    bpy.ops.export_scene.gltf(filepath=str(destination),export_format='GLB',use_selection=True,
        use_active_scene=True,export_apply=True,export_extras=True,export_yup=True,export_animations=False)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=source_hash:
        raise RuntimeError('Read-only master changed')
    report={'asset':asset_id,'logical_groups':count,'source_unchanged':True,'source_sha256':source_hash,
            'glb_bytes':destination.stat().st_size,'glb_sha256':hashlib.sha256(destination.read_bytes()).hexdigest()}
    (asset/'web/export-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--asset',required=True)
    result=export(parser.parse_args(args).asset)
