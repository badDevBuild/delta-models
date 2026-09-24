"""Owned final-batch miniature exterior art utilities. No operational geometry."""
import bpy,math,json,hashlib
from pathlib import Path
from model_helpers_amg import Sculpture
from rifle_batch3_helpers import side_plate,optic,sight
from batch4_rifle_helpers import guard
REFS={
'car15':'https://www.imfdb.org/images/thumb/1/1b/DFHO_Colt723.jpg/600px-DFHO_Colt723.jpg',
'k437':'https://www.imfdb.org/images/thumb/4/46/DFHO_HK433.jpg/600px-DFHO_HK433.jpg',
'ash12':'https://www.imfdb.org/images/thumb/2/23/DFHO_SHAK12.jpg/600px-DFHO_SHAK12.jpg',
'sg552':'https://www.imfdb.org/images/thumb/2/27/DFHO_SIGSG552.jpg/600px-DFHO_SIGSG552.jpg',
'kc17':'https://www.imfdb.org/images/thumb/0/0b/DFHO_AM17.jpg/600px-DFHO_AM17.jpg',
'mk47':'https://www.imfdb.org/images/thumb/4/4a/DFHO_MK47Dissent.jpg/600px-DFHO_MK47Dissent.jpg',
'ptr32':'https://www.imfdb.org/images/thumb/2/28/DFHO_PTR32.jpg/600px-DFHO_PTR32.jpg',
'ci19':'https://www.imfdb.org/images/thumb/0/04/DFHO_QBZ191n.jpg/600px-DFHO_QBZ191n.jpg',
'mcxlt':'https://img.gamewith.jp/article/thumbnail/rectangle/542359.png?date=1769744724',
'ar57':'https://img.gamewith.jp/article/thumbnail/rectangle/556174.png?date=1776335208'}
def setup(id,L,labels=None):
 s=Sculpture(id,L)
 names=labels or [('receiver','折面机匣外观'),('lower','下部机匣与固定护圈'),('handguard','护木外观'),('front','封闭前端'),('magazine','实心弹匣外观'),('grip','斜握把外观'),('stock','枪托外观'),('sights','顶部脊与机械瞄具'),('optic','可选紧凑瞄具')]
 for k,label in names:s.part(k,label,k!='optic')
 return s

def front(s,a,b,z=23,r=2.6,collar=True):
 s.cyl('Sealed decorative forward rod','front',((a+b)/2,0,z),r,b-a,s.metal,'X',.15)
 s.cyl('Closed flat front face','front',(a-.07,0,z),r*.92,.16,s.dark,'X',.025)
 if collar:
  s.cyl('Front thick closed collar','front',(a+4,0,z),r+1.2,7,s.metal,'X',.2)
  for x in [a+1,a+3,a+5]:s.cyl('Collar shallow annular detail','front',(x,0,z),r+1.35,.6,s.edge,'X',.1)

def receiver(s,pts,depth=19,mat=None):
 mat=mat or s.metal
 s.poly('Filled faceted main receiver','receiver',pts,depth,mat,.7)
 x0=min(x for x,z in pts);x1=max(x for x,z in pts);z0=min(z for x,z in pts);z1=max(z for x,z in pts)
 for sign in [-1,1]:
  s.box('Shallow long side seam','receiver',((x0+x1)/2,sign*depth/2,z0+5),(x1-x0-8,.5,1.15),s.dark,.22)
  for x in [x0+5,x0+(x1-x0)*.45,x1-6]:s.screw('Receiver attached embossed stud','receiver',x,z0+9,sign*(depth/2-.1),.8)
 s.box('Blind filled side port','receiver',((x0+x1)/2,depth/2, (z0+z1)/2),(min(30,(x1-x0)*.4),.65,7),s.dark,.6)
 s.box('Opaque metallic port inset','receiver',((x0+x1)/2,depth/2+.3,(z0+z1)/2),(min(25,(x1-x0)*.34),.4,4.4),s.steel,.4)
 s.box('Closed inset lower bead','receiver',((x0+x1)/2,depth/2+.4,(z0+z1)/2-3),(min(30,(x1-x0)*.4),.65,1.1),s.edge,.25)

