"""Only the ten remaining compact-family miniature exterior artworks.
All coordinates are arbitrary miniature art dimensions, never real interfaces.
"""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Vector
from model_helpers_amg import Sculpture
REF='https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops'

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

def slot(s,obj,key,x,z,w,h,depth,y):
 for sign in [-1,1]:
  s.cut(obj,s.box('Shallow blind exterior recess cutter',key,(x,sign*y,z),(w,depth,h),s.dark,min(.8,h*.3)))
  s.box('Blind recess filled shadow',key,(x,sign*(y-depth/2+.12),z),(w-.5,.24,h-.5),s.dark,min(.5,h*.2))

def inset(s,key,points,depth,mat,y,b=.3):
 for sign in [-1,1]:s.poly('Symmetric raised exterior panel',key,points,depth,mat,b,y=sign*y)

def stipple(s,key,x,z,w,h,y,mat=None,pitch=2.3):
 for sign in [-1,1]:
  for i in range(int(w/pitch)):
   for j in range(int(h/pitch)):
    s.box('Shallow stippled surface dot',key,(x+(i+.5)*pitch,sign*y,z+(j+.5)*pitch),(.56,.24,.56),mat or s.metal,.15)

def screws(s,key,coords,y,r=.8):
 for sign in [-1,1]:
  for x,z in coords:s.screw('Fixed exterior fastener',key,x,z,sign*y,r)

def guard(s,x,z,w=27,h=19,key='controls',mat=None):
 o=s.poly('Fixed guard exterior silhouette',key,[(x-w/2,z),(x+w/2,z),(x+w/2+1,z-h+4),(x+w/2-3,z-h),(x-w/2+3,z-h),(x-w/2-2,z-h+5)],6.5,mat or s.metal,.65)
 s.cut(o,s.poly('Open silhouette of guard',key,[(x-w/2+3,z-3),(x+w/2-3,z-3),(x+w/2-3,z-h+5),(x+w/2-5,z-h+3),(x-w/2+5,z-h+3),(x-w/2+2,z-h+6)],20,s.dark,.6))
 s.poly('Fixed curved trigger ornament',key,[(x+2,z+1),(x+4,z+1),(x+4,z-5),(x+2,z-10),(x-2,z-11),(x-3,z-10),(x,z-8),(x+2,z-4)],3.1,s.polymer,.35)

def sights(s,a,b,z,width=6):
 s.rail('sights',a,b,z,width,4.1)
 for x in [a+7,b-7]:
  s.box('Sight base', 'sights',(x,0,z+2.5),(8,8,2.7),s.metal,.35)
  s.poly('Fixed sight standing blade','sights',[(x-2,z+3),(x-2,z+9),(x,z+11),(x+2,z+9),(x+2,z+3)],3.5,s.metal,.35)
  s.box('Sight small opaque front marker','sights',(x-.1,-1.86,z+8),(1.3,.3,1.3),s.edge,.18)

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

def front(s,key,start,end,z,r=3.6,cap=4.5):
 s.cyl('Solid sealed front rod',key,((start+end)/2,0,z),r,end-start,s.steel,'X',.22)
 s.cyl('Solid front collar',key,(start+2,0,z),cap,4,s.metal,'X',.3)
 s.cyl('Opaque closed terminal disc',key,(start-.06,0,z),cap*.63,.15,s.dark,'X',.04)

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

