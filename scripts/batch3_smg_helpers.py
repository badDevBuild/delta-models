"""Owned helpers for four inert, solid game-reference miniature sculptures."""
import bpy, math, json
from mathutils import Vector
from model_helpers_amg import Sculpture

def wood(s):
    m=s.mat('Warm walnut artistic grain',(.105,.032,.011),0,.53)
    nt=m.node_tree;n=nt.nodes;l=nt.links;p=n.get('Principled BSDF')
    tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=2.8;tex.inputs['Detail'].default_value=2.3
    coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(.38,6,14)
    l.new(coord.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.21;ramp.color_ramp.elements[0].color=(.018,.0045,.0015,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(.15,.043,.010,1)
    l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.12;l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    return m

def optic(s,x,z,key='optic'):
    s.box('Optional solid ornament foot',key,(x,0,z+1),(13,8,3),s.metal,.45)
    s.poly('Optional compact sight shell',key,[(x-6,z+2),(x+6,z+2),(x+5.5,z+11),(x+3,z+13),(x-3.5,z+13),(x-6,z+10)],9,s.polymer,.7)
    for dx in [-6,6]:s.box('Opaque decorative lens',key,(x+dx,0,z+7.3),(.45,6.3,6.3),s.glass,.65)
    for sign in [-1,1]:s.cyl('Sight decorative side cap',key,(x+1,sign*4.4,z+6),1.5,.7,s.metal,'Y',.15)

def guard(s,pts,opening,key='grip'):
    a=s.poly('Solid fixed outer guard',key,pts,5.5,s.metal,.55);s.cut(a,s.poly('Exterior guard silhouette opening',key,opening,20,s.dark,.45))

def closed_front(s,key,x1,x2,z,r):
    s.cyl('Opaque solid forward sculpture',key,((x1+x2)/2,0,z),r,x2-x1,s.metal,'X',.18)
    s.cyl('Sealed dark front end',key,(x1,0,z),r*.82,.2,s.dark,'X',.05)
    for x in [x1+1.2,x2-1.6]:s.cyl('Solid front ornamental collar',key,(x,0,z),r+.45,1.1,s.edge,'X',.12)

def finish(s,description,imageurl):
    urls=[f'https://zilliongamer.com/delta-force/c/weapons/best-{s.asset}-build-delta-force',imageurl]
    notes=[description,'已于 2026-09-22 实际查看游戏基础配置截图；几何为独立艺术重建，未提取游戏资产。','隐藏面、截面厚度和细纹为艺术推断，文字和商标以抽象装饰替代；尺寸仅微缩雕塑设计尺寸。','实心封闭前端，无内部机构、膛室或真实接口。扳机/控制件为固定外观，网页拆装仅分组显示。','数字瞄具为可切换的艺术装饰；实体分件仅默认配置，按整体融合后左右胶合，当前未实机打印。']
    if s.asset in ['uzi','thompson']:notes.append('网页 GLB 使用显式棕色 PBR 回退；Blender 母版保留程序木纹，网页不含该程序纹理。')
    (s.out/'SOURCE_NOTES.md').write_text('# '+s.asset.upper()+' 外观参考\n\n'+'\n\n'.join(notes)+'\n\n'+'\n'.join('- '+u for u in urls)+'\n')
    result=s.finish(urls,notes)
    if s.asset in ['uzi','thompson']:
        from batch3_smg_gltf import apply_walnut_fallback
        result['web_material_fallback']=apply_walnut_fallback(result['glb'])
    # This reopens the saved master only for a separate optional-equipped render.
    bpy.ops.wm.open_mainfile(filepath=result['blend']);scene=bpy.context.scene
    for o in scene.objects:
        if o.type=='EMPTY' and not o.get('default_visible',True):
            for c in o.children_recursive:c.hide_render=False
    scene.cycles.samples=24;scene.render.filepath=str(s.out/'renders'/'optional.png');bpy.ops.render.render(write_still=True)
    return result
