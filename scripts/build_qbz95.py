"""QBZ95-1 bullpup silhouette reconstructed as a solid miniature art object."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch4_rifle_helpers import *
s=Sculpture('qbz95',270)
for key,label,show in [('receiver','无托式长机身',True),('handguard','斜纹短护木',True),('front','封闭前端与高前瞄具',True),('carry','高提把外观',True),('magazine','后置实心弯弹匣',True),('grip','前置握把与固定护圈',True),('stock','齐平后托外观',True),('controls','侧面固定装饰',True),('optic','可选提把瞄具',False)]:s.part(key,label,show)
body=s.mat('QBZ charcoal polymer',(.043,.052,.061),.09,.6)
upper=s.mat('QBZ dark blue alloy',(.076,.092,.106),.58,.41)
edge=s.mat('Molded grey edge highlights',(.076,.089,.101),.15,.56)
# Sealed front graphic cylinder and strong raised front tower.
s.cyl('Filled front extension','front',(-112,0,7),2.65,46,upper,'X',.16)
s.cyl('Flat closed front end','front',(-135,0,7),2.55,.16,s.dark,'X',.04)
s.cyl('Front collar wide base','front',(-89,0,7),5,4,upper,'X',.3)
s.cyl('Front sculpted second collar','front',(-94,0,7),3.4,6,upper,'X',.2)
s.poly('Raised front sight attached tower','front',[(-89,11),(-89,29),(-94,44),(-93,50),(-87,50),(-86,36),(-79,23),(-78,12)],7,upper,.6)
s.box('Front top blind notch','front',(-90,0,48),(4,7.4,2),s.dark,.25)
s.box('Front closed central post','front',(-90,0,50),(1.6,3,3),s.metal,.15)
s.screw('Front tower blind stud','front',-85,25,-3.5,.8)
# Rounded-profile short forearm with slanted molded grooves.
s.poly('Short solid front handguard','handguard',[(-88,19),(-31,19),(-25,13),(-29,-1),(-86,-1),(-90,5)],17.4,body,1.05)
s.box('Front handguard band','handguard',(-86,0,9),(4,18.5,20),upper,.55)
for sign in [-1,1]:
    for x in range(-80,-35,3):
        s.poly('Handguard diagonal shallow flute','handguard',[(x,1),(x+4.8,15),(x+5.6,15),(x+.8,1)],.4,edge,.22,y=sign*8.7)
    s.box('Handguard top joint seam','handguard',(-57,sign*8.6,18),(48,.4,.75),s.dark,.2)
for x in range(-79,-33,6):s.box('Top handguard blind vent','handguard',(x,0,19),(3.4,7,.3),s.dark,.45)
# Broad continuous solid bullpup envelope, subtly sloping below the rear magazine seat.
s.poly('Continuous filled bullpup body','receiver',[(-33,19),(27,23),(115,23),(131,25),(134,20),(134,-14),(119,-14),(113,-4),(52,-4),(38,-10),(22,-4),(-29,-4),(-35,1)],18,body,.9)
s.poly('Long upper metal spine','receiver',[(-30,20),(129,26),(134,22),(132,17),(-30,17)],17,upper,.7)
for sign in [-1,1]:
    s.box('Long receiver middle molded joint','receiver',(64,sign*8.95,10),(128,.45,.85),s.dark,.2)
    s.poly('Lower magazine seat angled relief','receiver',[(43,-8),(54,-1),(118,-1),(122,-7),(117,-8),(113,-3),(56,-3),(48,-10)],.5,edge,.25,y=sign*8.85)
    s.box('Upper rear shallow seam','receiver',(91,sign*8.95,18),(68,.35,.9),s.dark,.2)
# Stock cover has slightly wider cheek and heel surfaces, no separating functional assembly.
s.poly('Rear upper cheek cover','stock',[(38,21),(119,22),(132,25),(134,21),(134,15),(38,15)],19,body,.8)
s.box('Rear sealed rubber buttpad','stock',(133.8,0,5.5),(3.4,20,39),s.rubber,.95)
s.poly('Rear lower heel extension','stock',[(115,1),(131,1),(133,-14),(120,-14)],19,body,.75)
for sign in [-1,1]:
    s.box('Stock lower closed inset','stock',(124,sign*9.48,-7),(8,.3,4.5),s.dark,.65)
for z in range(-11,23,3):s.box('Rear buttpad subtle tread','stock',(135,0,z),(.45,19,.8),body,.18)
# Tall rounded rectangular carry-handle opening is the main identifying upper feature.
handle=s.poly('Tall solid carry handle frame','carry',[(-47,19),(-33,42),(-28,46),(34,46),(39,43),(44,20)],10,upper,.8)
s.cut(handle,s.poly('Carry handle display opening cutter','carry',[(-33,23),(-23,38),(-20,40),(28,40),(31,37),(32,23)],26,s.dark,.9))
s.box('Handle broad low attached rim','carry',(-2,0,21),(83,11.4,3),upper,.4)
s.box('Handle top long crest','carry',(2,0,45),(65,9.5,1.4),body,.45)
s.box('Handle rear fixed sight ornament','carry',(33,0,45),(6,11,3),upper,.45)
s.poly('Carry opening static inner ornament','carry',[(-13,21),(-12,28),(-8,30),(-7,26),(-8,21)],3,upper,.3)
s.cyl('Carry inner blind circle','carry',(-10,-1.7,26),.85,.3,s.edge,'Y',.05)
# Fore grip is ahead of the magazine and angled toward the rear.
s.poly('Front-positioned grip solid','grip',[(-4,-2),(10,-2),(10,-14),(26,-43),(10,-49),(-3,-23),(-8,-10)],15,body,1.1)
side_plate(s,'Grip dark inset field','grip',[(-1,-13),(8,-13),(20,-40),(12,-43),(1,-23)],7.55,s.rubber,.4,.65)
for sign in [-1,1]:
    for row in range(12):s.box('Grip horizontal molded ribs','grip',(3+row*.86,sign*7.8,-18-row*1.8),(8,.5,.8),edge,.22)
s.poly('Grip closed base lip','grip',[(9,-48),(26,-44),(28,-46),(10,-51)],16,body,.4)
guard(s,'grip',[(-39,-2),(-5,-2),(-4,-15),(-9,-22),(-32,-22),(-39,-15)],[(-34,-6),(-10,-6),(-9,-14),(-13,-18),(-29,-18),(-34,-13)],7)
s.poly('Guard static trigger ornament','grip',[(-22,-3),(-18,-3),(-18,-12),(-23,-16),(-25,-14),(-22,-10)],3,s.metal,.3)
# Posterior swept solid magazine, long vertical ribs and horizontal panel steps.
s.poly('Rear curved magazine closed form','magazine',[(61,-2),(88,-2),(85,-22),(75,-45),(57,-70),(37,-55),(50,-35),(57,-16)],13,body,.85)
side_plate(s,'Magazine broad side molded field','magazine',[(63,-7),(84,-7),(81,-24),(71,-44),(56,-65),(41,-54),(53,-34),(60,-16)],6.4,edge,.4,.45)
for sign in [-1,1]:
    for shift in [0,8,16]:
        s.poly('Magazine curved raised spine','magazine',[(63+shift,-6),(61+shift,-20),(54+shift,-39),(41+shift,-55),(42.5+shift,-56),(55.5+shift,-40),(62.5+shift,-20),(64.5+shift,-6)],.48,body,.22,y=sign*6.62)
    for z,x in [(-17,59),(-34,53),(-49,43)]:
        s.poly('Magazine transverse molded step','magazine',[(x,z),(x+24,z-3),(x+23,z-5),(x-1,z-2)],.42,body,.2,y=sign*6.6)
s.poly('Magazine solid curved heel','magazine',[(36,-55),(56,-71),(59,-68),(39,-52)],14,body,.5)
# Fixed decorative pads, rivets and a blind side opening; never moving internals.
for sign in [-1,1]:
    for x,z in [(4,-2),(36,-4),(125,-2),(82,-1),(-30,7)]:s.screw('Body blind stud','controls',x,z,sign*8.92,.82)
    s.cyl('Large lower blind pivot','controls',(37,sign*9.1,-4),3.2,.55,s.dark,'Y',.13)
    s.cyl('Large pivot closed center','controls',(37,sign*9.42,-4),2.5,.45,s.edge,'Y',.16)
    s.box('Small blank lower label','controls',(67,sign*9.16,-.5),(22,.38,4),body,.35)
s.box('Blind rectangular rear side recess','controls',(62,9.05,14),(24,.5,7),s.dark,.6)
s.box('Filled rear side inset','controls',(62,9.35,14),(21,.4,4.5),s.steel,.45)
s.poly('Fixed magazine release relief','controls',[(90,-3),(97,-3),(96,-9),(91,-8)],5,upper,.5)
optic(s,1,47)
s.scene['print_segment_breaks_x_mm']='[29.5]'
result=finish(s,'依据游戏默认图重建高提把、独立前握把、后置弯弹匣、斜纹短护木、齐平后托与高前瞄具，保留无托式特征。')
