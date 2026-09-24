"""AK-12 game-side miniature exterior; closed front and inert details only."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rifle_batch3_helpers import *
s=Sculpture('ak12',300)
for key,label,show in [('receiver','折线机匣外观',True),('cover','上盖与装饰轨',True),('handguard','短护木外观',True),('front','封闭细前端',True),('magazine','弯曲实心弹匣',True),('grip','握把与固定护圈',True),('stock','开窗枪托外观',True),('sights','固定机械瞄具',True),('optic','可选紧凑瞄具',False)]:s.part(key,label,show)
body=s.mat('AK grey alloy',(.115,.124,.129),.66,.45)
poly=s.mat('AK matte graphite',(.043,.049,.054),.08,.69)
mag=s.mat('Dark magazine molded polymer',(.037,.034,.034),.08,.69)
# Narrow exposed front, all end faces filled.
s.cyl('Solid sealed front rod','front',(-117,0,19),2.6,66,s.metal,'X',.17)
s.cyl('Closed shallow end','front',(-150,0,19),2.5,.2,s.dark,'X',.04)
s.cyl('Front shoulder ornament','front',(-128,0,19),3.7,6,body,'X',.25)
s.cyl('Short upper front spine','front',(-94,0,26),3,31,body,'X',.2)
s.box('Attached front shoulder block','front',(-105,0,22),(11,10,10),body,.8)
s.poly('Front sight triangulated root','sights',[(-110,22),(-110,33),(-105,44),(-101,44),(-97,26)],6,body,.5)
s.cyl('Closed front sight face','sights',(-104,0,40),2.1,3,body,'X',.13)
s.cyl('Blind front sight inset','sights',(-105.6,0,40),.9,.2,s.dark,'X',.03)
# Handguard side holes are blind shadow panels, sculptural shell is solid.
s.poly('Angular handguard solid shell','handguard',[(-84,34),(-25,34),(-20,29),(-20,10),(-39,7),(-82,10),(-87,15)],18,body,.9)
s.poly('Handguard lower chamfer','handguard',[(-82,13),(-39,11),(-24,8),(-39,6),(-83,9)],17,poly,.55)
s.rail('handguard',-83,-24,34.5,7,3.7)
for sign in [-1,1]:
    s.box('Handguard blind broad side recess','handguard',(-54,sign*9,25),(23,.5,5),s.dark,.7)
    for x in [-79,-63,-40,-25]:s.cyl('Handguard closed circular relief','handguard',(x,sign*9.12,28),1.8,.32,s.dark,'Y',.1)
    s.box('Handguard lower long shallow groove','handguard',(-60,sign*9.05,16),(39,.4,2),s.dark,.6)
    s.box('Handguard silver inset bar','handguard',(-54,sign*9.25,25),(11,.35,3),s.edge,.3)
    for x in [-60,-49]:s.screw('Handguard flush decoration','handguard',x,25,sign*9.22,.7)
# Folded sheet silhouette and rounded dust cover, no receiver cavity.
s.poly('Filled receiver contour','receiver',[(-26,31),(55,31),(75,22),(78,10),(74,3),(-23,3),(-28,12)],17,body,.7)
s.poly('Upper arched cover','cover',[(-25,32),(-22,38),(57,38),(67,32),(68,26),(-25,26)],16.5,body,1)
s.rail('cover',-20,61,38.2,7.5,3.7)
for sign in [-1,1]:
    s.box('Receiver lower folded edge','receiver',(24,sign*8.5,6),(100,.55,2.2),s.metal,.3)
    s.box('Cover long pressed side seam','cover',(16,sign*8.24,32),(77,.45,1.35),s.dark,.25)
    s.box('Cover lower raised edge','cover',(16,sign*8.48,28),(77,.55,1),s.edge,.22)
    for x,z in [(-20,13),(-10,10),(48,10),(68,12),(71,20)]:s.screw('Receiver blind rivet','receiver',x,z,sign*8.44,.8)
    s.box('Small blank identity panel','receiver',(22,sign*8.58,15),(15,.35,6),body,.2)
s.poly('Fixed side selector decorative blade','receiver',[(2,19),(27,24),(53,15),(50,11),(28,17),(5,14)],.9,s.metal,.3,y=8.65)
s.cyl('Selector blind pivot','receiver',(4,9.2,17),2,.7,s.edge,'Y',.15)
s.box('Fixed side handle support','receiver',(-6,-10.2,26),(6,5,3),body,.35)
s.cyl('Fixed side handle knob','receiver',(-6,-13,26),1.7,4,body,'Y',.2)
# Curved AK magazine has a broad smooth spine and stepped peripheral ribs.
s.poly('Curved magazine filled silhouette','magazine',[(-7,6),(22,4),(20,-19),(10,-44),(-4,-67),(-24,-56),(-12,-31),(-8,-12)],13,mag,.8)
side_plate(s,'Magazine shallow flat panel','magazine',[(-4,0),(18,-1),(15,-19),(6,-41),(-5,-59),(-18,-53),(-9,-31)],6.42,poly)
for sign in [-1,1]:
    for j in range(12):
        z=-9-j*3.7;x=-7-(max(0,j-2)*1.05)
        s.box('Magazine perimeter molded notch','magazine',(x,sign*6.65,z),(2.3,.38,1.3),s.edge,.17)
    for x,z in [(9,-7),(6,-21),(0,-36),(-8,-51)]:s.box('Magazine shallow center dash','magazine',(x,sign*6.6,z),(1,.35,6),s.dark,.2)
s.poly('Magazine closed heel','magazine',[(-25,-57),(-4,-69),(-1,-66),(-23,-54)],14,poly,.5)
# Broad angled grip, finger contours as overlapping shallow forms.
s.poly('Grip closed body','grip',[(52,6),(64,4),(66,-11),(76,-37),(62,-40),(58,-31),(58,-26),(54,-24),(54,-18),(50,-16),(49,-11),(45,-6)],14,poly,1)
side_plate(s,'Grip side textured panel','grip',[(53,-6),(62,-8),(70,-34),(62,-34),(54,-19)],6.95,s.rubber,.4,.6)
dot_texture(s,'grip',13,55,-10,7.15,.48,4,poly)
# Finger scallops are integrated into the grip outline, not detached round ornaments.
g=s.poly('Fixed trigger guard frame','grip',[(20,5),(51,4),(50,-9),(44,-14),(27,-14),(20,-9)],7,body,.65)
s.cut(g,s.poly('Guard window cutter','grip',[(24,1),(46,0),(45,-7),(42,-10),(28,-10),(25,-7)],20,s.dark,.5))
s.poly('Fixed trigger decoration','grip',[(36,4),(39,4),(39,-5),(36,-9),(34,-8),(36,-4)],2.8,s.metal,.3)
# Distinct adjustable-looking skeleton stock remains a single static sculpture.
s.cyl('Solid stock spine','stock',(94,0,14),4.4,39,body,'X',.5)
s.poly('Stock upper broad shoulder','stock',[(95,21),(146,21),(148,16),(145,8),(100,8),(94,12)],18,poly,.85)
s.poly('Stock rear butt solid bar','stock',[(143,21),(150,21),(150,-24),(143,-24)],19,s.rubber,.8)
s.poly('Stock descending lower brace','stock',[(94,14),(101,11),(143,-18),(145,-25),(136,-22),(94,0)],9.5,poly,.7)
s.poly('Stock internal shallow ledge','stock',[(104,6),(143,6),(143,1),(111,1)],12,poly,.5)
for sign in [-1,1]:
    s.box('Stock cheek side relief','stock',(123,sign*8.95,17),(37,.4,3.1),body,.45)
    s.poly('Stock lower contour ridge','stock',[(101,4),(137,-17),(139,-20),(101,0)],.35,body,.2,y=sign*4.65)
    s.screw('Stock shoulder decorative stud','stock',101,12,sign*9,.9)
for z in range(-21,21,3):s.box('Buttpad shallow tread','stock',(150,0,z),(.6,19,.8),poly,.15)
sight(s,'sights',57,39)
optic(s,17,40)
s.scene['print_segment_breaks_x_mm']='[-45]'
result=finish(s,'保留默认游戏图的短护木、无长侧导轨、细封闭前端、棱面机匣、弯曲弹匣和开窗枪托；默认不带瞄具配件。')
