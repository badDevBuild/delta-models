"""Author an inert, reference-derived AKM display miniature through Blender MCP."""
from pathlib import Path
import sys, math
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_ap import Model

m=Model('akm','AKM · 木色基础外观',294)
m.scene['print_segment_breaks_x_mm']='[-49.73]'  # Keep the curved magazine within one length segment.
steel=m.mat('AKM worn blued steel',(.068,.078,.081),.78,.38)
covermat=m.mat('AKM pressed steel cover',(.105,.117,.119),.8,.32)
edge=m.mat('AKM polished edge',(.18,.195,.192),.8,.31)
dark=m.mat('AKM shallow recess',(.019,.025,.027),.3,.63)
wood=m.mat('AKM amber laminate wood',(.27,.092,.027),.04,.41)
woodlight=m.mat('AKM wood figure light',(.34,.135,.044),.02,.49)
wooddark=m.mat('AKM wood figure dark',(.145,.042,.012),.02,.5)
bakelite=m.mat('AKM brown grip',(.135,.050,.026),.01,.53)
rubber=m.mat('AKM butt plate',(.035,.044,.045),.4,.61)
for key,label in [('receiver','机匣外观'),('cover','顶部盖板'),('handguard','木色护木'),('stock','木色整托'),('grip','后握把'),('magazine','实心弯曲弹匣外观'),('barrel','封口装饰前端'),('front_sight','固定前瞄具'),('rear_sight','固定后瞄具')]:m.part(key,label)

# The body is deliberately filled. Details are shallow exterior ornament only.
m.poly('Stamped receiver closed body','receiver',[(-49,24),(43,24),(49,17),(48,1),(12,-1),(-40,0),(-49,6)],17.0,steel,.7)
m.box('Receiver upper shoulder','receiver',(-1,0,24),(93,18,3.2),steel,.5)
m.poly('Front receiver shoulder','receiver',[(-51,25),(-43,25),(-43,2),(-51,6)],18.3,covermat,.45)
m.box('Rear stock tang exterior','receiver',(49,0,18),(12,13,8),steel,.6)
m.box('Top cover rounded pressing','cover',(-1,0,28.4),(88,16.4,9),covermat,2.9)
m.box('Cover rolled lower seam','cover',(-1,0,25.1),(88.5,17,1.4),edge,.32)
for px in [-8,12,32]:
    m.path('Cover shallow pressed crown','cover',[(px,7.5*math.cos(i*math.pi/18),27.0+6.2*math.sin(i*math.pi/18)) for i in range(19)],.27,steel)
m.box('Cover end tab','cover',(42.8,0,28.5),(3.8,11,6.3),steel,.8)
m.box('Cover fixed rear stud','cover',(43.5,0,32.8),(3.3,4.7,1.5),edge,.45)
for side in [-1,1]:
    y=side*8.55
    m.poly('Receiver stamped shallow side facet','receiver',[(-40,22),(37,22),(42,16),(40,4),(-37,4)],.28,covermat,.3,y)
    m.box('Receiver lower seam','receiver',(-1,y,2.3),(82,.6,.9),edge,.15)
    for x,z,r in [(-43,20,1.1),(-42,6,1.1),(-30,5,.95),(-17,5,.95),(35,6,.95),(40,18,1.1),(25,16,1.0)]:
        m.cyl('Dome receiver rivet','receiver',(x,y+side*.3,z),r,.7,steel,'Y',.25,24)
    m.poly('Blind magazine well dimple','receiver',[(-27,12),(-21,14),(-11,13),(-9,10),(-12,7),(-24,8)],.45,dark,.5,y+side*.3)
    m.poly('Magazine well dimple rim','receiver',[(-25,11.3),(-19,12.5),(-12,11.6),(-12,9.5),(-23,9.2)],.3,steel,.4,y+side*.59)
    m.path('Cover rolled shoulder highlight','cover',[(x,side*7.55,30.2) for x in [-42,-25,0,20,40]],.23,edge)
    # Closed side panel, not an opening or functional action.
    m.box('Sealed side recess','receiver',(-5,y+side*.36,20.5),(30,.25,3.2),dark,.65)
    m.box('Side relief bevel','receiver',(-5,y+side*.53,22.0),(30,.55,.7),edge,.2)
