"""Independent SR-3M game exterior sculpture with short handguard and skeleton stock."""
import sys,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_compact_helpers import finish,optic
s=Sculpture('sr3m',230)
for k,l,v in [('receiver','短机匣与带肋上盖',True),('handguard','斜槽短护木',True),('front','封闭前端与前瞄具',True),('foregrip','固定前竖握把',True),('stock','双杆骨架后托',True),('grip','宽弧形后握把',True),('magazine','短棕黑实心弹匣外观',True),('controls','固定操控与护圈',True),('optic','可选光学装饰',False)]:s.part(k,l,v)
s.scene['print_segment_breaks_x_mm']=[-76.0]
s.parts['handguard']['print_reinforcements']=json.dumps([{'center':[-76,-9.0,36], 'size':[1.6,1.8,12], 'reason':'Fill blind grooves at the miniature glue seam only'}, {'center':[-76,9.0,36], 'size':[1.6,1.8,12], 'reason':'Fill blind grooves at the miniature glue seam only'}])
black=s.mat('Deep charcoal steel',(.043,.051,.058),.7,.39)
magmat=s.mat('Muted brown black magazine',(.095,.05,.039),.12,.64)
# Rounded roof and flat lower receiver are shaped expressly for this short form.
s.poly('Short solid receiver block','receiver',[(-63,44),(-57,49),(10,49),(19,44),(20,29),(9,26),(-11,25),(-26,19),(-59,22)],18.0,black,.7)
s.box('Rounded dust cover crown','receiver',(-21,0,46),(78,17.8,9),s.metal,2.6)
s.poly('Long cover lower shoulder','receiver',[(-60,44),(13,44),(19,40),(16,37),(-60,37)],19.0,s.metal,.65)
for i in range(5):
    x=-53+i*14
    s.box('Dust cover sculpted transverse rib','receiver',(x,0,46.8),(1.25,18.1,7.4),s.edge,.4)
for side in [-1,1]:
    s.box('Closed upper side seam','receiver',(-17,side*9.2,37),(58,.4,1.2),s.dark,.3)
    s.poly('Lower receiver side face','receiver',[(-61,34),(8,34),(10,27),(-7,25),(-25,22),(-58,24)],.4,s.metal,.3,y=side*9.04)
    s.box('Closed side panel inset','receiver',(-12,side*9.46,35),(33,.25,2.0),s.dark,.4)
    for x,z in [(-57,29),(-31,28),(10,35)]:s.screw('Receiver round rivet','receiver',x,z,side*9.35,.82)
# Short handguard has steep slant grooves and two lateral decorative strips.
hand=s.poly('Compact sloped handguard','handguard',[(-106,29),(-106,45),(-73,45),(-68,49),(-61,49),(-61,23),(-67,22),(-76,28)],19.0,s.polymer,.7)
for side in [-1,1]:
    for i in range(5):
        x=-87+i*5
        s.cut(hand,s.poly('Blind diagonal handguard groove','handguard',[(x,31),(x+2,31),(x+10,42),(x+8,42)],1.0,s.dark,.28,y=side*9.38))
    for i in range(6):s.box('Short lateral rail ridge','handguard',(-103+i*3.0,side*10.2,36),(1.7,2.1,9),black,.25)
    s.box('Lateral rail root strip','handguard',(-95.5,side*9.4,36),(20,1.4,8),black,.4)
    s.screw('Handguard rear cosmetic screw','handguard',-66,28,side*9.65,1)
s.box('Short handguard top ledge','handguard',(-93,0,45.6),(26,8,1.7),s.metal,.35)
for i in range(4):s.box('Handguard top shallow blind slot','handguard',(-102+i*6,0,46.51),(3.9,4.8,.13),s.dark,.45)
s.cyl('Closed small front cylinder','front',(-110,0,37),3.7,9,s.steel,'X',.25)
s.cyl('Closed muzzle rim','front',(-114.4,0,37),4.1,1.2,black,'X',.2)
s.cyl('Opaque front disc','front',(-115.05,0,37),2.4,.12,s.dark,'X',.1)
s.box('Solid front sight block','front',(-107,0,41),(5.4,10,9),black,.6)
s.poly('Front fixed sight crest','front',[(-108.5,44),(-108.5,51),(-107,54),(-105.5,51),(-105.5,44)],3,black,.25)
for side in [-1,1]:s.box('Front sight shoulder','front',(-107,side*2.5,49),(3,1.4,6),s.metal,.3)
# Default front grip is retained as a fixed solid connected to the lower handguard.
s.box('Foregrip broad contact foot','foregrip',(-98,0,26),(10.6,13,5.5),black,.7)
s.poly('Front grip slightly tapered core','foregrip',[(-103,25),(-92,25),(-93,17),(-94,-6),(-97,-9),(-103,-8),(-104,-5)],11.8,s.polymer,1.0)
for side in [-1,1]:
    s.poly('Front grip inset face','foregrip',[(-101,19),(-95,19),(-96,-5),(-101,-5)],.3,s.rubber,.6,y=side*5.89)
    for i in range(9):s.box('Front grip shallow cross ribs','foregrip',(-98.4,side*6.1,17-i*2.3),(6.2,.35,.65),black,.2)
