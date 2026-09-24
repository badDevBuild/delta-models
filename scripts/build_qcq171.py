"""QCQ171 exterior miniature with shallow silver twin stock rails."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_compact_helpers import *
s=begin('qcq171',230,[('receiver','紧凑盒形机匣'),('handguard','短四面纹理护木'),('front','封闭短前杆'),('stock','银灰双杆与窄尾托'),('grip','黑色斜握把'),('magazine','长弧形实心弹匣'),('controls','固定护圈与侧按钮'),('sights','长顶部导轨与低瞄具')])
s.poly('Rectangular central upper shell','receiver',[(-54,18),(-56,36),(-51,41),(35,41),(40,37),(40,19),(24,11),(-9,11),(-17,17)],18.5,s.metal,.75)
s.poly('Compact lower shell','receiver',[(-49,22),(37,22),(36,13),(24,10),(17,4),(-16,4),(-21,12),(-46,13)],17.3,s.polymer,.65)
for side in [-1,1]:
 s.box('Closed side long slot','receiver',(-6,side*9.23,32),(59,.3,2.3),s.dark,.55)
 s.box('Closed side raised cover','receiver',(11,side*9.45,28),(29,.5,3.7),s.edge,.5)
 s.poly('Lower diagonal receiver panel','receiver',[(-16,19),(14,19),(18,15),(13,9),(-13,9)],.65,s.metal,.5,y=side*8.7)
screws(s,'receiver',[(-46,22),(34,21),(-12,15)],9.24,.82)
h=s.poly('Short square front handguard','handguard',[(-97,18),(-97,35),(-91,40),(-53,40),(-50,33),(-52,16),(-89,16)],20,s.polymer,.7)
for side in [-1,1]:
 s.box('Side miniature rail base','handguard',(-77,side*10,24),(33,1.1,8.1),s.metal,.3)
 for i in range(9):s.box('Side handguard rail ribs','handguard',(-92+i*3.7,side*10.7,24),(1.7,1.9,9.0),s.metal,.3)
 s.box('Upper handguard long recess','handguard',(-74,side*10.05,34),(25,.25,2.1),s.dark,.5)
 s.screw('Forearm retaining screw','handguard',-54,22,side*10,.82)
s.box('Bottom textured forearm spine','handguard',(-77,0,16),(36,11,3),s.polymer,.4)
front(s,'front',-115,-95,26.5,3.0,3.8)
for x in [-112,-109,-106]:s.cyl('Sealed front narrow ring','front',(x,0,26.5),3.55,.6,s.metal,'X',.1)
s.poly('Long curved solid magazine','magazine',[(-34,8),(-14,6),(-16,-16),(-20,-35),(-29,-65),(-42,-62),(-46,-57),(-37,-25)],12,s.polymer,.75)
for side in [-1,1]:
 s.poly('Magazine broad side panel','magazine',[(-32,3),(-17,2),(-21,-22),(-25,-38),(-34,-60),(-42,-57),(-33,-26)],.4,s.metal,.4,y=side*5.95)
 for j in range(5):
  z=-7-j*10;x=-26-max(0,-z-10)*.22
  s.box('Magazine horizontal shallow raised band','magazine',(x,side*6.28,z),(15,.5,.8),s.metal,.2)
s.poly('Magazine solid bottom lip','magazine',[(-44,-56),(-29,-61),(-31,-66),(-47,-61)],13.5,s.metal,.4)
grip(s,'grip',25,15,s.polymer,7.2,.89);guard(s,4,15,28,20)
s.box('Rear stock hinge collar','stock',(39,0,29),(8,17,19),s.polymer,.55)
for side in [-1,1]:
 s.box('Silver stock sliding display beam','stock',(72,side*7.6,29),(73,3.2,6.8),s.steel,.6)
 for x in [47,61,75,89,102]:s.box('Silver beam blind dark inset','stock',(x,side*9.24,29),(9.2,.25,2.3),s.dark,.6)
s.box('Rear stock top cuff','stock',(110,0,28),(13,24,16),s.polymer,.85)
s.poly('Narrow shoulder pad silhouette','stock',[(105,27),(116,27),(116,-3),(110,-6),(106,-4)],16,s.rubber,.7)
for side in [-1,1]:s.box('Rear cuff silver face','stock',(110,side*12,31),(10,.4,7),s.steel,.4)
for side in [-1,1]:
 s.cyl('Fixed selector pivot','controls',(27,side*9.5,20),1.9,.7,s.steel,'Y',.2)
 s.line('Fixed selector pointer','controls',(27,side*9.8,20),(22,side*9.8,17),.65,s.metal)
 s.cyl('Fixed side button','controls',(-8,side*9.9,23),2.2,1.0,s.metal,'Y',.2)
s.box('Continuous forearm top rail bedding','handguard',(-73,0,40.2),(50,6.8,2.0),s.metal,.22)
sights(s,-96,37,41.1,6.8);optic(s,-5,44,1)
result=finish(s,[REF,'https://www.imfdb.org/images/thumb/5/50/DFHO_QCQ171.jpg/600px-DFHO_QCQ171.jpg'],['默认双侧图保留短方护木侧肋、长弧形弹匣与银灰双杆窄尾托；镂空杆视觉以有底盲凹表达，实物小雕塑更易保持完整。'],cut=-58)
