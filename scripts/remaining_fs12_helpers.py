"""Root-owned FS12 miniature exterior helpers, independent of active workers."""
import bpy, math, json, hashlib

from pathlib import Path

from mathutils import Vector

from model_helpers_amg import Sculpture

def begin(asset,length,groups):
 s=Sculpture(asset,length)
 for key,label in groups:s.part(key,label)
 s.part('optic','可选紧凑光学装饰',False)
 return s

def optic(s,x,z,q=1):
 k='optic';s.box('Solid optical saddle',k,(x,0,z),(15*q,10*q,2.4*q),s.metal,.35*q)
 s.box('Optic opaque body',k,(x,0,z+3*q),(12*q,8*q,5*q),s.polymer,.6*q)
 s.poly('Optic hood silhouette',k,[(x-5*q,z+4*q),(x-4*q,z+13*q),(x+4*q,z+13*q),(x+6*q,z+6*q),(x+5*q,z+4*q)],8*q,s.metal,.4*q)
 for a in [-5,5]:s.box('Opaque glass front rear',k,(x+a*q,0,z+8.5*q),(.3*q,6*q,5*q),s.glass,.3*q)
 s.cyl('Fixed optic dial',k,(x+1*q,-4.5*q,z+3*q),1.7*q,1.5*q,s.edge,'Y',.15*q)

def stipple(s,key,x,z,w,h,y,mat=None,pitch=2.3):
 for sign in [-1,1]:
  for i in range(int(w/pitch)):
   for j in range(int(h/pitch)):
    s.box('Shallow stippled surface dot',key,(x+(i+.5)*pitch,sign*y,z+(j+.5)*pitch),(.56,.24,.56),mat or s.metal,.15)

def guard(s,x,z,w=27,h=19,key='controls',mat=None):
 o=s.poly('Fixed guard exterior silhouette',key,[(x-w/2,z),(x+w/2,z),(x+w/2+1,z-h+4),(x+w/2-3,z-h),(x-w/2+3,z-h),(x-w/2-2,z-h+5)],6.5,mat or s.metal,.65)
 s.cut(o,s.poly('Open silhouette of guard',key,[(x-w/2+3,z-3),(x+w/2-3,z-3),(x+w/2-3,z-h+5),(x+w/2-5,z-h+3),(x-w/2+5,z-h+3),(x-w/2+2,z-h+6)],20,s.dark,.6))
 s.poly('Fixed curved trigger ornament',key,[(x+2,z+1),(x+4,z+1),(x+4,z-5),(x+2,z-10),(x-2,z-11),(x-3,z-10),(x,z-8),(x+2,z-4)],3.1,s.polymer,.35)

def grip(s,key,x,z,mat=None,y=7.5,scale=1):
 pts=[(x-6,z),(x+6,z+1),(x+8,z-8),(x+19,z-35),(x+17,z-41),(x+3,z-43),(x-2,z-32),(x-4,z-17),(x-9,z-5)]
 pts=[(x+(a-x)*scale,z+(b-z)*scale) for a,b in pts]
 s.poly('Sloped solid grip',key,pts,y*2,mat or s.polymer,.9)
 for sign in [-1,1]:
  p=[(x-3,z-5),(x+3,z-5),(x+4,z-12),(x+14,z-34),(x+12,z-37),(x+4,z-37),(x-1,z-23)]
  s.poly('Grip textured field',key,[(x+(a-x)*scale,z+(b-z)*scale) for a,b in p],.5,s.rubber,.45,y=sign*(y-.04))
  for j in range(11):
   zz=z-(7+j*2.5)*scale;xx=x+max(0,(z-zz-10))*.32
   s.line('Grip raised shallow chevron',key,(xx-2.5*scale,sign*(y+.26),zz),(xx+2.5*scale,sign*(y+.26),zz+.7*scale),.23,s.metal)

def finish(s,sources,notes,cut=None):
 bpy.context.view_layer.update()
 pts=[o.matrix_world@Vector(v) for p in s.parts.values() if p['default_visible'] for o in p.children_recursive if o.type=='MESH' for v in o.bound_box]
 q=s.length/(max(p.x for p in pts)-min(p.x for p in pts))
 for o in s.col.objects:
  if o.type=='MESH':
   o.location*=q;o.scale*=q;s.active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
   for mod in o.modifiers:
    if mod.type=='BEVEL':mod.width*=q
 if cut is not None:s.scene['print_segment_breaks_x_mm']=[cut*q]
 n=notes+['参考游戏画面独立重建；隐藏面、顶部和细小尺寸为艺术推断，无游戏资源提取或商标复刻。','微缩实心非功能外观雕塑；前端封闭，无膛室、贯穿前孔、内构或可用接口。可选附件仅用于网页外观演示。']
 result=s.finish(sources,n)
 source=Path(result['blend']);sha=hashlib.sha256(source.read_bytes()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=str(source))
 for o in bpy.context.scene.objects:
  if o.type=='MESH' and o.parent and o.parent.name.startswith('part_'):o.hide_render=False
 bpy.context.scene.cycles.samples=24;bpy.context.scene.render.filepath=str(s.out/'renders'/'optional.png');bpy.ops.render.render(write_still=True)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
 (s.out/'SOURCE_NOTES.md').write_text('# '+s.asset+' 外观依据\n\n'+'\n'.join('- '+u for u in sources)+'\n\n'+'\n'.join('- '+x for x in n)+'\n\n图像为本次实际目视参考，未复制游戏模型、贴图或官方图片到交付包。实机打印尚未进行。\n')
 result['source_sha256']=sha;result['glb_sha256']=hashlib.sha256(Path(result['glb']).read_bytes()).hexdigest();return result
