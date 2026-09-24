"""Independent exterior art builders for remaining long models.
Arbitrary miniature proportions, sealed solids, no functional internal geometry.
"""
import bpy, math, sys, json
from pathlib import Path
from model_helpers_amg import Sculpture
from batch4_long_helpers import scope,grain,finish as base_finish
REFS={
'm250':'https://deltaforcewiki.vasdgame.com/playerhub/40001/object/18040000003.png',
'qjb201':'https://www.imfdb.org/images/thumb/8/88/DFHO_QJB205.jpg/600px-DFHO_QJB205.jpg',
'mini14':'https://www.imfdb.org/images/thumb/6/68/DFHO_Mini14.jpg/600px-DFHO_Mini14.jpg',
'psg1':'https://www.imfdb.org/images/thumb/c/c8/DFHO_HK_PSG1.jpg/600px-DFHO_HK_PSG1.jpg',
'sr25':'https://www.imfdb.org/images/thumb/9/97/DFHO_SR25.jpg/600px-DFHO_SR25.jpg',
'sr9':'https://www.imfdb.org/images/thumb/c/c1/DFHO_HK_SR9.jpg/600px-DFHO_HK_SR9.jpg',
'svch':'https://community-hs.233leyuan.com/community/post/d2484bf9990d48c8948351fa26a0938b_866113239.webp',
'vss':'https://www.imfdb.org/images/thumb/a/ac/DFHO_VSS.jpg/600px-DFHO_VSS.jpg',
'marlin':'https://www.imfdb.org/images/thumb/9/9a/DFHO_Marlin.jpg/600px-DFHO_Marlin.jpg',
'm82':'https://pbs.twimg.com/media/HGfyFskaEAAnfVB.jpg',
'r93':'https://www.imfdb.org/images/thumb/2/21/DFHO_BlaserR93.jpg/600px-DFHO_BlaserR93.jpg'}
NOTES={
'm250':'沙色长护木、横向封闭装饰带、织物方盒、镂空尾托和折叠双杆。',
'qjb201':'黑色阶梯式机身、棱面护木、绿色软盒、细长前杆和三角框托。',
'mini14':'棕木连体前床及整托、短直底匣、顶部散热浅槽及细长前杆。',
'psg1':'参考游戏标名 PSG-1，黑色长楔形护木、棕色掌托握把、方形贴腮尾托；默认无镜。',
'sr25':'长矩形护木、固定黑色整托、短直匣与前后机械瞄具。',
'sr9':'暗绿色长圆护木与拇指孔整托、短直匣和黑色上机身。',
'svch':'根据游戏宣传图重建纹理前杆、前握框、骨架握把和骨架托；参考为宣传配置，裸枪默认状态未确认。',
'vss':'木色双镂空整托、短竖纹护木、粗圆封闭前端与短斜匣。',
'marlin':'黑色弯颈整托、双前杆、大下置杠杆环与小护圈。',
'm82':'依据官方日文宣传侧视图：长箱形上机身、封闭双室外观前块、底匣、折叠双杆及框形尾托；默认无镜。',
'r93':'黑色一体精密托、长细前杆、矮底匣、折叠细杆及高贴腮尾托。'}

def new(asset,length):
 s=Sculpture(asset,length)
 for k,label in [('body','封闭主体'),('handguard','前床与护木'),('barrel','封闭前端'),('stock','尾托外观'),('grip','握持与护圈'),('magazine','实心下置装饰'),('details','固定表面细节'),('sights','顶轨与固定瞄具')]:s.part(k,label)
 s.part('optic','可选望远瞄具',False)
 s.wood=s.mat('Walnut brown',(.22,.076,.028),0,.53)
 s.woodlight=s.mat('Warm walnut grain',(.31,.135,.055),0,.6)
 s.green=s.mat('Dark olive furniture',(.08,.125,.106),.04,.62)
 s.tan=s.mat('Warm sand alloy',(.31,.248,.155),.55,.48)
 s.fabric=s.mat('Olive canvas',(.14,.143,.092),0,.95)
 s.scene['print_segment_breaks_x_mm']='[-5.31]'
 return s

