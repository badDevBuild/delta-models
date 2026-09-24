"""AKS-74U game-inspired small solid decorative exterior, miniature mm."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch4_rifle_helpers import *
s=Sculpture('aks74u',230)
for key,label,show in [('body','紧凑机匣外观',True),('cover','圆脊上盖',True),('handguard','棕木上下护木',True),('front','封闭短前端',True),('magazine','棕色实心弯弹匣',True),('grip','握把与固定护圈',True),('stock','三角镂空固定托',True),('sights','固定机械瞄具',True),('optic','可选紧凑瞄具',False)]:s.part(key,label,show)
wood=s.mat('Warm laminated walnut',(.27,.115,.047),.02,.46)
woodlight=s.mat('Walnut grain highlights',(.31,.145,.065),.03,.55)
bakelite=s.mat('Reddish brown molded surface',(.23,.078,.028),.02,.53)
body=s.mat('Cool blued stamped steel',(.09,.11,.122),.7,.38)
# Small protruding sealed cylinder; there is no bore.
s.cyl('Sealed short front tip','front',(-109,0,18),2.9,12,body,'X',.2)
s.cyl('Flat closed dark end','front',(-115,0,18),2.75,.15,s.dark,'X',.04)
s.cyl('Front sleeve collar','front',(-103,0,18),4.1,5,body,'X',.3)
s.box('Front sight broad attached block','front',(-103,0,23),(8,10,13),body,.6)
s.poly('Sight tapered front tower','sights',[(-108,23),(-106,36),(-103,38),(-101,38),(-98,25)],5,body,.4)
s.box('Front sight top notch shadow','sights',(-103,0,36),(3,5.4,1.4),s.dark,.25)
s.box('Front sight closed central post','sights',(-103,0,37.8),(1.3,2,3),s.metal,.2)
# Two offset hardwood lobes, slightly concave-looking outlines and modeled veneers.
s.poly('Short lower walnut shell','handguard',[(-101,21),(-61,21),(-56,17),(-56,7),(-63,6),(-99,11),(-102,15)],17,wood,.95)
s.poly('Upper walnut cap','handguard',[(-100,30),(-66,30),(-63,27),(-65,20),(-98,20)],14,wood,1)
for sign in [-1,1]:
    s.poly('Lower wood scalloped dark inset','handguard',[(-97,19),(-67,17),(-62,15),(-64,12),(-95,14)],.32,woodlight,.7,y=sign*8.4)
    for x in [-94,-79]:s.box('Blind upper vent shadow','handguard',(x,sign*7.05,22),(8,.35,1.8),s.dark,.65)
woodgrain(s,'handguard',-98,-65,25,7.05,woodlight,3)
woodgrain(s,'handguard',-96,-64,11.5,8.45,woodlight,3)
s.box('Front black wood end collar','handguard',(-101,0,18),(2.2,17,15),body,.4)
s.box('Rear black wood band','handguard',(-59,0,16),(2.5,17.5,21),body,.4)
# Small stamped receiver with separate rounded top cover and exterior reliefs.
s.poly('Filled receiver body','body',[(-58,28),(27,28),(34,21),(33,5),(-56,5)],16,body,.55)
s.poly('Low rounded dust cover','cover',[(-59,27),(-55,33),(24,33),(31,28)],16,body,.9)
s.box('Cover central raised ridge','cover',(-15,0,32.6),(75,6,1.1),s.edge,.3)
for sign in [-1,1]:
    s.box('Receiver lower folded hem','body',(-13,sign*8.05,7),(87,.55,1.5),s.metal,.22)
    s.box('Cover long seam','cover',(-15,sign*7.8,28.7),(73,.4,.85),s.dark,.2)
    for x,z in [(-53,23),(-49,13),(-40,10),(21,11),(29,19)]:s.screw('Closed stamped rivet','body',x,z,sign*8,.66)
    s.box('Blank decorative label pad','body',(-13,sign*8.1,17),(20,.28,5),body,.25)
    s.box('Upper receiver inset line','body',(-6,sign*8.06,24),(50,.4,1),s.dark,.2)
s.poly('Blind side selector relief','body',[(-10,20),(11,23),(25,15),(22,12),(9,18),(-11,17)],.75,s.metal,.3,y=8.25)
s.cyl('Selector round embossed root','body',(-10,8.65,18),1.8,.8,s.edge,'Y',.15)
s.box('Fixed side handle stem','body',(-43,-9.4,26),(6,4,2.7),body,.3)
s.cyl('Fixed side handle decorative knob','body',(-43,-11.8,26),1.4,3.2,s.metal,'Y',.2)
# Narrow curved solid brown magazine, smooth broad panel with edge lips.
s.poly('Brown curved magazine silhouette','magazine',[(-41,8),(-17,6),(-21,-12),(-28,-31),(-37,-48),(-57,-39),(-48,-19)],11.5,bakelite,.7)
side_plate(s,'Magazine quiet side field','magazine',[(-39,1),(-20,0),(-25,-18),(-38,-43),(-53,-37),(-45,-17)],5.65,woodlight,.3,.5)
for sign in [-1,1]:
    s.poly('Magazine long front seam','magazine',[(-41,4),(-43,-15),(-52,-38),(-50,-39),(-41,-16),(-39,4)],.35,wood,.2,y=sign*5.84)
    s.poly('Magazine rear seam','magazine',[(-20,4),(-25,-17),(-37,-44),(-35,-45),(-23,-18),(-18,4)],.35,wood,.2,y=sign*5.8)
s.poly('Magazine closed heel trim','magazine',[(-58,-39),(-37,-49),(-35,-46),(-55,-37)],12.4,wood,.45)
# Brown pistol grip and static silhouette frame, no interior action.
s.poly('Brown angled grip','grip',[(11,7),(28,6),(30,-9),(39,-29),(27,-34),(17,-12)],13,bakelite,.9)
side_plate(s,'Grip inset slab','grip',[(17,1),(26,1),(26,-10),(34,-27),(28,-29),(21,-12)],6.35,wood,.4,.55)
for sign in [-1,1]:
    for j in range(10):s.box('Grip shallow vertical check','grip',(23+j*.65,sign*6.61,-7-j*1.8),(4,.35,.5),woodlight,.12)
guard(s,'grip',[(-15,7),(13,7),(14,-6),(9,-10),(-10,-10),(-16,-5)],[(-11,3),(9,3),(10,-4),(7,-7),(-8,-7),(-12,-4)])
s.poly('Static trigger ornament','grip',[(-2,6),(1,6),(1,-2),(-2,-5),(-4,-4),(-2,0)],2.8,body,.25)
# Folded-looking triangular stock is three connected solid graphic bars.
s.box('Fixed stock shoulder hinge block','stock',(35,0,15),(8,14,21),body,.65)
s.poly('Triangular stock top bar','stock',[(35,21),(113,17),(113,12),(37,16)],8.5,body,.7)
s.poly('Triangular stock lower bar','stock',[(34,12),(39,8),(112,-13),(114,-9),(40,14)],8,body,.65)
s.poly('Closed stock butt bar','stock',[(110,18),(115,18),(115,-15),(109,-15)],11,body,.75)
for sign in [-1,1]:
    s.screw('Stock decorative end stud','stock',112,13,sign*5.45,.7)
    s.screw('Stock decorative root stud','stock',35,16,sign*7,.9)
s.poly('Low rear notch base','sights',[(-54,31),(-50,36),(-44,33),(-26,33),(-24,37),(-19,37),(-15,32)],7,body,.35)
optic(s,-12,33.5)
s.scene['print_segment_breaks_x_mm']='[-63]'
result=finish(s,'依据游戏默认图重建：短棕木上下护木、无长外露前杆、棕色平滑弯弹匣、棕握把和细三角开窗铁托。')
