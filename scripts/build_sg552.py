"""SG552: scalloped polymer forearm, narrow receiver and open triangular tail."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('sg552',300)
blue=s.mat('SG552 blue gray stamped metal',(.095,.11,.115),.58,.43)
poly=s.mat('SG552 satin molded polymer',(.06,.073,.078),.03,.65)
front(s,-149,-108,24,2.5,False)
s.cyl('Front fixed collar','front',(-111,0,24),4,5,blue,'X',.2)
ventguard(s,-109,-43,24,19,23,'round',poly)
for sign in [-1,1]:
 for x in range(-103,-48,4):
  for z in [17.5,19.2]:s.box('Forearm fine molded texture','handguard',(x,sign*9.55,z),(1,.38,.75),blue,.16)
 s.box('Forearm center parting seam','handguard',(-76,sign*9.5,21),(56,.35,.7),s.dark,.15)
receiver(s,[(-44,35),(49,35),(59,31),(61,18),(-43,18)],19,blue)
s.poly('Long folded lower receiver','lower',[(-43,21),(61,22),(62,10),(45,7),(15,7),(-39,10)],18,blue,.7)
for sign in [-1,1]:
 s.poly('Lower stamped shallow field','lower',[(-37,17),(-4,17),(-4,11),(-29,11)],.6,blue,.4,y=sign*8.95)
 s.cyl('Static selector small roundel','lower',(36,sign*9.2,15),2,1,s.metal,'Y',.2)
 s.poly('Static raised selector tab','lower',[(35,16),(32,10),(34,9),(38,14)],.7,s.metal,.2,y=sign*9.7)
 for x in [-38,-1,48]:s.screw('Lower receiver blind stud','lower',x,13,sign*8.9,.8)
magazine(s,[(-29,15),(-3,14),(-5,-28),(-11,-39),(-36,-34),(-32,-10)],14,'grid',s.polymer)
grip(s,36,7,'ridges',poly)
guard(s,'lower',[(-1,10),(39,10),(41,-9),(34,-15),(7,-15),(-1,-8)],[(4,6),(35,6),(36,-7),(31,-11),(10,-11),(4,-6)],6)
s.poly('Attached trigger flat ornament','lower',[(18,7),(21,7),(21,-4),(18,-7),(16,-6),(18,-2)],3,s.metal,.24)
open_stock(s,59,149,25)
s.rail('sights',-45,43,35.7,6,4)
s.box('Rear drum sight base','sights',(43,0,36),(12,10,3),blue,.45)
s.cyl('Rear closed sight drum','sights',(43,0,40),3.4,5,blue,'Z',.3)
s.poly('Front attached tall sight','sights',[(-114,26),(-114,44),(-111,49),(-107,49),(-105,26)],6,blue,.5)
s.cyl('Front circular opaque sight face','sights',(-110,0,43),3,4,blue,'X',.25)
s.cyl('Front blind circular dark mark','sights',(-112.1,0,43),1.45,.2,s.dark,'X',.05)
s.box('Front sight attached shoulder','sights',(-109,0,30),(8,10,10),blue,.5)
optic(s,8,37)
s.scene['print_segment_breaks_x_mm']='[-48]'
result=finish(s,'依据游戏默认双侧图重建圆点护木、折面机匣、短斜匣、横肋握把与宽三角镂空托。')
