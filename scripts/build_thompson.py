"""Thompson game reference: fixed walnut furniture and straight magazine exterior."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch3_smg_helpers import Sculpture,wood,optic,guard,closed_front,finish
s=Sculpture('thompson',280)
for k,l,v in [('receiver','平直金属机匣外观',True),('handguard','水平木制护木',True),('stock','固定木制枪托',True),('grip','木握把及固定护圈',True),('magazine','直形实心弹匣',True),('muzzle','封闭细前端',True),('sights','固定机械瞄具',True),('optic','可选数字微型瞄具',False)]:s.part(k,l,v)
w=wood(s);m=s.mat('Thompson charcoal steel',(.049,.057,.061),.7,.42)
s.scene['print_segment_breaks_x_mm']=[-17]
# Long horizontal receiver and smaller stepped lower housing.
s.box('Long rectangular solid receiver','receiver',(26,0,16.6),(99,12.5,13),m,.65)
s.box('Receiver narrow top ridge','receiver',(25,0,23),(102,8.8,1.8),m,.45)
s.poly('Stepped lower housing','receiver',[(-18,12),(75,12),(75,7),(57,7),(49,2),(16,2),(8,8),(-18,8)],12,m,.55)
for sign in [-1,1]:
    s.box('Receiver subtle long pressed seam','receiver',(25,sign*6.32,19),(94,.25,.7),s.edge,.18)
    s.box('Upper long side inset panel','receiver',(29,sign*6.31,15),(86,.3,4.5),m,.4)
    s.box('Blind short receiver side recess','receiver',(3,sign*6.54,16),(26,.25,2.3),s.dark,.4)
    s.box('Filled receiver recess lower line','receiver',(4,sign*6.7,15),(23,.2,.54),s.edge,.16)
    for x,z in [(18,9),(34,9),(54,10),(68,15)]:s.screw('Cosmetic receiver blind rivet','receiver',x,z,sign*6.28,.65)
    for i in range(11):s.box('Abstract worn receiver lettering','receiver',(22+i*1.25,sign*6.59,14),(.68,.12,.25),s.edge,.05)
    s.cyl('Fixed control round ornament','receiver',(30,sign*6.32,6),1.35,.5,m,'Y',.15)
    s.poly('Fixed control short paddle','receiver',[(30,6),(33,5),(34,3),(31,3)],.5,m,.3,y=sign*6.64)
# Closed barrel artwork and flat-ended horizontal wooden foreguard observed in screenshot.
closed_front(s,'muzzle',-140,-20,14,2.2)
s.cyl('Forward decorative shoulder','muzzle',(-27,0,14),3.4,15,m,'X',.4)
for x in [-42,-39,-36,-33]:s.cyl('Front surface shallow ornamental band','muzzle',(x,0,14),2.65,.5,m,'X',.1)
s.poly('Rounded horizontal wooden foreguard','handguard',[(-94,11),(-20,11),(-17,8),(-19,-1),(-24,-3),(-90,-3),(-94,0)],15.8,w,1.65)
s.box('Wood foreguard thin upper metal strip','handguard',(-55,0,10.9),(73,8.5,1.3),m,.4)
for sign in [-1,1]:
    for x in [-88,-24]:s.screw('Wood foreguard recessed ornamental screw','handguard',x,3.4,sign*7.92,.72)
    s.poly('Wood foreguard molded lower edge','handguard',[(-88,-.5),(-24,-.5),(-22,1),(-89,1)],.3,w,.5,y=sign*7.65)
# Broad fixed stock with downward heel, a solid wooden art form.
s.poly('Fixed walnut stock silhouette','stock',[(64,10),(78,10),(88,14),(96,15),(109,12),(135,8),(139,5),(140,-22),(137,-26),(130,-27),(118,-22),(102,-12),(91,-5),(77,-2),(64,1)],17.0,w,2.0)
s.poly('Stock metal heel cap','stock',[(137,7),(140,5),(140,-23),(137,-26)],17.4,m,.7)
for sign in [-1,1]:
    s.box('Stock closed sling plate','stock',(112,sign*8.5,-11),(10,.4,2.4),m,.55)
    for x in [108,116]:s.screw('Stock small sling plate studs','stock',x,-11,sign*8.72,.48)
# Traditional curved wooden grip, fixed exterior guard, long straight magazine.
s.poly('Wooden grip solid silhouette','grip',[(39,4),(49,5),(53,0),(53,-8),(58,-14),(63,-25),(63,-30),(59,-35),(53,-35),(51,-31),(50,-23),(46,-18),(42,-15),(43,-11),(42,-6),(37,-2)],14.3,w,1.05)
for sign in [-1,1]:
    s.poly('Grip slightly inset walnut panel','grip',[(43,-5),(48,-4),(48,-12),(53,-19),(59,-28),(57,-32),(55,-31),(54,-24),(49,-19),(45,-15)],.36,w,.6,y=sign*7.0)
    s.screw('Grip fixed cosmetic wood screw','grip',50,-16,sign*7.17,.75)
guard(s,[(11,5),(42,5),(45,-2),(44,-12),(39,-17),(18,-17),(13,-13)],[(15,2),(39,2),(41,-3),(40,-11),(37,-14),(20,-14),(16,-11)])
s.poly('Fixed ornamental trigger','grip',[(29,4),(32,3),(32,-4),(28,-10),(25,-11),(26,-8),(29,-3)],2.7,m,.4)
s.box('Solid straight box magazine','magazine',(5,0,-13),(12.2,10.3,52),m,.65)
s.box('Magazine top ornamental collar','magazine',(5,0,7.4),(14.2,12,3),m,.45)
s.box('Magazine bottom cap','magazine',(5,0,-39),(13.1,11.3,2.2),m,.45)
for sign in [-1,1]:
    s.box('Magazine shallow broad inset','magazine',(5,sign*5.17,-14),(8,.23,40),s.dark,.4)
    for x in [1.8,8.2]:s.box('Magazine longitudinal folded edge','magazine',(x,sign*5.36,-14),(.85,.5,40),s.edge,.23)
    for z in [-3,-12,-21,-30]:s.cyl('Magazine small blind witness dot','magazine',(5,sign*5.37,z),.52,.17,m,'Y',.05,20)
# Distinct small fixed front sight and protected rear open exterior notch.
s.box('Front sight collar art','sights',(-128,0,15.8),(5.6,5.8,4),m,.4)
s.poly('Fixed front blade','sights',[(-130,16),(-126,16),(-127,24),(-129,24)],2.6,m,.3)
s.box('Rear sight broad foot','sights',(65,0,24.4),(15,10,2.7),m,.45)
for sign in [-1,1]:s.poly('Rear fixed protective wing','sights',[(60,25),(71,25),(71,30),(68,31),(60,27)],1.5,m,.3,y=sign*3.6)
s.box('Rear fixed notch base','sights',(67,0,27),(3,6.7,3),m,.3)
optic(s,23,24)
result=finish(s,'实际查看游戏默认图：细长平直金属机匣、细前端、水平木护木、直弹匣、棕色木握把与下垂固定木枪托；保留该默认配置，而非鼓匣或垂直前握把。','https://zilliongamer.com/uploads/delta-force/weapons-builds/submachine-gun/thompson/thompson-delta-force-build.jpg')
