"""S12K game exterior, miniature sealed sculpture with independent profiles."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_long_helpers import scope,finish
s=Sculpture('s12k',300)
for key,label,show in [('receiver','封闭冲压机匣',True),('cover','圆棱上盖',True),('handguard','带槽方护木',True),('barrel','封闭短前杆',True),('stock','黑色固定整托',True),('magazine','斜直匣外壳装饰',True),('grip','握把与固定护圈',True),('sights','固定机械瞄具',True),('optic','可选短望远瞄具',False)]:s.part(key,label,show)
grey=s.mat('Mottled grey alloy',(.12,.13,.134),.58,.52)
rubbed=s.mat('Polymer rubbed bevels',(.095,.1,.105),.04,.61)
s.scene['print_segment_breaks_x_mm']='[-38]'
s.poly('Closed stamped lower receiver','receiver',[(-35,34),(-30,38),(51,38),(58,33),(60,16),(-32,16)],22,grey,.75)
for sign in [-1,1]:
    s.box('Receiver lower seam','receiver',(11,sign*11.1,18),(88,.55,1.1),s.edge,.25)
    s.poly('Receiver pressed middle recess','receiver',[(-17,21),(-15,25),(-7,25),(-6,21)],.5,s.dark,.7,y=sign*11.16)
    s.poly('Receiver shallow oval back recess','receiver',[(16,22),(22,26),(35,26),(38,23),(31,21),(20,21)],.6,s.polymer,.65,y=sign*11.2)
    for x,z in [(-28,22),(-26,31),(-3,21),(44,22),(53,28)]:s.screw('Receiver visible rivet','receiver',x,z,sign*11.3,.8)
s.poly('Fixed side selector ornament','receiver',[(15,30),(42,25),(41,22),(32,22),(12,28)],1.1,s.metal,.5,y=-12)
s.cyl('Selector fixed round boss','receiver',(15,-12.4,29),2.2,1,s.steel,'Y',.2)
s.box('Closed side shutter','receiver',(-5,-11.3,33),(30,.5,5),s.dark,.55)
s.box('Closed shutter silver surface','receiver',(-5,-11.62,33),(25,.25,2.7),s.steel,.35)
s.box('Fixed side handle bridge','receiver',(-7,-13,31),(14,6,2.4),s.metal,.45)
s.cyl('Fixed side handle knob','receiver',(-13,-16,31),1.8,4.2,s.metal,'Y',.3)
# Rounded top cover has large flat-bottom overlap, with short ribbed seams.
s.poly('Rounded closed upper cover','cover',[(-32,34),(-31,40),(-27,43),(48,43),(55,39),(57,34)],19.8,s.metal,1.2)
s.box('Top cover subtle crown','cover',(11,0,42.3),(70,10,1.8),s.edge,.65)
for sign in [-1,1]:
    s.box('Upper cover long seam','cover',(9,sign*9.97,36),(77,.5,.7),s.polymer,.2)
    for x in [-22,3,28,47]:s.box('Cover narrow transverse ribs','cover',(x,sign*9.95,39),(1,.4,4),s.edge,.3)
# Squared ribbed handguard follows the Saiga game silhouette and shallow slots.
s.poly('Boxy closed lower handguard','handguard',[(-115,37),(-113,42),(-33,42),(-29,36),(-30,20),(-38,18),(-105,18),(-114,22)],23,s.polymer,1)
for sign in [-1,1]:
    s.poly('Sweeping lower handguard facet','handguard',[(-110,22),(-97,28),(-42,28),(-32,23),(-38,21),(-102,21)],.55,rubbed,.65,y=sign*11.51)
    s.box('Upper handguard horizontal seam','handguard',(-74,sign*11.66,40),(75,.65,.9),s.edge,.25)
    for x in [-96,-82,-68,-54]:
        s.box('Handguard blind horizontal slot','handguard',(x,sign*11.6,36),(10.2,.8,2.6),s.dark,.75)
        s.box('Slot lower reflected lip','handguard',(x,sign*12.04,35.2),(8,.2,.45),grey,.12)
    s.screw('Handguard front pin','handguard',-108,28,sign*11.8,.9)
    s.screw('Handguard rear pin','handguard',-35,30,sign*11.8,.9)
s.cyl('Solid short closed front','barrel',(-131,0,27),3.5,38,s.metal,'X',.25,64)
s.cyl('Solid rounded front collar','barrel',(-147,0,27),3.7,6,s.metal,'X',.2)
s.cyl('Closed dark forward disc','barrel',(-150.08,0,27),2.5,.18,s.dark,'X',.02)
s.cyl('Closed upper short connection','barrel',(-109,0,40),2.7,17,s.metal,'X',.25)
s.box('Front upper contact block','barrel',(-111,0,38),(5.5,8,7.2),s.metal,.55)
s.poly('Black fixed traditional buttstock','stock',[(56,34),(69,32),(82,30),(96,32),(109,35),(149,35),(150,31),(149,-2),(141,-4),(104,6),(72,14),(58,17)],20.5,s.polymer,1.8)
s.poly('Stock upper rubbed comb','stock',[(95,31),(109,34),(145,34),(148,32),(145,30),(106,31)],20,rubbed,.7)
s.poly('Stock rear rubber pad','stock',[(148,36),(150,35),(150,-4),(148,-5)],21.4,s.rubber,.5)
for sign in [-1,1]:
    s.poly('Stock long sculpted panel','stock',[(75,25),(108,27),(114,25),(113,18),(100,18),(74,22)],.55,s.dark,.65,y=sign*10.3)
    s.poly('Stock panel inner face','stock',[(79,24),(107,25),(111,24),(110,20),(101,20)],.4,rubbed,.5,y=sign*10.63)
    for x,z in [(68,25),(141,3)]:s.screw('Stock fixed screw','stock',x,z,sign*10.4,.95)
s.poly('Filled slanted straight magazine','magazine',[(-17,18),(9,18),(6,5),(-8,-35),(-17,-37),(-36,-30),(-27,-4)],14.4,s.polymer,.9)
for sign in [-1,1]:
    s.poly('Slant magazine broad inset','magazine',[(-14,12),(4,12),(-9,-30),(-30,-25)],.6,s.metal,.65,y=sign*7.25)
    s.poly('Magazine inset top panel','magazine',[(-12,9),(1,9),(-3,-7),(-17,-6)],.45,s.dark,.4,y=sign*7.6)
    s.poly('Magazine inset bottom panel','magazine',[(-18,-9),(-4,-10),(-9,-25),(-23,-21)],.45,s.dark,.4,y=sign*7.6)
    s.line('Magazine front raised rib','magazine',(-24,sign*7.65,-22),(-13,sign*7.65,10),.55,rubbed)
s.poly('Magazine wide base flange','magazine',[(-36,-28),(-9,-36),(-6,-33),(-7,-39),(-17,-41),(-38,-33)],15.5,s.metal,.65)
s.poly('Black slanted pistol grip','grip',[(38,18),(54,17),(55,6),(66,-20),(64,-25),(53,-28),(47,-24),(41,-3)],14.5,s.polymer,1.1)
for sign in [-1,1]:
    s.poly('Grip inset panel','grip',[(43,11),(50,10),(59,-19),(54,-22),(49,-18)],.6,s.rubber,.55,y=sign*7.32)
    for z in [-14,-9,-4,1]:s.box('Grip shallow texture','grip',(50-z*.22,sign*7.7,z),(4.5,.35,.55),rubbed,.15)
g=s.poly('Fixed rounded trigger guard','grip',[(11,17),(40,17),(43,3),(39,-3),(18,-3),(11,3)],6,s.metal,.85)
s.cut(g,s.poly('Guard external opening','grip',[(15,14),(36,14),(39,3),(36,0),(20,0),(15,4)],16,s.dark,.55))
s.poly('Fixed trigger crescent','grip',[(28,16),(31,16),(31,9),(27,3),(24,3),(28,9)],2.7,s.steel,.3)
s.box('Front low sight footing','sights',(-110,0,42),(8,7.2,2.7),s.metal,.35)
s.box('Front fixed blade','sights',(-110,0,44),(3.2,2.7,3),s.edge,.25)
s.box('Rear tangent root','sights',(-36,0,41),(21,11,3.6),s.metal,.45)
s.poly('Rear fixed tangent ramp','sights',[(-47,42),(-47,44),(-28,46),(-25,43)],7.7,s.edge,.35)
s.box('Rear fixed cross blade','sights',(-26,0,45),(3.7,11,3),s.metal,.4)
scope(s,'optic',13,43.4,48)
result=finish(s,'https://www.imfdb.org/images/thumb/a/a4/DFHO_Saiga.jpg/600px-DFHO_Saiga.jpg',['保留默认黑色固定整托、带横槽方护木、圆棱上盖、斜直匣与短前杆；不加入参考默认图没有的鼓形配件。','所有槽为浅盲槽或表面色块，操控装饰固定，前端完全封闭。'])
