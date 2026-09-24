"""AUG game reference: silver bullpup exterior, all surfaces solid and inert."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rifle_batch3_helpers import *
s=Sculpture('aug',280)
for key,label,show in [('chassis','银灰上壳体',True),('stock','后部牛犊枪托',True),('forebody','前部护木外观',True),('front','封闭长前端',True),('grip','大护圈与握把',True),('magazine','后置网格弹匣',True),('sights','固定机械瞄具',True),('optic','可选紧凑瞄具',False)]:s.part(key,label,show)
silver=s.mat('Brushed cool grey housing',(.29,.33,.35),.62,.43)
poly=s.mat('AUG graphite composite',(.055,.065,.07),.06,.71)
edge=s.mat('Molded silver edge',(.2,.23,.24),.35,.53)
# Long smooth silver spine, stepped at the front and with a large rear cheek panel.
s.poly('Full solid bullpup upper body','chassis',[(-83,28),(-42,33),(-26,28),(124,28),(137,20),(139,11),(131,6),(-81,6),(-86,12)],24,silver,1.5)
s.poly('Receiver underside forward ledge','chassis',[(-80,8),(15,8),(22,1),(-30,-1),(-65,1),(-81,4)],21,poly,.8)
s.poly('Raised center top rail platform','chassis',[(-77,31),(26,31),(31,29),(30,26),(-80,26)],15,s.metal,.7)
s.rail('chassis',-77,30,32.2,8,3.6)
for sign in [-1,1]:
    s.box('Rear long blind cheek inset','chassis',(91,sign*11.98,20),(74,.5,9.3),poly,1.9)
    s.box('Middle blind cheek inset','chassis',(33,sign*12.03,20),(34,.55,9.3),s.dark,1.5)
    s.box('Middle closed textured panel','chassis',(33,sign*12.32,20),(31,.45,7.6),s.rubber,1.1)
    for i in range(15):s.box('Cheek pad subtle stipple stripe','chassis',(19+i*2,sign*12.56,20),(.65,.2,4.7),poly,.13)
    s.poly('Front upper blind trapezoid','chassis',[(-80,25),(-54,25),(-59,20),(-80,20)],.5,s.dark,.6,y=sign*11.95)
    for x in [-71,-56,-41]:s.box('Upper forward shallow slit','chassis',(x,sign*12.12,29),(8,.35,2),s.dark,.5)
    s.poly('Closed side window raised border','chassis',[(-25,26),(-6,26),(-8,19),(-25,19)],.5,poly,.6,y=sign*12)
    s.poly('Closed side window dark face','chassis',[(-23,24),(-9,24),(-10,21),(-23,21)],.3,s.dark,.4,y=sign*12.27)
    for x,z in [(-82,10),(-30,11),(12,12),(53,9),(89,10),(128,9)]:s.screw('Chassis cosmetic countersunk pin','chassis',x,z,sign*12,.9)
    s.box('Abstract model plaque','chassis',(-7,sign*12.23,11),(21,.3,3.5),edge,.3)
    for i in range(8):s.box('Abstract plaque mark','chassis',(-15+i*2.2,sign*12.41,11),(.8,.15,1),poly,.05)
# Filled butt sweeps down behind the rear magazine.
s.poly('Bullpup fixed rear stock','stock',[(41,9),(135,10),(138,3),(125,-40),(116,-41),(108,-25),(93,-16),(67,-10),(42,-7)],22,poly,1.2)
side_plate(s,'Rear stock molded panel','stock',[(73,-9),(126,4),(124,-33),(116,-34),(108,-20),(96,-14)],10.92,s.rubber,.45,.7)
s.poly('Fixed rear rubber heel','stock',[(135,13),(140,10),(128,-42),(123,-43)],24,s.rubber,.7)
for sign in [-1,1]:
    for x,z in [(74,-4),(121,-7),(122,-23)]:s.screw('Stock side pin relief','stock',x,z,sign*11.05,.85)
    s.box('Stock blind sling recess','stock',(117,sign*11.02,-11),(7,.35,2),s.dark,.55)
# Distinct front is offset below the top spine; short side rail and long exposed rod.
s.poly('Front silver solid casing','forebody',[(-87,27),(-45,27),(-37,19),(-40,8),(-86,8)],25,silver,.8)
s.cyl('Closed front collar','forebody',(-85,0,17),6.4,8,silver,'X',.4)
s.cyl('Solid exposed long front','front',(-113,0,17),2.8,54,s.metal,'X',.18)
s.cyl('Closed front end disc','front',(-140,0,17),2.7,.2,s.dark,'X',.04)
s.cyl('Front white-grey shoulder','front',(-94,0,17),4.1,12,silver,'X',.35)
s.cyl('Lower exposed solid spine','forebody',(-65,0,10),3.3,44,s.metal,'X',.25)
for sign in [-1,1]:
    s.box('Front rail attached flat bed','forebody',(-62,sign*12.3,17),(30,1.2,6.4),s.metal,.4)
    for x in range(-75,-46,3):s.box('Front rail short rib','forebody',(x,sign*13.02,17),(1.7,1.4,7),edge,.25)
    s.screw('Front guard decorative fastening','forebody',-82,17,sign*12.7,1.2)
# Oversize open guard is characteristic in both game side views.
s.poly('Angled closed pistol grip','grip',[(-24,8),(-12,8),(-8,-3),(-6,-11),(8,-29),(6,-37),(-8,-40),(-20,-25),(-29,-7)],15.5,poly,.9)
guard=s.poly('Large fixed external hand guard','grip',[(-66,8),(-57,8),(-40,-14),(-29,-28),(-19,-35),(-7,-35),(3,-30),(9,-33),(7,-40),(-10,-43),(-25,-39),(-37,-30),(-51,-11)],7.2,silver,1)
s.cut(guard,s.poly('Large hand guard inner window','grip',[(-56,6),(-49,6),(-35,-14),(-24,-28),(-16,-32),(-8,-33),(-8,-36),(-21,-36),(-32,-28),(-45,-10)],25,s.dark,.8))
side_plate(s,'Grip raised sculptural side panel','grip',[(-20,-4),(-12,-4),(-11,-13),(2,-30),(-4,-34),(-13,-24)],7.65,edge,.5,.6)
for sign in [-1,1]:
    for z,x in [(-7,-20),(-13,-17),(-20,-12),(-28,-6)]:s.box('Grip broad inset texture','grip',(x,sign*7.95,z),(5,.45,2.3),poly,.4)
s.poly('Fixed trigger decoration','grip',[(-34,7),(-31,7),(-30,-2),(-34,-6),(-37,-5),(-33,-1)],2.7,s.metal,.3)
# Rear magazine slopes toward the forward side, with visible square waffle pattern.
s.poly('Rear inserted solid magazine','magazine',[(36,1),(67,-5),(64,-25),(58,-53),(26,-45),(31,-21)],14,poly,.7)
s.poly('Magazine closed heel plate','magazine',[(26,-43),(59,-51),(60,-55),(24,-47)],15,s.metal,.5)
side_plate(s,'Magazine broad square panel','magazine',[(36,-5),(64,-10),(60,-28),(56,-47),(29,-41),(33,-21)],6.9,s.rubber,.5,.4)
for sign in [-1,1]:
    for row in range(6):
        z=-12-row*5.7;shift=-row*.95
        s.line('Magazine transverse waffle ridge','magazine',(34+shift,sign*7.2,z),(62+shift,sign*7.2,z-6),.48,s.metal)
    for i in range(4):
        x=35+i*6.8
        s.line('Magazine longitudinal waffle ridge','magazine',(x,sign*7.2,-9-i*1.35),(x-7,sign*7.2,-44-i*1.35),.44,s.metal)
sight(s,'sights',-69,33,True);sight(s,'sights',22,33)
optic(s,-20,34)
s.scene['print_segment_breaks_x_mm']='[-50]'
result=finish(s,'实际游戏 AUG 双侧图显示银灰牛犊壳体、前部短侧轨、细长前端、后置方格弹匣、大型一体护圈与深色后托；未使用现实 AUG 常见圆筒瞄准镜作为默认配置。')