# Fixed external side silhouettes.
m.cyl('Selector pivot ornament','receiver',(32,-9.5,17),2.1,1.7,steel,'Y',.3)
m.poly('Fixed selector lever silhouette','receiver',[(32,18),(7,16),(-16,12),(-17,10),(-12,9),(12,13),(33,15)],.9,steel,.45,-9.5)
m.box('Selector thumb tab','receiver',(-15,-10.1,10.5),(7,2.0,2.9),edge,.4)
for i in range(4):m.box('Selector tab grip line','receiver',(-17+i*1.3,-11.2,10.5),(.35,.3,1.9),dark,.07)
m.rod('Fixed handle external stem','receiver',(-6,-8.5,21),(-6,-15.1,21),1.1,steel)
m.cyl('Fixed handle knob','receiver',(-6,-15,21),1.8,4.4,edge,'X',.6)

# Wooden handguard and upper rounded wood cover, no separate real interface.
m.poly('Lower wooden guard','handguard',[(-104,15),(-95,18),(-52,18),(-47,13),(-48,1),(-57,-2),(-96,-1),(-104,4)],17.8,wood,1.7)
m.box('Upper wooden guard','handguard',(-77,0,23.8),(41,14.5,11.2),wood,3.3)
for x in [-98,-54]:m.box('Handguard dark retaining ornament','handguard',(x,0,14.4),(3.2,19.0,12.6),steel,.6)
for side in [-1,1]:
    m.path('Wood guard finger contour','handguard',[(-96,side*9.0,10),(-85,side*9.0,8.7),(-70,side*9.0,8.5),(-57,side*9.0,10)],.28,wooddark)
    for j in range(8):
        z=2.8+j*1.16
        pts=[(-95+i*6.1,side*8.93,z+.35*math.sin(i*.85+j)) for i in range(7)]
        m.path('Handguard fine wood grain','handguard',pts,.075,wooddark if j%3 else woodlight)
    for j in range(4):
        m.path('Upper guard wood grain','handguard',[(-94+i*6.1,side*6.9,25.5+j*.65+.18*math.sin(i+j)) for i in range(6)],.08,wooddark)
    for x in [-95,-59]:m.screw('Handguard band rivet','handguard',x,13.0,side*9.55,.7,edge,dark)

# Barrel-shaped ornament is capped and solid; the entire miniature is nonfunctional.
m.cyl('Solid exterior barrel ornament','barrel',(-95.5,0,14),2.55,101,steel)
m.cyl('Solid front tip','barrel',(-144,0,14),3.2,6,covermat,b=.25)
m.cyl('Filled front face','barrel',(-147.0,0,14),2.80,.18,dark,b=.04)
m.cyl('Front cap inset relief','barrel',(-147.11,0,14),1.4,.08,steel,b=.03)
m.cyl('Tip collar','barrel',(-139.6,0,14),2.95,1.1,edge,b=.15)
m.cyl('Gas block exterior collar','barrel',(-83.0,0,14),4.0,6.4,steel,b=.35)
m.poly('Gas block angled exterior','barrel',[(-87,15),(-86,25),(-80,28),(-77,25),(-79,14)],8.3,steel,.6)
m.cyl('Upper closed tube ornament','barrel',(-61,0,26),2.8,42,steel,b=.3)
m.cyl('Upper front ring','barrel',(-80.0,0,26),3.4,3.6,edge,b=.2)
m.rod('Under barrel strengthening rod','barrel',(-139.0,0,9.6),(-61,0,9.6),.85,steel)

