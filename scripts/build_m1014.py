"""Game default M1014 traditional-stock exterior sculpture; entirely inert."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch3_mixed_helpers import finish
s=Sculpture('m1014',300)
for key,label,show in [('receiver','封闭机匣外观',True),('stock','黑色弯颈固定枪托',True),('handguard','黑色长护木',True),('barrel','封闭长前端',True),('lower_tube','下方实心管状装饰',True),('guard','固定护圈与铜色装饰',True),('sights','机械瞄具与短上轨',True),('optic','可选小型瞄具',False)]:s.part(key,label,show)
body=s.mat('Worn graphite steel',(.115,.13,.135),.66,.43)
poly=s.mat('Matte synthetic stock',(.043,.052,.059),0,.66)
grip=s.mat('Synthetic shallow relief',(.068,.078,.083),0,.72)
bronze=s.mat('Bronze fixed decoration',(.29,.19,.083),.67,.43)
s.scene['print_segment_breaks_x_mm']='[0]'
# Sealed rectangular receiver with the distinct angled back of the game default.
s.poly('Closed receiver sculpture','receiver',[(-25,24),(28,24),(36,20),(45,16),(44,6),(25,3),(-21,3),(-25,6)],17.0,body,1.0)
s.poly('Receiver top long bevel','receiver',[(-25,24),(28,24),(35,20),(32,19),(27,22),(-25,22)],16.3,s.edge,.35)
for side in [-1,1]:
    s.box('Receiver lower edge seam','receiver',(7,side*8.52,5.3),(59,.3,.7),s.dark,.15)
    s.screw('Receiver small front pin','receiver',-16,9,side*8.53,.75)
    s.screw('Receiver small rear pin','receiver',34,11,side*8.53,.78)
    s.box('Blank side label relief','receiver',(9,side*8.59,15),(12,.2,2.5),body,.25)
s.box('Sealed side port border','receiver',(-9,8.59,18),(24,.35,7),s.dark,.5)
s.box('Sealed side port steel face','receiver',(-9,8.82,18),(21,.35,5.1),s.steel,.4)
for x in [-16,-12,-8,-4]:s.box('Closed shutter decoration slot','receiver',(x,9.02,18),(1.3,.15,2.5),s.dark,.3)
s.cyl('Fixed side handle ornament','receiver',(0,11.4,16),1.7,5.7,s.metal,'Y',.3)
s.box('Fixed side button plate','receiver',(11,8.83,9),(5.7,.8,5),s.metal,.5)
s.cyl('Fixed side button','receiver',(11,9.8,9),1.6,1.8,s.steel,'Y',.23)
# Continuous curved sporting wrist and full black butt. No separate pistol grip.
s.poly('Traditional synthetic buttstock','stock',[(41,19),(48,16),(58,11),(67,7),(70,8),(74,13),(81,16),(143,10),(148,7),(148,-30),(144,-32),(86,-15),(78,-12),(70,-11),(64,-7),(61,-4),(57,3),(43,7)],18.5,poly,1.7)
s.poly('Stock raised comb','stock',[(77,15),(82,17),(140,12),(145,9),(144,7),(83,13)],17.8,grip,.75)
s.poly('Rubber full buttpad','stock',[(147,11),(150,10),(150,-33),(147,-34)],20,s.rubber,.75)
s.poly('Buttpad spacer','stock',[(145.8,10),(147.8,10),(147.8,-32),(145.8,-32)],19.5,s.metal,.35)
for side in [-1,1]:
    s.poly('Stock side long inset','stock',[(83,9),(137,4),(140,-24),(85,-10)],.3,grip,.65,y=side*9.24)
    s.poly('Stock black sling recess','stock',[(112,2),(124,1),(124,-6),(112,-5)],.38,s.dark,.5,y=side*9.43)
    s.box('Stock solid sling inset face','stock',(118,side*9.67,-2),(9.1,.25,4.2),poly,.4)
    for i in range(9):
        z=-3+i*.9;x=64+i*.36
        s.box('Wrist shallow diagonal grip relief','stock',(x,side*9.25,z),(.45,.26,1.25),grip,.12)
for z in range(-31,10,3):s.box('Buttpad molded ridges','stock',(149.5,0,z),(.8,20.1,.8),poly,.2)
# Fore-end is broad, smooth, and vertically inset as in the game picture.
s.poly('Long polymer handguard','handguard',[(-93,16),(-90,20),(-27,20),(-22,15),(-22,4),(-27,1),(-87,1),(-93,4)],18.4,poly,1.4)
for side in [-1,1]:
    s.poly('Handguard long grip field','handguard',[(-87,15),(-31,15),(-27,12),(-28,5),(-87,5)],.45,grip,.65,y=side*9.16)
    for i in range(15):s.box('Fore-end shallow molded grip','handguard',(-85+i*3.8,side*9.43,9),(.55,.26,6.8),poly,.18)
    s.box('Handguard long upper seam','handguard',(-58,side*9.24,17),(58,.25,.6),s.dark,.18)
for xx in [-93,-22]:s.box('Fore-end end collar','handguard',(xx,0,10),(2.7,18.8,16.2),s.metal,.55)
# Fully capped dual front silhouette, with connected bands and cosmetic flutes.
s.cyl('Solid upper barrel sculpture','barrel',(-87,0,24),3.6,126,s.metal,'X',.23,64)
s.cyl('Closed upper muzzle face','barrel',(-150.05,0,24),2.5,.18,s.dark,'X',.03)
s.box('Fictional upper barrel rib','barrel',(-81,0,27.1),(102,3.5,1.6),s.edge,.25)
for x in [-134,-126,-117,-107,-96,-85,-74,-63,-52,-41,-30]:s.box('Rib short dividing seam','barrel',(x,0,27.9),(.3,3.1,.15),s.dark,.03)
s.cyl('Solid lower parallel tube','lower_tube',(-82,0,14.3),3.4,123,s.metal,'X',.25)
s.cyl('Solid lower tube end cap','lower_tube',(-144,0,14.3),3.8,3.7,s.edge,'X',.25)
s.cyl('Lower tube closed face','lower_tube',(-145.92,0,14.3),2.8,.15,s.dark,'X',.03)
for side in [-1,1]:
    for z in [13.3,15.5]:s.box('Lower tube shallow longitudinal flute','lower_tube',(-120,side*3.1,z),(37,.45,.45),s.edge,.18)
s.box('Front tube sculptural connecting band','lower_tube',(-135,0,19.0),(5.2,7.8,13.8),s.metal,.7)
s.box('Rear tube hidden artistic connection','lower_tube',(-91,0,19),(4,6.0,11),s.metal,.5)
guard=s.poly('Fixed bronze-accent guard','guard',[(15,6),(40,6),(41,-3),(37,-10),(24,-10),(17,-5)],6.6,s.metal,.75)
s.cut(guard,s.poly('Guard external opening','guard',[(20,3),(36,3),(37,-2),(34,-6),(25,-6),(21,-3)],16,s.dark,.5))
s.poly('Fixed copper trigger ornament','guard',[(29,5),(32,5),(33,0),(30,-5),(27,-5),(29,-1)],2.8,bronze,.35)
s.cyl('Fixed guard rear ornament','guard',(37,-4,3),1.4,2.5,s.metal,'Y',.2)
# Reference-default small rail and fixed ramp sights.
s.rail('sights',-24,22,24.45,6.0,3.4)
s.box('Rear sight ramp seat','sights',(24,0,25.35),(10,8,3),s.metal,.45)
s.poly('Rear sight broad ramp','sights',[(19,26.35),(22,30.35),(28,30.35),(31,26.35)],7.2,s.metal,.45)
s.box('Rear sight sealed inset','sights',(26,0,30.35),(2.5,4.2,.3),s.dark,.15)
s.poly('Front sight protective ramp','sights',[(-138,27),(-136,33),(-129,33),(-126,27)],5.7,s.metal,.5)
s.box('Front fixed red inlay','sights',(-132,0,33.4),(3.2,1.1,.9),s.mat('Red opaque sight inlay',(.35,.014,.009),.1,.45),.2)
# Opaque optional red dot, fully seated on the arbitrary decorative rail.
s.box('Optic ornamental base','optic',(-6,0,28.1),(14,8,3.0),s.metal,.45)
s.poly('Optic short hood','optic',[(-12,29),(-12,36),(-10,39),(-1,39),(1,36),(1,29)],7.3,s.metal,.65)
s.box('Optic opaque front panel','optic',(-12.1,0,34),(0.4,5.2,6.6),s.glass,.4)
for side in [-1,1]:s.screw('Optic small side fastener','optic',-5,30,side*4.1,.68)
for obj in s.parts['optic'].children_recursive:obj.location.z-=.65
result=finish(s,'https://www.imfdb.org/images/thumb/1/1c/DFHO_M4S90.jpg/600px-DFHO_M4S90.jpg',['以游戏默认传统黑色固定整托为主，保留弯颈、长双管轮廓、护木、上方窄筋与短上轨；未误用带手枪握把的改装款。','右侧窗采用封闭浅浮雕，铜色操控饰件固定；可选短瞄具为数字艺术附件。'])
