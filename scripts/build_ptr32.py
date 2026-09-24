"""PTR-32 exterior: walnut slim forearm, long curved fluted magazine, fixed stock."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('ptr32',300)
wood=s.mat('Warm brown varnished walnut',(.185,.072,.028),.08,.45)
grain=s.mat('Fine walnut grain relief',(.09,.035,.014),.03,.61)
body=s.mat('PTR stamped charcoal steel',(.07,.084,.09),.7,.4)
front(s,-149,-117,23,2.15,False)
s.poly('Narrow walnut forearm filled body','handguard',[(-117,29),(-40,29),(-40,17),(-112,17),(-119,21)],16,wood,.95)
for sign in [-1,1]:
 for x in [-111,-104,-97,-61,-54,-47]:s.cyl('Blind upper wood vent','handguard',(x,sign*7.96,25.5),1.2,.5,s.dark,'Y',.12,32)
 for row in range(7):s.poly('Fine long wood grain','handguard',[(-109,19+row*.85),(-47,20+row*.8),(-47,20.17+row*.8),(-109,19.18+row*.85)],.25,grain,.06,y=sign*8)
for x in [-117,-41]:s.box('Forearm dark end collar','handguard',(x,0,23),(3.5,17,14),body,.5)
s.cyl('Solid thin upper exposed spine','receiver',(-55,0,33),2.7,133,body,'X',.25)
receiver(s,[(-42,32),(-32,37),(58,37),(69,32),(72,24),(-42,24)],17,body)
s.poly('Stamped lower receiver silhouette','lower',[(-41,27),(69,27),(76,20),(76,11),(48,9),(29,3),(6,6),(-39,13)],16,body,.7)
for sign in [-1,1]:
 s.poly('Stamped receiver cheek ridge','lower',[(-39,19),(-14,10),(1,10),(6,14),(-11,13),(-39,23)],.6,s.edge,.35,y=sign*7.95)
 s.cyl('Static lower selector ornament','lower',(35,sign*8.1,18),2.3,1,s.edge,'Y',.2)
 for x in [-34,18,63]:s.screw('Blind receiver pin detail','lower',x,16,sign*7.9,.75)
 s.box('Upper folded side long rim','receiver',(11,sign*8.4,30),(93,.5,1.2),s.edge,.2)
magazine(s,[(-28,14),(-2,10),(-7,-10),(-18,-33),(-35,-57),(-59,-44),(-42,-21),(-32,-2)],13,'ribs',body)
for sign in [-1,1]:
 for off in [0,7,14]:
  s.poly('Magazine continuous curved pressed flute','magazine',[(-25+off,1),(-31+off,-19),(-47+off,-42),(-49+off,-43),(-33+off,-19),(-27+off,1)],.48,s.dark,.22,y=sign*6.65)
grip(s,35,6)
guard(s,'lower',[(-1,8),(39,8),(39,-10),(33,-17),(9,-17),(1,-10)],[(5,4),(35,4),(35,-8),(30,-13),(11,-13),(6,-8)],6)
s.poly('Attached curved trigger ornament','lower',[(20,5),(23,5),(23,-5),(20,-9),(18,-8),(20,-3)],3,body,.25)
s.poly('Fixed rear metal stock neck','stock',[(60,36),(69,34),(84,24),(88,24),(88,10),(70,10),(61,19)],18,body,.8)
s.poly('Broad fixed polymer stock','stock',[(83,27),(148,27),(149,23),(149,-17),(142,-17),(108,-4),(83,10)],21,s.polymer,1.1)
s.box('Stock closed heel','stock',(148.5,0,5),(3,22,43),s.rubber,.7)
for sign in [-1,1]:
 s.box('Blind stock sling inset','stock',(125,sign*10.4,12),(12,.5,9),s.dark,.6)
 s.box('Stock sling solid crossrib','stock',(126,sign*10.65,12),(2,.7,8.5),body,.3)
 for z in [20,-9]:s.screw('Stock inset stud','stock',141,z,sign*10.45,.9)
s.box('Rear sight attached base','sights',(56,0,38),(11,10,3),body,.5)
s.cyl('Opaque rear drum sight','sights',(56,0,41),3.2,4,body,'Z',.3)
s.box('Front sight attached foot','sights',(-118,0,30),(8,9,11),body,.5)
s.poly('Front fixed sight pedestal','sights',[(-122,30),(-121,41),(-119,45),(-114,44),(-113,30)],6,body,.5)
s.cyl('Front closed sight ring','sights',(-118,0,41),2.8,3.6,body,'X',.2)
s.cyl('Front blind inset mark','sights',(-119.9,0,41),1.2,.2,s.dark,'X',.03)
s.box('Fixed front handle root','receiver',(-95,-4,33),(6,7,3),body,.4)
s.cyl('Fixed front handle knob','receiver',(-95,-8,33),1.8,4,s.polymer,'Y',.2)
optic(s,15,38)
s.scene['print_segment_breaks_x_mm']='[0]'
result=finish(s,'依据游戏默认双侧图重建棕木细护木、窄上脊、明显弯曲的长压纹弹匣、斜握把与黑色固定后托。')
