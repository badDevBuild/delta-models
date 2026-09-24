"""Long ribbed handguard, carry handle and short magazine from game defaults."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch4_rifle_helpers import *
s=Sculpture('m16a4',330)
for key,label,show in [('upper','长上机匣外观',True),('lower','下机匣与固定护圈',True),('handguard','分节圆柱长护木',True),('front','封闭长前端',True),('magazine','短直实心弹匣',True),('grip','斜握把外观',True),('stock','固定长枪托',True),('sights','提把与三角前瞄具',True),('optic','可选顶部瞄具',False)]:s.part(key,label,show)
body=s.mat('Anodized blue black alloy',(.083,.098,.104),.65,.43)
poly=s.mat('Dark satin polymer',(.041,.048,.052),.05,.66)
ring=s.mat('Polymer rib highlight',(.055,.063,.068),.08,.57)
# Filled narrow front extension and sculptural collars.
s.cyl('Sealed front cylinder','front',(-143,0,21),2.5,44,body,'X',.15)
s.cyl('Closed flat front face','front',(-165,0,21),2.43,.18,s.dark,'X',.04)
s.cyl('Front shoulder collar','front',(-121,0,21),4.1,7,body,'X',.24)
# Long, round, subtly tapered-looking polymer guard made from closed forms.
s.cyl('Long filled handguard body','handguard',(-64,0,21),9.3,114,poly,'X',.75,64)
s.cyl('Front handguard collar','handguard',(-120,0,21),9.7,3,body,'X',.35,64)
s.cyl('Rear handguard shoulder','handguard',(-7,0,21),10.3,5,body,'X',.45,64)
for x in range(-115,-10,6):
    s.cyl('Handguard molded circular segment','handguard',(x,0,21),9.67,1.45,ring,'X',.27,48)
for sign in [-1,1]:
    s.box('Handguard long mold joint','handguard',(-65,sign*9.12,21),(103,.5,.65),s.dark,.15)
    for x in range(-112,-14,9):
        s.box('Handguard blind upper vent','handguard',(x,sign*4.9,28.5),(4.4,1.8,.35),s.dark,.35)
        s.box('Handguard shallow lower notch','handguard',(x,sign*4.5,13),(3.6,1.7,.4),s.dark,.3)
# Solid upper with barrel-shaped crest and lower polygon folds.
s.poly('Closed upper receiver core','upper',[(-7,31),(52,31),(65,23),(66,12),(-5,12)],17,body,.7)
s.box('Upper narrow shoulder strip','upper',(25,0,30.3),(65,10,3),body,.6)
s.poly('Filled lower receiver silhouette','lower',[(-5,17),(58,16),(63,10),(48,2),(27,1),(17,-4),(-4,-2)],16,body,.65)
s.poly('Magazine well front slope','lower',[(-4,12),(20,9),(20,-2),(-3,-4)],18,body,.5)
for sign in [-1,1]:
    s.box('Upper parting line','upper',(26,sign*8.5,17),(64,.45,1.1),s.dark,.2)
    s.poly('Lower flared magazine rim','lower',[(-4,-2),(18,-.5),(19,-3),(-4,-5)],.6,s.edge,.3,y=sign*8.9)
    for x,z in [(0,10),(34,11),(54,14),(4,23)]:s.screw('Receiver flush detail','lower',x,z,sign*8.4,.73)
    s.box('Abstract blank receiver stamp','lower',(22,sign*8.65,8),(8,.3,3.4),body,.2)
s.box('Blind ejection side recess','upper',(21,8.52,23),(24,.45,7),s.dark,.45)
s.box('Static closed cover inset','upper',(21,8.83,22.5),(22,.42,5.5),body,.45)
s.box('Cover lower hinge-like relief','upper',(21,9.05,19.7),(23,.7,1),s.edge,.2)
s.poly('Side deflector solid relief','upper',[(37,27),(43,25),(45,20),(40,19)],3,body,.6,y=8.1)
s.cyl('Rear knob base','upper',(53,9.2,25),2.3,4,body,'Y',.25)
s.cyl('Rear knob cap','upper',(53,11.3,25),2.8,1.5,s.polymer,'Y',.25)
s.cyl('Left selector embossed pivot','lower',(42,-8.85,10),2,.9,s.edge,'Y',.15)
s.poly('Left static selector arm','lower',[(41,11),(37,7),(39,5),(44,9)],.6,body,.3,y=-9.25)
# Default compact straight magazine, deliberately not the common curved variant.
s.poly('Short straight magazine solid','magazine',[(-2,0),(17,0),(18,-19),(-2,-19)],12.5,s.metal,.55)
for sign in [-1,1]:
    for x in [2,8,14]:s.box('Magazine shallow vertical pressed flute','magazine',(x,sign*6.25,-10),(1.4,.5,13),s.dark,.25)
    s.box('Magazine lower narrow lip','magazine',(8,sign*6.4,-18.2),(20,.7,1.3),s.edge,.23)
s.box('Magazine closed base','magazine',(8,0,-19),(22,13.5,1.7),s.metal,.35)
# Angled grip, attached guard and solid artistic trigger relief.
s.poly('Angled pistol grip body','grip',[(45,4),(59,4),(64,-8),(77,-31),(62,-34),(50,-13),(43,-7)],13,poly,.95)
side_plate(s,'Grip molded side panel','grip',[(50,-6),(59,-8),(71,-29),(64,-29),(53,-12)],6.4,s.rubber,.5,.6)
for sign in [-1,1]:
    for row in range(10):
        s.box('Grip molded check ridge','grip',(55+row*1.12,sign*6.72,-11-row*1.7),(4.5,.4,.8),poly,.2)
s.poly('Grip closed heel','grip',[(60,-32),(76,-33),(76,-35),(61,-36)],14,poly,.45)
guard(s,'lower',[(18,6),(48,6),(47,-8),(42,-12),(25,-12),(18,-7)],[(22,2),(44,2),(43,-6),(40,-9),(27,-9),(22,-6)])
s.poly('Static thin trigger ornament','lower',[(34,3),(37,3),(37,-4),(34,-7),(32,-6),(34,-2)],2.7,s.metal,.24)
# Traditional long solid buttstock, broad flat comb and tapering underface.
s.cyl('Stock shoulder filled neck','stock',(66,0,22),7.9,15,body,'X',.65)
s.poly('Fixed long stock solid','stock',[(66,28),(161,28),(165,24),(165,-14),(157,-13),(96,7),(70,10)],21,poly,1.2)
s.box('Stock closed rubber heel','stock',(164,0,5.5),(3,22,39),s.rubber,.9)
side_plate(s,'Subtle stock side field','stock',[(77,24),(158,24),(158,-7),(100,11),(77,14)],10.3,poly,.45,.9)
for sign in [-1,1]:
    s.box('Stock top molded seam','stock',(117,sign*10.4,25),(78,.3,.6),ring,.2)
    s.screw('Stock inset heel screw','stock',159,18,sign*10.6,.7)
s.box('Attached lower sling relief','stock',(153,0,-12),(7,5,4),body,.6)
for z in range(-11,24,3):s.box('Stock heel fine tread','stock',(165.3,0,z),(.45,21,.9),poly,.2)
# Open carry-handle silhouette with fixed broad supports.
s.poly('Carry handle attached long base','sights',[(-7,31),(61,31),(57,35),(-6,35)],11,body,.45)
carry=s.poly('Carry handle solid frame','sights',[(-5,33),(-4,45),(44,49),(52,46),(57,34)],8.5,body,.55)
s.cut(carry,s.poly('Carry opening cutter','sights',[(1,36),(1,41),(42,44),(47,42),(49,36)],24,s.dark,.4))
s.box('Rear sight drum base','sights',(52,0,44),(8,11,5),body,.65)
s.cyl('Rear sight closed dial','sights',(52,-6,45),2.4,2.2,s.polymer,'Y',.2)
s.box('Front sight lower cross base','sights',(-119,0,24),(10,11,7),body,.5)
t=s.poly('Front triangular sight frame','sights',[(-123,24),(-123,46),(-119,51),(-116,51),(-107,28)],5,body,.45)
s.cut(t,s.poly('Sight triangle silhouette cutter','sights',[(-119,31),(-119,43),(-117,44),(-111,31)],16,s.dark,.2))
s.box('Front top closed notch','sights',(-119,0,49),(3.5,5.8,2),s.metal,.25)
optic(s,24,47)
s.scene['print_segment_breaks_x_mm']='[-31]'
result=finish(s,'依据游戏默认图重建长圆柱分节护木、高提把、三角前瞄具、短直弹匣和固定长枪托；没有采用常见的长弯弹匣改装款。')