def front(s,x0,x1,z=27,r=3):
 s.cyl('Sealed miniature front rod','barrel',((x0+x1)/2,0,z),r,x1-x0,s.metal,'X',.25)
 s.cyl('Closed end face','barrel',(x0-.04,0,z),r*.75,.12,s.dark,'X',.01)

def pins(s,key,xs,z,y=8):
 for sign in [-1,1]:
  for x in xs:s.screw('Sculpted fastening mark',key,x,z,sign*y,.75)

def panel(s,key,pts,depth=16,mat=None,b=.6):return s.poly('Layered exterior panel',key,pts,depth,mat or s.metal,b)

def guard(s,x,z=11,w=24):
 o=panel(s,'grip',[(x,z),(x+w,z),(x+w,z-16),(x+w-3,z-19),(x+3,z-19),(x,z-14)],6,s.metal,.8)
 s.cut(o,s.poly('Decorative guard silhouette opening','grip',[(x+3,z-2),(x+w-3,z-2),(x+w-3,z-13),(x+w-6,z-16),(x+5,z-16),(x+3,z-12)],16,s.dark,.5))
 panel(s,'grip',[(x+w*.53,z),(x+w*.65,z),(x+w*.62,z-8),(x+w*.43,z-12),(x+w*.38,z-10),(x+w*.52,z-6)],2.5,s.steel,.3)

def pistol_grip(s,x=45,z=11,mat=None,palm=False):
 panel(s,'grip',[(x,z),(x+14,z),(x+24,z-35),(x+7,z-39),(x+3,z-34)],14,mat or s.polymer,1.2)
 for sign in [-1,1]:
  for row in range(7):s.line('Grip shallow transverse texture','grip',(x+7+row*.4,sign*7,z-12-row*3),(x+16+row*.4,sign*7,z-12-row*3),.22,s.rubber)
 if palm:s.box('Broad fixed palm shelf','grip',(x+16,0,z-37),(26,22,6),s.polymer,1.1)
 guard(s,x-23,z)

def magazine(s,x=0,z=13,w=24,h=28,mat=None,curve=0):
 pts=[(x-w/2,z),(x+w/2,z),(x+w/2-curve*.2,z-h*.45),(x+w/2-curve,z-h),(x-w/2-curve,z-h),(x-w/2-curve*.4,z-h*.4)]
 panel(s,'magazine',pts,12,mat or s.polymer,.75)
 for sign in [-1,1]:
  for xx in [x-w*.27,x+w*.27]:
   s.line('Raised magazine seam','magazine',(xx,sign*6,z-3),(xx-curve,sign*6,z-h+3),.4,s.edge)
  for zz in [z-h*.3,z-h*.7]:s.box('Magazine horizontal relief','magazine',(x-curve*.45,sign*6,zz),(w*.88,.5,.65),s.metal,.12)
 s.box('Solid magazine bottom lip','magazine',(x-curve,0,z-h),(w+2,13,2.2),s.polymer,.5)

def box_receiver(s,a=-28,b=66,z=25,mat=None):
 panel(s,'body',[(a,z+10),(b-7,z+10),(b,z+6),(b,z-14),(a+12,z-14),(a,z-9)],18,mat or s.metal,1)
 for sign in [-1,1]:
  s.box('Upper stamped lengthwise line','details',((a+b)/2,sign*9.05,z+4),(b-a-9,.8,1.3),s.edge,.25)
  s.box('Closed side inset','details',(a+25,sign*9.15,z+1),(27,.7,5.1),s.dark,.6)
  s.box('Side shutter highlight','details',(a+24,sign*9.55,z+1),(23,.35,2.8),s.steel,.35)
  s.cyl('Fixed selector disc','details',(b-18,sign*9.3,z-7),2.4,.9,s.metal,'Y',.15)
  s.line('Fixed selector tab','details',(b-18,sign*9.75,z-7),(b-24,sign*9.75,z-8),.65,s.edge)
 pins(s,'details',[a+7,b-5],z-6,9.1)

