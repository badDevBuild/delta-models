"""Local art helpers for the four mixed batch-three sculptures only."""
import bpy, math, json
from pathlib import Path

REF='https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops'

def scope(s,key,x,z,length=47):
    s.box('Arbitrary decorative optic saddle',key,(x,0,z),(length*.68,7,2.6),s.metal,.45)
    for xx in [x-length*.22,x+length*.22]:
        s.box('Opaque optic pillar',key,(xx,0,z+4),(4.4,6,7),s.metal,.5)
        s.cyl('Sculpted optic ring',key,(xx,0,z+9),5.0,3.1,s.polymer,'X',.2)
    s.cyl('Solid optical ornament',key,(x,0,z+9),4.2,length,s.metal,'X',.3)
    s.cone('Front optic flare',key,(x-length*.5,0,z+9),6.2,4.2,9,s.metal,'X',.3)
    s.cyl('Front opaque lens',key,(x-length*.5-4.6,0,z+9),5.4,.3,s.glass,'X',.1)
    s.cyl('Rear opaque lens',key,(x+length*.5+.1,0,z+9),3.4,.3,s.glass,'X',.1)
    s.cyl('Optic fixed top dial',key,(x+3,0,z+15),3.2,4,s.metal,'Z',.25)
    s.cyl('Optic fixed side dial',key,(x+3,-5,z+9),2.8,4,s.metal,'Y',.25)

def grain(s,key,x0,x1,z0,rows,y,woodlight,wooddark):
    for side in [-1,1]:
        for row in range(rows):
            for step in range(10):
                x=x0+(x1-x0)*step/10;dx=(x1-x0)/10
                z=z0+row*2.1
                obj=s.line('Subtle carved wood grain',key,(x,side*y,z+math.sin(step*.7+row)*.28),(x+dx,side*y,z+math.sin((step+1)*.7+row)*.28),.065,woodlight if row%2 else wooddark)
                obj['print_skip']=True # Below nozzle width, surface colour relief only.

def finish(s,image,notes):
    result=s.finish([REF,image],notes+['基于游戏双侧截图的独立缩比重建；未提取游戏资源或复刻标识。未见截面、顶部和局部细纹为艺术推断。','实心非功能外观雕塑：前端封闭、操控装饰固定，无内部机构、真实尺寸或可用接口；可选配件仅供数字展示。'])
    # Reload the editable master: finish joins surfaces for GLB only.
    bpy.ops.wm.open_mainfile(filepath=result['blend'])
    scene=bpy.context.scene
    for obj in scene.objects:
        if obj.type=='MESH' and obj.parent and obj.parent.name.startswith('part_'):
            obj.hide_render=False
    scene.cycles.samples=24
    scene.render.filepath=str(s.out/'renders'/'optional.png')
    bpy.ops.render.render(write_still=True)
    result['optional_render']=scene.render.filepath
    return result