def lower(s,x=0,z=9):
 s.poly('Lower solid sculptural envelope','lower',[(x-9,z+7),(x+50,z+7),(x+51,z-2),(x+39,z-9),(x+17,z-9),(x-9,z-4)],17,s.metal,.6)
 s.poly('Flared solid magazine well','lower',[(x-9,z+4),(x+14,z+3),(x+14,z-10),(x-9,z-8)],18,s.metal,.55)
 for sign in [-1,1]:
  s.cyl('Fixed side control roundel','lower',(x+37,sign*8.4,z),2.2,1,s.edge,'Y',.18)
  s.poly('Static embossed selector','lower',[(x+36,z+1),(x+31,z-3),(x+32,z-5),(x+39,z)],.8,s.metal,.25,y=sign*9)
  s.box('Blank inset inscription field','lower',(x+3,sign*9,z-3),(13,.5,4),s.edge,.35)
 guard(s,'lower',[(x+12,z-4),(x+41,z-4),(x+42,z-17),(x+35,z-21),(x+18,z-21),(x+12,z-15)],[(x+16,z-8),(x+37,z-8),(x+37,z-14),(x+33,z-17),(x+20,z-17),(x+17,z-13)],6)
 s.poly('Attached static trigger relief','lower',[(x+27,z-6),(x+30,z-6),(x+30,z-12),(x+27,z-15),(x+25,z-14),(x+27,z-10)],3,s.metal,.25)

def grip(s,x=37,z=3,kind='ridges',mat=None):
 mat=mat or s.polymer
 pts=[(x-3,z+3),(x+12,z+4),(x+14,z-8),(x+29,z-35),(x+14,z-40),(x+1,z-15),(x-5,z-6)]
 s.poly('Solid sloping grip silhouette','grip',pts,14,mat,1)
 side_plate(s,'Inset grip molded side panel','grip',[(x+3,z-9),(x+10,z-9),(x+23,z-33),(x+15,z-34)],6.8,s.rubber,.55,.5)
 for sign in [-1,1]:
  for row in range(10):
   s.box('Molded grip fine rib','grip',(x+8+row*.95,sign*7.12,z-12-row*1.85),(6,.35,.65),mat,.15)
  s.screw('Blind grip heel stud','grip',x+18,z-31,sign*7,.7)

def magazine(s,pts,depth=14,kind='ribs',mat=None):
 mat=mat or s.polymer;s.poly('Completely solid magazine form','magazine',pts,depth,mat,.65)
 # Surface details follow a centerline chosen from the silhouette, remaining inset.
 top=max(z for x,z in pts);bottom=min(z for x,z in pts)
 def span(z):
  xs=[]
  for (x1,z1),(x2,z2) in zip(pts,pts[1:]+pts[:1]):
   if (z1<=z<z2) or (z2<=z<z1):xs.append(x1+(z-z1)*(x2-x1)/(z2-z1))
  return min(xs),max(xs)
 for sign in [-1,1]:
  for row in range(int((top-bottom-8)/6)):
   z=top-6-row*6;a,b=span(z)
   s.box('Magazine transverse embossed bead','magazine',((a+b)/2,sign*depth/2,z),(max(2,b-a-5),.5,.9),s.edge,.2)
   if kind=='grid':
    for frac in [.25,.72]:s.box('Magazine short cell wall','magazine',(a+(b-a)*frac,sign*(depth/2+.05),z-2),(1.1,.6,4),mat,.18)

def buffer_stock(s,a,b,z=23,style='triangle'):
 s.cyl('Solid stock neck','stock',(a+10,0,z),5.6,23,s.metal,'X',.3)
 s.poly('Upper stock cheek solid','stock',[(a+18,z+7),(b-1,z+7),(b,z+3),(b,z-9),(a+22,z-9)],19,s.polymer,.9)
 if style=='triangle':
  o=s.poly('Fixed triangular stock frame','stock',[(a+21,z-4),(b,z-4),(b,z-34),(b-6,z-34),(a+29,z-15)],15,s.polymer,.85)
  s.cut(o,s.poly('Stock open silhouette cutter','stock',[(a+35,z-10),(b-7,z-10),(b-7,z-26),(b-12,z-25)],30,s.dark,.5))
 else:
  s.poly('Fixed low stock lower wedge','stock',[(a+24,z-5),(b,z-5),(b,z-27),(b-9,z-22),(a+41,z-11)],15,s.polymer,.75)
 s.box('Stock sealed heel','stock',(b,0,z-12),(3,20,43),s.rubber,.7)
 for zz in range(int(z-29),int(z+7),3):s.box('Heel shallow grip rib','stock',(b+1.5,0,zz),(.42,18,.9),s.polymer,.15)
 for sign in [-1,1]:
  s.box('Cheek broad shallow inset','stock',((a+b)/2+6,sign*9.4,z),(max(5,b-a-28),.45,5),s.polymer,.5)
  s.screw('Stock decorative pivot','stock',b-9,z-5,sign*7.45,1.1)

