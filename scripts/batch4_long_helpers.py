"""Art-only helpers local to the four long exterior sculptures of batch four."""
import bpy, math
from pathlib import Path

REF='https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops'

def scope(s,key,x,z,length=54):
    s.box('Decorative closed saddle',key,(x,0,z),(length*.72,9,3.4),s.metal,.5)
    for xx in [x-length*.22,x+length*.22]:
        s.box('Solid optic pillar',key,(xx,0,z+4),(5.4,7.5,7.4),s.metal,.6)
        s.cyl('Optic outer band',key,(xx,0,z+10),5.8,3.8,s.polymer,'X',.25)
    s.cyl('Solid scope sculpture',key,(x,0,z+10),4.8,length,s.metal,'X',.3)
    s.cone('Front decorative bell',key,(x-length*.5,0,z+10),7.1,4.8,11,s.metal,'X',.3)
    s.cyl('Opaque blue front disc',key,(x-length*.5-5.6,0,z+10),6.3,.35,s.glass,'X',.05)
    s.cyl('Opaque rear disc',key,(x+length*.5+.1,0,z+10),4,.3,s.glass,'X',.05)
    s.cyl('Fixed top dial',key,(x+3,0,z+16),3.7,4.5,s.metal,'Z',.3)
    s.cyl('Fixed side dial',key,(x+3,-6,z+10),3.2,4.5,s.metal,'Y',.3)

def grain(s,key,x0,x1,z0,rows,y,light,dark):
    for sign in [-1,1]:
        for row in range(rows):
            for step in range(8):
                x=x0+(x1-x0)*step/8; dx=(x1-x0)/8
                z=z0+row*1.8
                o=s.line('Fine surface wood grain',key,(x,sign*y,z+math.sin(step*.6+row)*.3),(x+dx,sign*y,z+math.sin((step+1)*.6+row)*.3),.07,light if row%2 else dark)
                o['print_skip']=True

def finish(s,image,notes):
    result=s.finish([REF,image],notes+['按游戏双侧截图独立重建的缩比外观。未见顶部、底部、截面和局部纹理为艺术推断，未提取游戏文件。','所有前端封闭，固定装饰件，无真实枪械尺寸、可用接口或内部机构。打印为实心微缩雕塑；可选瞄具仅用于数字展示。'])
    bpy.ops.wm.open_mainfile(filepath=result['blend'])
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and o.parent and o.parent.name.startswith('part_'):o.hide_render=False
    bpy.context.scene.cycles.samples=24
    bpy.context.scene.render.filepath=str(s.out/'renders'/'optional.png')
    bpy.ops.render.render(write_still=True)
    result['optional_render']=bpy.context.scene.render.filepath
    return result
