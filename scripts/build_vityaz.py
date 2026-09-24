"""Vityaz/勇士: black short receiver, slim curved magazine, open triangular stock."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_compact_helpers import *
s=begin('vityaz',240,[('receiver','黑色短机匣与上盖'),('handguard','分层短聚合物护木'),('front','封闭细前杆'),('stock','三角骨架后托'),('grip','黑色斜向握把'),('magazine','细长弯曲实心弹匣'),('controls','固定侧控与护圈'),('sights','机械瞄具与短顶轨')])
s.poly('Short stamped-like receiver sculpture','receiver',[(-33,14),(-37,32),(-30,38),(33,38),(40,30),(40,13),(17,8),(-25,9)],18.8,s.metal,.65)
s.poly('Long rounded angular dust cover','receiver',[(-37,33),(-30,42),(29,42),(36,37),(38,30)],17.3,s.metal,.8)
for side in [-1,1]:
 s.box('Closed long upper side line','receiver',(-1,side*9.39,29),(61,.3,2.1),s.dark,.55)
 s.poly('Receiver side flat plate','receiver',[(-29,26),(34,27),(34,17),(21,12),(-24,13)],.4,s.metal,.35,y=side*9.42)
 s.box('Shallow front slant line','receiver',(-27,side*9.71,23),(1.3,.25,7),s.dark,.25)
 for x,z in [(-28,18),(-11,20),(18,18),(33,22)]:s.cyl('Small receiver rivet','receiver',(x,side*9.67,z),.85,.6,s.steel,'Y',.12)
h=s.poly('Lower compact ribbed handguard','handguard',[(-86,14),(-87,27),(-82,32),(-35,32),(-32,26),(-35,12),(-78,12)],19.8,s.polymer,.75)
s.poly('Upper compact handguard cap','handguard',[(-84,29),(-81,38),(-38,38),(-34,31)],16.5,s.polymer,.7)
for side in [-1,1]:
 s.box('Upper handguard shallow panel','handguard',(-59,side*8.25,34),(40,.6,4.9),s.metal,.7)
 for i in range(10):s.box('Lower handguard short rib','handguard',(-81+i*4.1,side*9.7,20),(1.7,.8,7.5),s.metal,.35)
 s.poly('Handguard lower lip','handguard',[(-82,15),(-36,15),(-36,13),(-78,13)],.5,s.metal,.3,y=side*9.5)
front(s,'front',-120,-83,25,2.6,3.3)
s.cyl('Decorative upper gas-like solid rod','front',(-80,0,34),2.7,25,s.metal,'X',.2)
s.box('Solid forearm front collar','front',(-86,0,27),(6.2,15,17),s.metal,.45)
s.poly('Front sight supporting upright','sights',[(-98,25),(-96,42),(-91,42),(-90,25)],4.7,s.metal,.35)
s.box('Front fixed sight crown','sights',(-94,0,42),(6,7.7,2.5),s.metal,.35)
s.poly('Slender curved magazine solid','magazine',[(-17,10),(1,9),(-1,-12),(-6,-33),(-16,-59),(-23,-63),(-37,-57),(-25,-33),(-20,-11)],10.4,s.polymer,.7)
for side in [-1,1]:
 s.poly('Magazine side relief','magazine',[(-15,5),(-2,4),(-6,-15),(-12,-36),(-22,-57),(-32,-55),(-22,-31)],.4,s.metal,.4,y=side*5.1)
 for j in range(4):
  z=-7-j*13;x=-12-max(0,-z-5)*.30
  s.box('Magazine shallow transverse line','magazine',(x+1.5,side*5.24,z),(9,.25,.6),s.dark,.14)
s.poly('Magazine sealed curved base','magazine',[(-35,-54),(-21,-59),(-21,-64),(-39,-58)],12,s.metal,.45)
grip(s,'grip',27,13,s.polymer,6.7,.88);guard(s,8,13,27,18)
s.box('Fixed rear hinge block','stock',(40,0,25),(9,16,20),s.metal,.6)
st=s.poly('Triangular metal rear stock silhouette','stock',[(43,30),(117,26),(119,-6),(109,-9),(42,14)],10.5,s.metal,.65)
s.cut(st,s.poly('Stock open triangular silhouette','stock',[(51,25),(111,21),(111,-1),(54,16)],25,s.dark,.5))
s.box('Stock narrow shoulder pad','stock',(118,0,9),(4,14,37),s.rubber,.6)
for side in [-1,1]:
 s.line('Stock upper highlight ridge','stock',(49,side*5.4,28),(111,side*5.4,24),.65,s.edge)
 s.cyl('Rear hinge decorative pivot','stock',(41,side*8.1,24),3.0,.7,s.steel,'Y',.25)
 s.poly('Fixed long selector paddle','controls',[(4,24),(26,22),(29,20),(28,17),(23,17),(4,22)],.8,s.steel,.3,y=side*9.75)
 s.box('Fixed side handle stem','controls',(-11,side*11.5,30),(7.7,4.4,2.7),s.metal,.45)
 s.box('Fixed side handle tip','controls',(-11,side*13.5,30),(4.0,2.1,4.2),s.polymer,.45)
s.rail('sights',-27,31,41.3,6.1,4)
s.box('Low rear sight plate','sights',(-30,0,39.5),(11,9,4),s.metal,.5)
s.box('Rear sight tiny blade','sights',(-32,0,42.5),(3,6,3),s.polymer,.3)
optic(s,5,44,.9)
result=finish(s,[REF,'https://www.imfdb.org/images/thumb/1/16/DFHO_Vityaz.jpg/600px-DFHO_Vityaz.jpg'],['按游戏默认双侧图重建黑色短护木、细长弧匣、短机匣、三角骨架尾托及上方机械瞄具。','短前杆和上方并行装饰杆均实心封闭，机匣盖和侧柄固定，不具机械活动功能。'],cut=-43)