# Short curved solid magazine, brown black rather than an extended option.
s.poly('Short curved magazine sculpture','magazine',[(-59,23),(-33,20),(-35,2),(-39,-14),(-43,-16),(-62,-10),(-64,-6),(-60,9)],12.0,magmat,.7)
for side in [-1,1]:
    s.poly('Magazine inset main face','magazine',[(-58,17),(-36,15),(-38,3),(-42,-11),(-60,-7)],.3,magmat,.35,y=side*6.05)
    for i in range(7):
        z=14-i*3.8
        s.poly('Short magazine embossed rib','magazine',[(-59,z),(-37.5-max(0,-z)*.16,z-2),(-38-max(0,-z)*.16,z-2.8),(-59,z-.8)],.65,s.metal,.2,y=side*6.08)
s.poly('Magazine lower heel','magazine',[(-62,-8),(-40,-14),(-40,-17),(-64,-11)],13.1,black,.4)
s.poly('Broad sculpted rear grip','grip',[(-9,27),(11,27),(10,15),(11,5),(19,-22),(17,-25),(0,-26),(-3,-20),(-4,-8),(-7,0),(-13,12)],15.8,s.polymer,1.3)
for side in [-1,1]:
    s.poly('Grip broad rubber face','grip',[(-7,20),(6,20),(6,12),(7,4),(15,-20),(2,-22),(-.5,-15),(-2,-6),(-7,4)],.25,s.rubber,.7,y=side*7.9)
    for i in range(8):
        z=15-i*4.4;x=-1+max(0,-z)*.25
        s.box('Grip low horizontal texture','grip',(x,side*8.06,z),(7,.25,.38),s.polymer,.12)
# Single connected rod stock silhouette, no movable hinge.
s.box('Closed rear stock hinge','stock',(22,0,34),(11,16,18),black,.7)
s.box('Stock broad front shoulder','stock',(31,0,35),(13,12,14),s.metal,.65)
s.line('Stock upper solid rod','stock',(31,0,39),(111,0,38),2.0,s.metal)
s.line('Stock lower curved rod front','stock',(30,0,30),(97,0,5),2.05,s.metal)
s.line('Stock lower curved rod heel','stock',(97,0,5),(111,0,4),2.05,s.metal)
s.poly('Fixed thin rear shoulder pad','stock',[(108,40),(114,40),(115,37),(114,2),(111,0),(108,1)],9.5,s.rubber,.7)
s.box('Stock central wrap strip','stock',(72,0,25.8),(6,5.7,28),s.rubber,.5)
for side in [-1,1]:
    s.box('Hinge inset cover','stock',(26,side*8.0,34),(7.5,.8,11),s.polymer,.7)
    s.screw('Stock fixed hinge stud','stock',24,35,side*8.5,1.2)
# Fixed controls and a solid trigger ornament inside the exterior guard.
guard=s.poly('Fixed angular guard','controls',[(-32,25),(-10,25),(-9,16),(-14,5),(-30,5),(-36,9)],6.2,black,.6)
s.cut(guard,s.poly('Exterior guard silhouette opening','controls',[(-31,22),(-13,22),(-12,17),(-16,9),(-28,9),(-32,11)],20,s.dark,.55))
s.poly('Fixed narrow trigger ornament','controls',[(-19,25),(-16,24),(-17,14),(-19,11),(-22,11),(-20,14)],2.5,s.steel,.35)
for side in [-1,1]:
    s.poly('Fixed long selector ornament','controls',[(-45,35),(7,34),(10,32),(7,30),(-10,31),(-45,33)],.75,s.metal,.35,y=side*9.45)
    s.box('Fixed charging stalk','controls',(-29,side*11.2,37),(9,5.5,2.4),black,.45)
    s.cyl('Fixed charging knob','controls',(-25,side*13.5,37),2.4,3.5,s.metal,'Y',.2)
    s.screw('Selector fixed pivot','controls',9,33,side*10.0,1.1)
s.box('Rear fixed sight foot','controls',(-64,0,49),(8,11,2.5),black,.4)
s.box('Rear fixed sight crest','controls',(-63,0,51),(3.8,8.5,3.4),s.metal,.35)
# Digital optic rests on a short artist-scale filled saddle above the cover.
s.box('Optic solid lower saddle','optic',(-17,0,50.2),(23,10,3.0),black,.5)
optic(s,'optic',-17,52.1,.88)
result=finish(s,'https://www.imfdb.org/images/thumb/a/a9/DFHO_SR3M.jpg/600px-DFHO_SR3M.jpg',['依据游戏短护木、斜槽、默认前竖握把、短棕黑弹匣和双杆骨架托重新建模。','上盖肋线、双侧操控为固定浅浮雕；托杆加粗作为微缩雕塑，隐藏面和细纹为艺术推断。'])