# Raised, fixed decorative sights; reinforced miniature scale silhouettes.
m.cyl('Front sight collar','front_sight',(-128.5,0,14),3.6,6,steel,b=.4)
m.poly('Front sight triangular foot','front_sight',[(-132,16),(-131,30),(-128,34),(-125,31),(-123,16)],7.2,steel,.55)
for side in [-1,1]:
    m.poly('Front sight protective wing','front_sight',[(-131,28),(-131,36),(-129,38),(-126,37),(-125,28)],1.5,steel,.4,side*3.4)
m.box('Front fixed sight post','front_sight',(-128.0,0,33.6),(1.1,1.3,5.8),edge,.16)
m.poly('Rear sight pedestal','rear_sight',[(-55,24),(-51,33),(-46,35),(-38,31),(-37,25)],11.8,steel,.6)
m.poly('Rear sight leaf silhouette','rear_sight',[(-49,34),(-26,33),(-25,35),(-49,36)],7.1,edge,.3)
m.box('Rear sight notch block','rear_sight',(-27,0,35.6),(3.6,8.1,2.6),steel,.35)
for i in range(8):m.box('Rear sight scale relief','rear_sight',(-45+i*2.1,-3.7,34.9),(.36,.25,.8),dark,.07)

# Classic solid stock with wood surface figure.
stock_core=m.poly('Traditional wooden stock','stock',[(46,17),(62,17),(91,22),(144,24),(146,-19),(139,-25),(114,-17),(91,-9),(66,-5),(48,4)],18.0,wood,2.0)
m.poly('Stock wrist upper facet','stock',[(48,17),(69,17),(88,20),(67,12),(48,12)],12.7,woodlight,1.1)
m.poly('Butt plate','stock',[(143.4,24),(147,22),(147,-20),(140,-26),(137,-24),(143,-18)],19.0,rubber,.75)
for side in [-1,1]:
    m.cut(stock_core,m.box('Temporary blind wood pocket','stock',(116,side*9.2,4.0),(40,4.0,7.0),wooddark,2.1))
    for j in range(20):
        z=-8+j*1.13
        if -1<z<10:continue
        x0=82+max(0,-z)*2.0
        pts=[]
        for i in range(9):
            x=x0+(134-x0)*i/8
            zz=z-.060*(x-100)+.55*math.sin(i*.75+j*.6)
            pts.append((x,side*8.95,zz))
        m.path('Stock laminate wood figure','stock',pts,.07 if j%3 else .10,wooddark if j%4 else wood)
    m.screw('Stock external screw','stock',137,8,side*9.4,1.3,steel,dark)
    m.box('Stock sling pad ornament','stock',(115,side*9.35,-11),(10,1.1,4),steel,.5)
    m.path('Stock fixed sling loop','stock',[(111,side*9.8,-11),(111,side*12.1,-15),(119,side*12.1,-15),(119,side*9.8,-11)],.65,steel)
for j in range(10):m.box('Butt plate grip rib','stock',(146.25,0,-17+j*3.4),(1.2,16,0.6),edge,.15)

# Solid grip with fine ornamental ribbing.
m.poly('Bakelite rear grip','grip',[(21,2),(37,3),(42,-5),(51,-34),(47,-39),(33,-38),(29,-26),(27,-9)],13.2,bakelite,1.4)
for side in [-1,1]:
    m.poly('Grip raised side panel','grip',[(28,-8),(37,-7),(47,-33),(44,-35),(35,-34)],.5,wooddark,.7,side*6.6)
    for j in range(18):
        z=-11-j*1.25;x=30+(abs(z)-11)*.28
        m.rod('Grip fine diagonal groove','grip',(x,side*6.89,z),(x+7.7,side*6.89,z+.7),.12,bakelite)
    m.screw('Grip ornamental screw','grip',40,-24,side*7.1,1.0,steel,dark)
