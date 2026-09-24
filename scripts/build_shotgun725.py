"""725 over-under, sealed miniature double-front art with walnut stock."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_compact_helpers import *
s=begin('shotgun725',330,[('receiver','银灰短机匣外壳'),('barrels','上下双实心长杆'),('forearm','木色短前护木'),('stock','弧颈木色整托'),('pad','黑色肩垫'),('controls','固定弧形护圈与装饰'),('details','木纹与机匣浅浮雕'),('sights','顶部细脊与低瞄点')])
wood=s.mat('Walnut warm brown',(.20,.095,.042),0,.52);grain=s.mat('Walnut grain highlight',(.265,.136,.065),0,.66);darkwood=s.mat('Walnut dark grain',(.10,.043,.019),0,.73)
s.box('Solid paired-rod breech block','receiver',(25,0,23),(43,17,16),s.steel,.9)
s.poly('Silver lower receiver sculpted edge','receiver',[(3,24),(45,24),(47,16),(42,11),(14,11),(6,14)],18,s.steel,.75)
for sign in [-1,1]:
 s.poly('Receiver silver side facet','receiver',[(6,27),(42,27),(45,21),(41,14),(13,14),(7,16)],.5,s.edge,.5,y=sign*9)
 s.box('Receiver blind upper seam','receiver',(25,sign*9.3,24),(29,.22,.8),s.dark,.25)
 for x in [12,35]:s.screw('Receiver small fixed fastener','receiver',x,18,sign*9.25,.68)
for z in [24,32.3]:
 s.cyl('Full length solid upper lower barrel sculpture','barrels',(-65,0,z),4.6,202,s.metal,'X',.3)
 s.cyl('Closed end opaque face','barrels',(-166.08,0,z),2.8,.16,s.dark,'X',.09)
 s.cyl('Short front terminal ring','barrels',(-164.8,0,z),4.75,2.2,s.metal,'X',.18)
s.box('Solid narrow join between parallel rods','barrels',(-64,0,28.2),(200,4.3,2.0),s.metal,.3)
s.poly('Long wooden forearm','forearm',[(-54,25),(-50,29),(6,29),(7,19),(2,13),(-47,13),(-53,17)],19.6,wood,1.3)
for sign in [-1,1]:
 s.poly('Forearm lower wood bevel','forearm',[(-48,16),(2,16),(5,20),(4,14),(-45,14)],.5,darkwood,.5,y=sign*9.7)
 for i in range(6):
  z=17+i*1.7
  s.line('Subtle forearm horizontal woodgrain','details',(-47,sign*9.92,z),(1,sign*9.92,z+.5*math.sin(i)),.20,grain)
s.poly('Traditional curved walnut stock','stock',[(41,30),(53,30),(65,25),(77,16),(89,12),(102,20),(163,14),(165,-24),(157,-26),(107,-9),(91,-3),(83,-8),(73,-7),(67,4),(56,13),(43,14)],20.8,wood,1.2)
for sign in [-1,1]:
 s.poly('Stock broad subtly raised cheek face','stock',[(107,15),(157,10),(158,-17),(112,-5),(96,0)],.48,wood,.85,y=sign*10.35)
 for i in range(7):
  x=110+i*6.0;z=9-i*.35
  s.line('Diagonal stock woodgrain upper','details',(x,sign*10.46,z),(x+8,sign*10.46,z-12),.24,grain)
 for i in range(5):
  x=62+i*3.2;z=18-i*2.2
  s.line('Curved stock neck small grain','details',(x,sign*10.4,z),(x+3,sign*10.4,z-5),.18,darkwood)
s.poly('Rubber shoulder endpad','pad',[(160,15),(165,14),(167,-24),(162,-26)],24,s.rubber,.9)
for sign in [-1,1]:
 for z in [-17,-7,3,12]:s.box('Pad subtle transverse texture','pad',(164.3,sign*12,z),(1.8,.25,1.1),s.polymer,.18)
guard(s,38,14,22,15,'controls',s.metal)
s.poly('Fixed top lever exterior','controls',[(37,31),(52,30),(55,28),(53,26),(38,29)],4.8,s.metal,.5)
s.box('Receiver top joining ridge','sights',(24,0,32),(41,4.3,3),s.metal,.4)
s.box('Long low barrel top rib','sights',(-64,0,36.7),(199,3.8,1.3),s.metal,.25)
s.box('Tiny front sight bead base','sights',(-158,0,37.8),(4.4,3.8,1.6),s.metal,.35)
s.cyl('Solid bright front bead','sights',(-158,0,39),.75,1.1,s.steel,'Z',.15)
optic(s,23,37.7,.76)
result=finish(s,[REF,'https://www.imfdb.org/images/thumb/2/2e/DFHO_725.jpg/600px-DFHO_725.jpg'],['按默认双侧图保留极长上下双杆、银灰短机匣、传统木色短护木与弯颈整托。','木纹采用明确PBR颜色与少量几何浅线，不依赖无法导出的程序纹理；双前端均为实心封闭。'],cut=-12)