def open_stock(s,a,b,z=23,thin=False):
 d=11 if thin else 19
 s.box('Stock attached shoulder block','stock',(a+3,0,z),(9,d+1,18),s.metal,.75)
 pts=[(a+5,z+8),(a+24,z+4),(b-2,z+4),(b,z),(b,z-36),(b-5,z-36),(a+25,z-10),(a+6,z-8)]
 o=s.poly('Solid open stock outline','stock',pts,d,s.polymer,.9)
 hole=[(a+31,z-2),(b-8,z-2),(b-8,z-26),(a+35,z-9)]
 s.cut(o,s.poly('Stock silhouette void cutter','stock',hole,32,s.dark,.55))
 s.box('Stock closed rubber heel','stock',(b,0,z-16),(3,d+2,42),s.rubber,.7)
 for sign in [-1,1]:s.screw('Stock shoulder inset pivot','stock',a+6,z,sign*d/2,1.2)
 for zz in range(int(z-32),int(z+2),3):s.box('Stock heel tread','stock',(b+1.5,0,zz),(.4,d,.8),s.polymer,.12)

def ventguard(s,a,b,z=23,depth=20,height=19,kind='mlok',mat=None):
 mat=mat or s.metal
 s.poly('Closed faceted guard envelope','handguard',[(a,z+height/2),(b,z+height/2),(b+2,z-height/2),(a+4,z-height/2),(a,z-height/2+4)],depth,mat,.8)
 for sign in [-1,1]:
  for x in range(int(a+6),int(b-3),14):
   if kind=='round':s.cyl('Blind round guard recess','handguard',(x,sign*(depth/2-.07),z+4),1.6,.45,s.dark,'Y',.12,32)
   else:s.box('Closed long guard recess','handguard',(x,sign*(depth/2-.03),z+1),(8,.45,2.5),s.dark,.5)
  s.box('Guard lower bevel seam','handguard',((a+b)/2,sign*depth/2,z-height/2+3),(b-a-9,.4,.8),s.edge,.18)
  for x in [a+3,b-3]:s.screw('Guard closed stud','handguard',x,z-3,sign*(depth/2-.1),.85)
 if kind=='quad':
  for sign in [-1,1]:
   s.box('Side decorative nonstandard ridge rail','handguard',((a+b)/2,sign*(depth/2+.4),z),(b-a-9,1.2,5),mat,.3)
   for x in range(int(a+5),int(b-3),4):s.box('Side rail transverse ornament','handguard',(x,sign*(depth/2+.8),z),(1.8,1.5,6),mat,.2)
 for x in range(int(a+5),int(b-3),5):s.box('Guard lower attached ridges','handguard',(x,0,z-height/2-.4),(2.8,8,1.5),mat,.18)

def finish(s,description):
 approx=[description,'2026-09-22 实际查看游戏外观参考；轮廓独立重建，宽度、遮蔽面与细小纹理为艺术推断。','微缩实心外观雕塑；封闭前端，无膛室、内部机构、通孔或真实安装接口。网页分组仅作外观拆装。','可选光学装饰默认隐藏，只供数字展示；没有提取游戏网格或贴图。发布者声明可按 CC BY-NC 4.0 非商业再分发。']
 sources=[REFS[s.asset], 'https://gamewith.jp/deltaforce/556174' if s.asset=='ar57' else 'https://gamewith.jp/deltaforce/542359' if s.asset=='mcxlt' else 'https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops']
 result=s.finish(sources,approx)
 (s.out/'SOURCE_NOTES.md').write_text('# '+s.asset.upper()+' 外观参考记录\n\n'+''.join('- '+x+'\n' for x in sources)+'\n'+''.join('- '+x+'\n' for x in approx)+'\n尺寸是桌面艺术模型尺寸。基础外观融合后分平面胶合，不代表真实装配方式。未实机打印。\n')
 bpy.ops.wm.open_mainfile(filepath=str(s.out/'source'/f'{s.asset}.blend'))
 for o in bpy.context.scene.objects:
  if o.type=='EMPTY' and o.name.startswith('part_'):
   for c in o.children_recursive:c.hide_render=False
 bpy.context.scene.render.filepath=str(s.out/'renders'/'optional.png');bpy.ops.render.render(write_still=True)
 return result