def build_pistol(asset,length,kind):
 labels=[('frame','实心聚合物下壳'),('slide','分层封闭滑套外观'),('front','封闭前端与下方短导轨'),('grip','双侧握把纹理'),('controls','固定护圈与操控装饰'),('base','握把底部实心底盖'),('sights','低矮机械瞄具')]
 s=begin(asset,length,labels)
 gun=s.mat('Dark satin slide',(.105,.115,.126),.63,.43)
 if kind=='g17':
  slide=[(-40,23),(-40,34),(31,34),(32,32),(32,23)]
  frame=[(-39,23),(33,23),(34,19),(30,15),(28,4),(37,-22),(37,-27),(20,-29),(17,-24),(10,2),(7,10),(-8,11),(-9,17),(-37,17)]
  gp=[(14,10),(26,11),(24,5),(34,-21),(32,-25),(22,-25),(17,-14),(10,4)]
  base=[(19,-25),(36,-24),(38,-27),(36,-30),(18,-30)]
  serrations=range(7);sx=18;frontx=-41.5;frame_mat=s.polymer
 elif kind=='qsz':
  slide=[(-39,23),(-38,34),(26,34),(29,31),(35,23),(32,20),(-37,20)]
  frame=[(-38,22),(32,22),(35,17),(29,12),(26,3),(31,-23),(30,-28),(12,-28),(12,-24),(14,-3),(9,9),(-11,10),(-13,18),(-38,18)]
  gp=[(16,9),(25,7),(25,-1),(28,-23),(14,-24),(16,-5),(12,4)]
  base=[(12,-24),(30,-24),(32,-28),(31,-30),(10,-30)]
  serrations=range(10);sx=4;frontx=-40;frame_mat=s.polymer
 else:
  slide=[(-40,22),(-40,29),(-37,34),(-34,32),(17,32),(24,35),(31,35),(36,28),(36,22)]
  frame=[(-39,23),(33,23),(38,20),(34,15),(31,10),(31,4),(41,-25),(40,-29),(20,-29),(17,-7),(14,6),(6,11),(-5,11),(-8,18),(-39,18)]
  gp=[(20,13),(29,13),(29,5),(37,-25),(23,-26),(22,-8),(17,6)]
  base=[(20,-26),(40,-26),(42,-29),(40,-31),(18,-31)]
  serrations=range(12);sx=9;frontx=-41;frame_mat=gun
 s.poly('Solid entire lower frame silhouette','frame',frame,11.4,frame_mat,.85)
 sl=s.poly('Solid closed slide exterior','slide',slide,12.0,gun,.65)
 s.box('Slide top crown','slide',(-3,0,33),(60,9.7,2.2),gun,.5)
 if kind=='beretta':
  s.box('Open-top visual dark closed bedding','slide',(-13,0,33.3),(49,7.2,1.2),s.dark,.45)
  s.cyl('Visible solid upper spine','slide',(-13,0,33.6),2.35,45,s.steel,'X',.25)
 if kind=='qsz':
  for sign in [-1,1]:s.poly('Front diagonal slide facet','slide',[(-37,33),(-27,33),(-22,23),(-35,23)],.55,s.edge,.35,y=sign*5.95)
 for sign in [-1,1]:
  s.box('Closed upper side chamber marking','slide',(7,sign*6.0,31),(14,.24,2.3),s.dark,.5)
  s.box('Lower slide seam','slide',(-6,sign*6.05,24),(66,.23,.75),s.dark,.17)
  for j in serrations:
   x=sx+j*1.25
   a=s.box('Rear angled shallow slide serration','slide',(x,sign*6.06,28.6),(.58,.4,7.1),s.polymer,.12);a.rotation_euler[1]=-.27 if kind!='g17' else 0
  s.poly('Textured separate grip panel','grip',gp,.75,s.polymer,.55,y=sign*5.8)
  for j in range(13):
   z=5-j*2.1
   cx=(26+max(0,-z)*.25) if kind=='beretta' else ((19+max(0,-z)*.31) if kind=='g17' else (21+max(0,-z)*.10))
   for i in range(5):
    s.box('Small grip checker relief','grip',(cx-4+i*1.8,sign*6.26,z),(.64,.22,.64),s.metal,.14)
  if kind!='g17':
   for x,z in ([(23,12),(30,-20)] if kind=='beretta' else [(18,8),(23,-23)]):s.screw('Grip fixed decorative screw','grip',x,z,sign*6.31,.74)
  s.poly('Fixed thumb ledge','controls',[(10,22),(19,22),(20,20),(14,19),(10,20)],.9,s.steel,.3,y=sign*5.8)
  s.box('Frame fixed side button','controls',(13.2,sign*6.1,15),(2.8,1.0,3.1),s.metal,.3)
 if kind=='g17':
  for j in range(3):s.box('Grip front finger relief','frame',(13.8+j*1.75,0,-2-j*6.5),(3.4,8.0,2.2),s.polymer,.65)
 guard(s,-1,17,23,18,'controls',s.polymer)
 s.poly('Solid grip bottom shoe','base',base,13,s.polymer,.45)
 front(s,'front',frontx,-34.7,27.5,2.5,3)
 s.box('Lower foreframe rail base','front',(-25,0,16.6),(26,10.5,2.4),s.polymer,.4)
 if kind!='beretta':
  for x in [-34,-30,-26]:s.box('Underframe decorative short ridge','front',(x,0,15.3),(2.4,11.0,1.4),s.metal,.25)
 s.box('Low front sight blade','sights',(-35,0,35.2),(3.1,2.2,2.8),s.polymer,.3)
 s.poly('Solid rear sight outline','sights',[(24,33),(25,36.4),(29,36.4),(31,33)],6,s.polymer,.35)
 for sign in [-1,1]:s.box('Rear sight pale dot','sights',(26.8,sign*2.15,36.0),(.7,.6,.28),s.steel,.12)
 if kind!='g17':
  s.poly('Fixed rear crest ornament','controls',[(31,24),(33,28),(38,31),(40,29),(38,26),(35,24)],3.7,gun,.4)
 optic(s,10,34.5,.58)
 urls={'g17':'https://www.imfdb.org/images/thumb/1/18/DFHO_G17.jpg/600px-DFHO_G17.jpg','qsz':'https://www.imfdb.org/images/thumb/5/5d/DFHO_QSZ92.jpg/600px-DFHO_QSZ92.jpg','beretta':'https://www.imfdb.org/images/thumb/a/a4/DFHO_M9.jpg/600px-DFHO_M9.jpg'}
 notes={'g17':'根据默认游戏双侧图重建平直窄滑套、仅后侧直纹、斜握把指槽和细密点纹；与 G18 前后纹路区别保留。','qsz':'根据默认游戏双侧图重建前斜切滑套、后部斜向纹、近直立握把、后方固定凸起和下方短轨。','beretta':'根据更新后93R游戏默认双侧图重建上部凹面、露出实心金属脊、弧形握把和后斜纹；没有采用旧92FS参考图的前侧独立纹。'}
 return finish(s,[REF,urls[kind]],[notes[kind],'光学附件为自定小型展示装饰；所有可见开口只表达外壳阴影，前端、上壳和握把底部均封闭。'])
