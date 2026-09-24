"""Helpers limited to batch-four compact exterior sculptures."""
import bpy
from pathlib import Path
REF='https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops'

def optic(s,key,x,z,scale=1):
    q=scale
    s.box('Solid miniature optic saddle',key,(x,0,z),(16*q,10*q,2*q),s.metal,.4*q)
    s.box('Opaque optic lower housing',key,(x,0,z+3.4*q),(13*q,9*q,5.2*q),s.polymer,.7*q)
    s.poly('Hood sculpture silhouette',key,[(x-5*q,z+5*q),(x-4*q,z+13*q),(x+4*q,z+13*q),(x+6*q,z+7*q),(x+5*q,z+5*q)],8*q,s.metal,.5*q)
    s.box('Opaque front optic colour',key,(x-5.05*q,0,z+9*q),(.35*q,6.1*q,5.6*q),s.glass,.5*q)
    s.box('Opaque rear optic colour',key,(x+4.95*q,0,z+9*q),(.35*q,6.1*q,5.6*q),s.glass,.5*q)
    s.cyl('Fixed optic side dial',key,(x+1*q,-5*q,z+4*q),1.8*q,1.6*q,s.edge,'Y',.15*q)

def finish(s,image,notes):
    r=s.finish([REF,image],notes+['依据游戏默认双侧截图独立缩比重建；无资源提取，未复刻商标。顶部、隐藏面和细小材质为艺术推断。','实心非功能外观雕塑；前端封闭，无内构、实际尺寸或可用接口；可选附件仅用于数字外观展示。'])
    bpy.ops.wm.open_mainfile(filepath=r['blend'])
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and o.parent and o.parent.name.startswith('part_'):o.hide_render=False
    bpy.context.scene.cycles.samples=24
    bpy.context.scene.render.filepath=str(s.out/'renders'/'optional.png')
    bpy.ops.render.render(write_still=True)
    r['optional_render']=bpy.context.scene.render.filepath
    return r