def sights(s,a=-80,b=65,z=37,full=True):
 s.box('Fixed display saddle foot','sights',(b-20,0,z-2),(43,7,5),s.metal,.4)
 if full:s.box('Continuous shallow top spine','sights',((a+b)/2,0,z-1.3),(b-a,6.5,3),s.metal,.3)
 if full:s.rail('sights',a,b,z,7,4)
 else:s.rail('sights',b-34,b,z,7,4)
 for x in [a+3,b-5]:
  s.box('Fixed sight base','sights',(x,0,z+2),(5.5,8,4),s.metal,.5)
  s.box('Fixed sculptural sight blade','sights',(x,0,z+7),(2.8,3.5,8),s.metal,.45)
 scope(s,'optic',b-27,z+3,56)

def closed_stock(s,a,b,mat=None):
 panel(s,'stock',[(a,33),(b-3,33),(b,29),(b,-1),(b-4,-2),(a+8,14),(a,15)],20,mat or s.polymer,1.3)
 s.box('Rubber butt plate','stock',(b,0,15),(3,21,36),s.rubber,.8)
 for sign in [-1,1]:s.line('Stock diagonal molded line','stock',(a+14,sign*10,19),(b-8,sign*10,4),.25,s.edge)

def skeleton_stock(s,a,b,mat=None):
 s.cyl('Solid upper stock beam','stock',((a+b)/2,0,29),5.7,b-a,mat or s.metal,'X',.5)
 o=panel(s,'stock',[(a+12,29),(b-2,29),(b,25),(b,-8),(b-6,-9),(a+12,10)],17,mat or s.polymer,1)
 s.cut(o,s.poly('Exterior stock open shape','stock',[(a+20,17),(b-9,16),(b-8,1),(a+24,10)],30,s.dark,.7))
 s.box('Rubber butt plate','stock',(b,0,11),(3,19,43),s.rubber,.8)
 pins(s,'stock',[a+16,b-8],23,8.5)

def traditional(s,a=48,b=149,mat=None):
 panel(s,'stock',[(a,24),(a+12,22),(a+31,12),(a+45,17),(b-3,15),(b,11),(b,-20),(b-5,-22),(a+44,-4),(a+28,-7),(a+17,1),(a+5,11),(a,11)],20,mat or s.wood,1.8)
 s.box('Traditional black butt pad','stock',(b,0,-3),(2.8,21,37),s.rubber,.65)
 if mat is None:grain(s,'stock',a+65,b-7,-3,7,10,s.woodlight,s.wood)
 pins(s,'stock',[b-12],-13,10)

def folded_bipod(s,key,a,b,z=6):
 for sign in [-1,1]:
  s.line('Fixed folded display rod',key,(a,sign*7,z),(b,sign*11,z-6),1.9,s.metal)
  s.box('Folded rod foot',key,(b,sign*11,z-6),(9,6,4),s.polymer,.55)
  s.cyl('Solid folded pivot',key,(a,sign*7,z),3.8,4,s.metal,'Y',.35)
 s.box('Folded rod mounting sculpture',key,(a,0,z+3),(7,19,10),s.metal,.6)

def finalize(s,cutplane_mm=None):
 # Scale exterior art as a miniature without preserving any mechanical dimensions.
 factor=s.length/300
 for o in s.col.all_objects:
  if o.type=='MESH':
   o.location*=factor;o.scale*=factor
   s.active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 s.scene['print_segment_breaks_x_mm']=json.dumps([cutplane_mm if cutplane_mm is not None else -5.31*factor])
 return base_finish(s,REFS[s.asset],[NOTES[s.asset],'所有装饰面使用显式 PBR 色值；前端全部实心封闭。没有可用枪械零件或内部结构。'])
