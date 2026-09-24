"""MDR: short tan bullpup exterior art, based on game catalogue and launch picture."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_compact_helpers import *
s=begin('mdr',280,[('receiver','无托式沙色机身'),('handguard','短梯形浅槽护木'),('front','封闭短前端'),('stock','一体后托与黑色肩垫'),('grip','沙色斜向握把'),('magazine','后置实心方弹匣外观'),('controls','固定控制与护圈'),('sights','顶部短轨与机械瞄具')])
tan=s.mat('Warm sand shell',(.38,.32,.21),.3,.59);light=s.mat('Sand edge facets',(.52,.46,.31),.35,.55)
s.poly('Long angular bullpup upper shell','receiver',[(-43,22),(-48,34),(-40,42),(125,42),(137,35),(135,17),(97,16),(83,7),(55,6),(37,11),(10,14),(-21,17)],24,tan,.8)
s.poly('Receiver broad center ridge','receiver',[(-35,41),(119,43),(130,39),(129,34),(-42,34)],18,light,.65)
for side in [-1,1]:
 s.box('Closed long lateral groove','receiver',(18,side*12,32),(103,.32,2.1),s.dark,.55)
 s.poly('Raised side angled spine','receiver',[(-31,30),(83,30),(96,26),(98,23),(-20,23)],.65,light,.45,y=side*12)
 s.box('Closed rear side panel','receiver',(102,side*12.14,27),(44,.4,5.5),s.metal,.7)
 s.poly('Receiver lower sand facet','receiver',[(44,17),(128,17),(130,11),(115,9),(95,13),(64,10),(48,9)],.65,tan,.45,y=side*11.9)
screws(s,'receiver',[(-33,25),(2,27),(38,27),(72,25),(127,22)],12,.85)
h=s.poly('Solid tapered short forearm','handguard',[(-125,22),(-127,31),(-121,41),(-44,41),(-37,31),(-37,21),(-55,15),(-120,16)],23,tan,.75)
for x in [-115,-98,-81,-64]:slot(s,h,'handguard',x,32,12,3.4,1.4,11.43)
for side in [-1,1]:
 s.poly('Forearm lower bevel line','handguard',[(-121,22),(-47,22),(-47,18),(-119,18)],.45,light,.3,y=side*11.3)
 for x in [-111,-88,-65]:s.box('Forearm upper small blind slot','handguard',(x,side*11.53,37),(12,.2,1.2),s.dark,.35)
 s.screw('Forearm end fastener','handguard',-45,25,side*11.56,.9)
front(s,'front',-140,-121,28,3.3,4.1)
s.poly('Sand integrated rear butt silhouette','stock',[(87,17),(135,21),(137,14),(135,-10),(115,-9),(102,2),(87,6)],24,tan,.95)
s.poly('Sculpted rear angled lower facet','stock',[(106,6),(132,13),(130,-5),(116,-4)],24.2,light,.7)
s.box('Thick black shoulder pad','stock',(138,0,17),(5,27,55),s.rubber,.9)
s.poly('Black top cheek plate','stock',[(58,42),(61,46),(123,46),(128,42),(125,37),(63,37)],21,s.polymer,.65)
for side in [-1,1]:
 s.poly('Rear triangular stipple inlay','stock',[(105,10),(129,14),(128,-2),(119,-3)],.4,s.rubber,.6,y=side*12.1)
 s.line('Rear diagonal surface seam','stock',(106,side*12.36,4),(125,side*12.36,-2),.27,light)
 s.cyl('Rear fixed sling disc','stock',(130,side*12.35,17),2.4,.7,s.metal,'Y',.2)
s.poly('Rear magazine solid slab','magazine',[(52,9),(83,9),(86,-36),(81,-44),(51,-42),(50,-27)],16.5,s.polymer,.85)
for side in [-1,1]:
 for x in [56,65,77]:s.box('Magazine long shallow raised ribs','magazine',(x,side*8.25,-15),(1.1,.5,39),s.metal,.2)
 for z in [-3,-15,-27]:s.box('Magazine transverse recessed line','magazine',(67,side*8.45,z),(28,.25,.7),s.dark,.15)
s.box('Magazine solid bottom shoe','magazine',(68,0,-42),(36,19,4.2),s.metal,.55)
grip(s,'grip',11,16,tan,8.1,.93);guard(s,-9,17,31,21,mat=tan)
for side in [-1,1]:
 s.cyl('Fixed selector disc','controls',(18,side*12.3,22),2.1,.8,s.metal,'Y',.2)
 s.line('Selector fixed pointer','controls',(18,side*12.65,22),(13,side*12.65,20),.8,s.metal)
 s.box('Closed receiver button','controls',(-13,side*12.7,22),(3.7,1.5,4.2),s.steel,.45)
 s.box('Small fixed charging knob','controls',(-51,side*13.1,34),(6.5,4,3),s.metal,.45)
sights(s,-121,127,42.3,7.2);optic(s,-5,45.5,1)
result=finish(s,['https://g.aitags.cn/weapons/mdr','https://g.aitags.cn/wp-content/uploads/2026/09/image.webp','https://clan.fastly.steamstatic.com/images/45050610/3c518e72e534ba43a63e22c31559327db2b66fc7.jpg'],['主体采用资料站基础小图的短前端、沙色整机、后置方匣和沙色握把；官方海报用于侧面层次，不把海报长筒和前握把当作默认配件。','侧槽全部为有底装饰；托身后部纹理、背侧和小五金为缩比艺术推断。'],cut=-28)
