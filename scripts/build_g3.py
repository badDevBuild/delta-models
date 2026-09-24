"""G3 game-default exterior: slender forearm, tall straight magazine, fixed stock."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch4_rifle_helpers import *
s=Sculpture('g3',340)
for key,label,show in [('receiver','长折面机匣外观',True),('upper','上部细长金属脊',True),('handguard','窄长护木',True),('front','封闭细长前端',True),('magazine','直板实心弹匣',True),('grip','握把与固定护圈',True),('stock','固定聚合物枪托',True),('sights','固定鼓形与前瞄具',True),('optic','可选紧凑瞄具',False)]:s.part(key,label,show)
body=s.mat('G3 blue-grey metal',(.094,.109,.119),.66,.41)
fore=s.mat('Long dark grey forearm',(.105,.119,.118),.15,.64)
poly=s.mat('G3 graphite polymer',(.032,.039,.043),.05,.72)
magmat=s.mat('Pressed charcoal magazine',(.055,.064,.069),.52,.46)
s.cyl('Sealed long front extension','front',(-148,0,22),2.45,44,body,'X',.18)
s.cyl('Filled front face','front',(-170,0,22),2.37,.18,s.dark,'X',.03)
s.cyl('Front end broad collar','front',(-131,0,22),3.7,6,s.metal,'X',.25)
s.box('Fixed front sight attached root','front',(-128,0,28),(10,9,12),body,.65)
# Slender lower guard, angled bevels separate it from the exposed upper spine.
s.poly('Long slender solid forearm','handguard',[(-129,27),(-24,27),(-23,12),(-117,13),(-130,17)],15,fore,.8)
s.box('Forearm rear broad band','handguard',(-25,0,20),(4.5,18,17),body,.55)
s.box('Forearm front end band','handguard',(-128,0,21),(3,15.5,13),body,.5)
for sign in [-1,1]:
    s.box('Forearm lower recessed line','handguard',(-75,sign*7.45,16),(93,.4,1),poly,.25)
    for x in [-119,-108,-97,-53,-42,-32]:
        s.box('Closed rectangular forearm vent','handguard',(x,sign*7.45,24),(6.5,.5,2.2),s.dark,.45)
    s.box('Forearm side long molded channel','handguard',(-77,sign*7.49,21),(96,.4,1),s.edge,.22)
    s.screw('Forearm front retaining relief','handguard',-125,19,sign*7.5,.65)
# Upper uninterrupted narrow pipe and stamped receiver crest.
s.cyl('Solid upper long graphic spine','upper',(-53,0,31),3,156,body,'X',.3)
s.poly('Rounded upper receiver envelope','upper',[(-29,32),(-23,36),(74,36),(84,32),(86,25),(-28,25)],17,body,.8)
s.box('Receiver long central flat crest','upper',(28,0,35.8),(99,8,1.2),s.edge,.3)
s.poly('Solid pressed lower envelope','receiver',[(-27,27),(83,27),(95,19),(95,10),(74,7),(58,1),(28,1),(5,4),(-25,10)],16,body,.65)
for sign in [-1,1]:
    s.box('Upper seam folded relief','upper',(22,sign*8.45,29),(96,.55,1.4),s.edge,.2)
    s.box('Receiver shallow long shadow','receiver',(28,sign*8,22),(94,.4,1.2),s.dark,.22)
    s.poly('Receiver pressed side gusset','receiver',[(-27,20),(-2,10),(13,12),(17,16),(2,12),(-26,24)],.6,s.edge,.3,y=sign*8)
    for x,z in [(-21,14),(31,9),(75,17),(88,16)]:s.screw('Receiver blind pin','receiver',x,z,sign*7.98,.74)
    s.box('Rear pressed relief panel','receiver',(76,sign*8.14,12),(16,.35,4.5),body,.25)
s.box('Long blind right side window','upper',(27,8.5,28),(30,.55,7),s.dark,.6)
s.box('Window filled metallic insert','upper',(27,8.81,28),(25,.42,4.5),s.steel,.45)
s.box('Fixed front handle root','upper',(-103,-4.2,32),(5,7,3.5),body,.5)
s.cyl('Fixed front handle rounded ornament','upper',(-103,-8.2,32),2.2,4,poly,'Y',.25)
# Deep, nearly straight pressed magazine with perimeter bead and stamped squares.
s.poly('Straight tall magazine solid','magazine',[(-16,12),(13,8),(14,-41),(9,-44),(-17,-41)],13,magmat,.7)
side_plate(s,'Magazine recessed broad field','magazine',[(-13,2),(10,0),(10,-38),(-13,-36)],6.45,body,.4,.4)
for sign in [-1,1]:
    for x in [-10,-1,8]:s.box('Magazine raised longitudinal rib','magazine',(x,sign*6.7,-19),(1.3,.65,36),s.metal,.25)
    for z in [-5,-14,-23,-32]:
        for x in [-7,3]:s.box('Magazine pressed short dash','magazine',(x,sign*6.69,z),(5,.45,1),s.edge,.22)
s.poly('Magazine closed broad heel','magazine',[(-18,-41),(11,-45),(15,-42),(14,-40),(-18,-38)],14,s.metal,.5)
# Separate static grip housing and guard silhouette, no usable mechanism.
s.poly('Grip housing filled rear body','grip',[(20,15),(73,15),(72,3),(54,-4),(36,-4),(21,1)],15.5,poly,.65)
s.poly('Angled grip solid','grip',[(54,4),(67,3),(69,-11),(80,-32),(65,-40),(54,-20),(47,-8)],14,poly,1)
side_plate(s,'Grip shallow inset panel','grip',[(58,-8),(64,-9),(73,-29),(66,-33),(58,-19)],6.88,s.rubber,.35,.7)
for sign in [-1,1]:
    for row in range(10):s.box('Grip fine parallel texture','grip',(60+row*.7,sign*7.06,-12-row*1.7),(5,.3,.7),fore,.15)
    s.cyl('Grip housing blind selector pivot','grip',(47,sign*8.1,10),2.5,.9,s.edge,'Y',.17)
    s.poly('Fixed selector side relief','grip',[(45,11),(43,6),(45,5),(49,10)],.5,body,.25,y=sign*8.6)
guard(s,'grip',[(15,3),(52,2),(52,-12),(45,-17),(25,-17),(17,-11)],[(20,0),(48,-1),(47,-10),(43,-13),(27,-13),(22,-9)])
s.poly('Static trigger ornament','grip',[(35,0),(38,0),(38,-8),(34,-11),(32,-10),(35,-6)],2.8,s.metal,.25)
# Raised stock neck and low sloping buttplate are characteristic in side view.
s.poly('Stock metal shoulder solid','stock',[(78,35),(87,34),(103,23),(108,22),(108,10),(93,9),(80,20)],18,body,.9)
s.poly('Fixed broad polymer stock','stock',[(103,24),(168,24),(170,20),(170,-16),(162,-15),(127,-2),(104,10)],21,poly,1.05)
s.box('Stock sealed rubber heel','stock',(169,0,4),(3,22,39),s.rubber,.8)
side_plate(s,'Stock broad quiet side field','stock',[(113,19),(163,19),(163,-10),(132,1),(115,10)],10.3,poly,.35,.7)
for sign in [-1,1]:
    for z in [15,-8]:s.screw('Stock side inset stud','stock',160,z,sign*10.49,.85)
    s.box('Stock blind side sling recess','stock',(145,sign*10.5,9),(10,.55,7),s.dark,.7)
    for x in [142,147]:s.box('Stock sling recess solid crossbar','stock',(x,sign*10.8,9),(1.2,.6,7),body,.2)
for z in range(-12,23,3):s.box('Rubber stock heel ridges','stock',(170.5,0,z),(.4,21.5,.8),poly,.18)
# Low rear drum and protected front post as closed forms.
s.box('Rear sight foot','sights',(71,0,36),(10,9,2.3),body,.45)
s.cyl('Rear opaque sight drum','sights',(72,0,39),3.1,4,body,'Z',.3)
s.cyl('Rear sight blind mark','sights',(70.3,-2.1,39),.85,.35,s.dark,'Y',.07)
s.poly('Front sight raised tower','sights',[(-132,30),(-130,42),(-126,44),(-122,41),(-121,29)],6,body,.55)
s.cyl('Front sight filled ring graphic','sights',(-127,0,41),2.6,3,body,'X',.2)
s.cyl('Front sight blind circle','sights',(-128.6,0,41),1.1,.2,s.dark,'X',.04)
optic(s,26,36.8)
s.scene['print_segment_breaks_x_mm']='[-28]'
result=finish(s,'依据游戏默认图重建细长窄护木、外露上脊、折面机匣、直板压纹弹匣、聚合物斜握把与固定后托。')