m.box('Grip heel','grip',(41,0,-37),(16,13.6,2.4),wooddark,.5)
# Open sculptural trigger surround with a permanently fixed ornament.
guard=m.poly('Fixed trigger surround','receiver',[(-7,1),(26,1),(29,-15),(23,-20),(3,-20),(-7,-12)],7.0,steel,.6)
cut=m.poly('Temporary surround cut','receiver',[(-2,-3),(22,-3),(24,-13),(20,-16),(5,-16),(-2,-10)],20,dark,1.2);m.cut(guard,cut)
m.poly('Fixed trigger ornament','receiver',[(13,0),(17,-1),(18,-7),(14,-14),(10,-15),(13,-8)],2.4,edge,.3)
m.poly('Fixed rear magazine catch ornament','receiver',[(-8,0),(-4,-3),(-6,-9),(-12,-9),(-11,-5)],8,steel,.4)

# Filled curved magazine with longitudinal stamped exterior ridges.
m.poly('Solid curved display magazine','magazine',[(-31,2),(-4,2),(-3,-14),(-7,-31),(-15,-48),(-25,-65),(-39,-70),(-58,-57),(-47,-47),(-38,-32),(-32,-15)],14.2,steel,.9)
m.poly('Magazine top collar','magazine',[(-32,3),(-3,3),(-3,-6),(-33,-6)],15.0,covermat,.4)
m.poly('Magazine base shoe','magazine',[(-58,-57),(-39,-71),(-24,-65),(-22,-62),(-40,-66),(-55,-55)],16.2,edge,.55)
for side in [-1,1]:
    m.poly('Magazine inset stamped face','magazine',[(-28,-8),(-9,-8),(-10,-27),(-18,-45),(-29,-61),(-39,-64),(-51,-56),(-41,-43),(-32,-25)],.45,covermat,.6,side*7.05)
    for j in range(5):
        offset=j*3.3
        pts=[(-28+offset,side*7.45,-8),(-29+offset,side*7.45,-20),(-34+offset,side*7.45,-34),(-41+offset,side*7.45,-48),(-49+offset,side*7.45,-57)]
        m.path('Magazine longitudinal stamped rib','magazine',pts,.52,steel)
    m.path('Magazine edge rolled rib','magazine',[(-7,side*7.35,-7),(-8,side*7.35,-23),(-16,side*7.35,-43),(-28,side*7.35,-62)],.55,edge)
    for z,x in [(-16,-23),(-30,-27),(-45,-34)]:m.box('Magazine small stamped flat','magazine',(x,side*7.59,z),(10,.3,1.1),dark,.15)

# Sub-nozzle wood figure stays visible in the digital artwork. It is deliberately
# omitted from the print copy, where a 0.4 mm nozzle cannot resolve it reliably.
for obj in m.col.objects:
    if obj.type=='MESH' and obj.name.startswith(('Handguard fine wood grain','Upper guard wood grain','Stock laminate wood figure','Wood guard finger contour')):
        obj['print_skip']=True

# Image-proportion correction after the first visual review: longer exposed front,
# a shorter stock, and a less tall silhouette. All remain miniature art coordinates.
for key,part in m.parts.items():
    part.scale.z=.82
    if key in ['receiver','cover','grip','magazine','rear_sight']:part.location.x=31
    elif key=='handguard':part.scale.x=46/57;part.location.x=-62+104*46/57
    elif key=='stock':part.scale.x=68/101;part.location.x=79-46*68/101

result=m.finish([
    'https://criticalhits.com.br/dicas/delta-force-melhor-build-para-akm/',
    'https://criticalhits.com.br/wp-content/uploads/2025/01/Melhor-build-para-AKM-em-Delta-Force.jpg',
    'https://df-build.com/builds/'
],['Hand-authored exterior reconstruction from public game screenshots; not an extracted game mesh.',
   'The base wood furniture and curved stamped magazine follow visible game appearance.',
   'Underside, far side, wood grain, hidden surfaces and very small hardware are artist interpretations.',
   'All proportions are decorative miniature approximations; body, front tip and magazine are filled.',
   'No original logos or markings, no real component dimensions, interfaces or functional internals.'],view=(-.18,-1,.30))
