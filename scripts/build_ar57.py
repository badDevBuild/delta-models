"""AR57 exterior: opaque amber top box, long perforated-look forearm, no bottom mag."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('ar57',300,[('receiver','短后部上机匣'),('lower','封闭下框与固定护圈'),('handguard','长排圆点护木'),('front','封闭短前端'),('magazine','顶置实心长匣'),('grip','斜纹握把'),('stock','贴腮与分段尾托'),('sights','前后机械瞄具'),('optic','可选紧凑瞄具')])
body=s.mat('AR57 soft charcoal alloy',(.076,.087,.095),.62,.42)
smoke=s.mat('Opaque smoked amber magazine shell',(.114,.079,.049),.18,.42)
front(s,-149,-131,24,2.5,False)
ventguard(s,-140,-30,25,22,18,'round',body)
# Keep only the model-specific two ordered round arrays below.
for o in list(bpy.data.objects):
 if o.name.startswith('Blind round guard recess'):
  bpy.data.objects.remove(o,do_unlink=True)
for sign in [-1,1]:
 for x in range(-134,-34,5):
  s.cyl('Closed round forearm lower array','handguard',(x,sign*11,22),1.3,.5,s.dark,'Y',.12,24)
  s.cyl('Closed round forearm upper array','handguard',(x+2,sign*11,27),1.3,.5,s.dark,'Y',.12,24)
 s.box('Guard thin continuous lower molding','handguard',(-86,sign*11,18),(102,.5,1),s.edge,.2)
receiver(s,[(-33,35),(55,35),(62,29),(63,15),(-30,15)],20,body)
s.poly('Solid low receiver envelope','lower',[(-33,20),(62,20),(61,7),(44,0),(4,0),(-31,4)],18,body,.65)
s.poly('Closed bottom box well sculpture','lower',[(-31,9),(-5,8),(-4,-11),(-30,-10)],19,body,.6)
for sign in [-1,1]:
 for z in [-6,-2,3]:s.box('Bottom blank sculptural box relief','lower',(-18,sign*9.5,z),(16,.5,.8),s.edge,.17)
 s.cyl('Static selector roundel','lower',(39,sign*9,10),2.2,1,s.edge,'Y',.18)
 s.poly('Static short selector tab','lower',[(38,11),(34,7),(36,5),(42,9)],.6,s.metal,.25,y=sign*9.6)
 s.screw('Lower receiver recessed stud','lower',9,10,sign*9,.85)
guard(s,'lower',[(-3,6),(40,6),(43,-10),(34,-18),(8,-18),(-1,-12)],[(3,2),(36,2),(37,-8),(31,-14),(11,-14),(5,-9)],6)
s.poly('Attached fixed trigger','lower',[(20,3),(23,3),(23,-7),(20,-10),(18,-9),(20,-4)],3,s.metal,.25)
grip(s,36,1)
s.box('Top opaque magazine sculptural saddle','handguard',(-72,0,34.5),(102,15,2),body,.4)
# Long TOP cartridge-box silhouette is completely opaque/solid, no ammunition.
s.poly('Long solid smoked upper magazine','magazine',[(-120,35),(9,35),(9,45),(-116,45),(-121,42)],20,smoke,.8)
for sign in [-1,1]:
 s.box('Magazine long opaque shallow side window','magazine',(-56,sign*10,40),(116,.45,5.7),smoke,.5)
 for z in [35.8,44.2]:s.box('Magazine long perimeter bead','magazine',(-55,sign*10.1,z),(127,.6,.85),s.metal,.2)
 for x in [-118,7]:s.box('Magazine solid end collar','magazine',(x,sign*10.05,40),(3,.7,10),s.metal,.25)
 for x in range(-110,2,7):s.box('Magazine subtle opaque exterior tick','magazine',(x,sign*10.25,39),(1.1,.3,4),smoke,.15)
s.box('Top magazine closed end block','magazine',(8,0,40),(4,23,12),s.metal,.5)
s.cyl('Stock filled neck','stock',(72,0,24),5,25,s.metal,'X',.3)
s.poly('Compact upper stock cheek','stock',[(78,31),(122,31),(124,28),(124,15),(88,13),(78,18)],20,s.polymer,.8)
s.line('Stock narrow lower solid connector','stock',(119,0,18),(141,0,20),2.2,s.metal)
s.line('Stock diagonal solid connector','stock',(119,0,18),(138,0,28),1.7,s.metal)
s.poly('Rear separated sculptural tail pad','stock',[(142,34),(149,34),(149,-18),(143,-19),(139,11),(132,20)],18,s.polymer,.85)
s.box('Stock back closed rubber heel','stock',(149,0,7),(3,19,52),s.rubber,.7)
for sign in [-1,1]:
 s.screw('Rear tail inset stud','stock',143,21,sign*9,.9)
 s.box('Cheek side soft inset','stock',(104,sign*9.8,24),(28,.5,4.5),s.polymer,.5)
s.box('Receiver attached rail spine','receiver',(35,0,35.4),(46,8,2),body,.35)
s.rail('sights',12,57,36,6,4)
s.box('Forward raised sight support','sights',(-131,0,35),(15,13,5),body,.5)
sight(s,'sights',-130,38,True);sight(s,'sights',51,37)
optic(s,34,37.6)
s.scene['print_segment_breaks_x_mm']='[-35]'
result=finish(s,'依据 AR57 默认游戏大图重建顶置烟棕长匣、长排圆点护木、无下垂弹匣的封闭底框、短贴腮块与分段窄尾托；顶置匣为实心不透明艺术件。')
