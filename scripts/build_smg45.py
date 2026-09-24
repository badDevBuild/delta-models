"""SMG-45 game exterior miniature with long handguard and triangular brace."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_compact_helpers import finish,optic
s=Sculpture('smg45',230)
for k,l,v in [('receiver','分层机匣实心外壳',True),('handguard','长条浅槽护木',True),('front','封闭短前端',True),('stock','三角镂空后托外观',True),('grip','斜向纹理握把',True),('magazine','细长弧形实心弹匣外观',True),('controls','固定操控与护圈',True),('sights','长顶轨与固定瞄具',True),('optic','可选紧凑光学装饰',False)]:s.part(k,l,v)
s.scene['print_segment_breaks_x_mm']=[-35.0]
# Body and forend are independently profiled rather than derived from AR geometry.
s.poly('Main angular upper receiver','receiver',[(-28,31),(-24,38),(38,38),(43,33),(43,18),(27,16),(18,10),(-7,10),(-16,16),(-28,17)],19.0,s.metal,.75)
s.poly('Upper receiver crown facet','receiver',[(-25,37),(32,39),(41,36),(42,31),(-28,31)],14.8,s.edge,.6)
s.poly('Lower sculpted receiver','receiver',[(-25,20),(37,20),(38,11),(26,8),(17,9),(14,1),(-2,0),(-19,4),(-23,12)],17.5,s.polymer,.75)
for side in [-1,1]:
    s.poly('Receiver blind lower facet','receiver',[(-20,16),(-3,17),(0,13),(-4,3),(-18,6)],.45,s.metal,.35,y=side*8.78)
    s.box('Closed receiver long recess','receiver',(8,side*9.5,29),(43,.25,3.1),s.dark,.75)
    s.box('Inset receiver cover','receiver',(10,side*9.72,26),(27,.45,3.0),s.steel,.6)
    s.poly('Raised rear side cover','receiver',[(23,33),(38,32),(39,22),(28,22)],.7,s.metal,.5,y=side*9.5)
    for x,z in [(-20,22),(34,21),(27,11)]:s.screw('Receiver cosmetic fastener','receiver',x,z,side*(8.65 if z==11 else 9.5),.95)
hand=s.poly('Solid long squared handguard','handguard',[(-101,21),(-101,34),(-96,37),(-27,37),(-25,33),(-26,16),(-94,16)],18.2,s.metal,.65)
for side in [-1,1]:
    for i in range(5):
        x=-91+i*12.0
        s.cut(hand,s.box('Handguard blind horizontal slot','handguard',(x,side*9.03,25),(9.7,1.15,3.1),s.dark,1.2))
        s.box('Handguard recess shadow','handguard',(x,side*8.54,25),(8.6,.2,2.0),s.dark,.7)
    s.poly('Handguard bevel lower strip','handguard',[(-98,20),(-28,20),(-28,17),(-93,17)],.45,s.edge,.3,y=side*8.84)
    s.box('Upper long handguard recessed line','handguard',(-66,side*9.11,32.8),(59,.15,1.1),s.dark,.3)
    for x in [-94,-33]:s.screw('Handguard end screw','handguard',x,29,side*9.13,.72)
s.box('Solid lower handguard lip','handguard',(-64,0,16),(70,13,2.7),s.polymer,.45)
s.cyl('Short closed forward cylinder','front',(-106,0,26.1),4.1,14,s.steel,'X',.25)
s.cyl('Front decorative solid cap','front',(-113.5,0,26.1),4.6,3.0,s.metal,'X',.25)
s.cyl('Opaque front disc','front',(-115.06,0,26.1),2.8,.15,s.dark,'X',.1)
for xx in [-113.8,-112.7]:s.cyl('Front smooth narrow band','front',(xx,0,26.1),4.75,.4,s.metal,'X',.09)
# Long thin curved magazine silhouette is characteristic of the game default.
s.poly('Long magazine solid core','magazine',[(-20,5),(-2,3),(-5,-15),(-9,-35),(-15,-58),(-20,-59),(-29,-55),(-24,-35),(-22,-13)],10.0,s.polymer,.75)
for side in [-1,1]:
    s.poly('Magazine long inset face','magazine',[(-19,0),(-5,-1),(-9,-17),(-14,-36),(-20,-54),(-26,-52),(-21,-31)],.40,s.metal,.3,y=side*5.02)
    for z,x in [(-11,-15),(-30,-18),(-46,-21.5)]:s.box('Magazine transverse shallow seam','magazine',(x,side*5.27,z),(11,.23,.55),s.dark,.15)
s.poly('Magazine broad base shoe','magazine',[(-28,-53),(-17,-56),(-14,-58),(-17,-61),(-31,-57)],11.4,s.metal,.4)
# Sculpted grip and fixed guard are wholly decorative.
s.poly('Rearward sloped grip','grip',[(20,12),(31,12),(32,1),(41,-19),(40,-25),(28,-27),(24,-20),(22,-10),(17,1)],15.0,s.polymer,.9)
for side in [-1,1]:
    s.poly('Grip recessed stipple field','grip',[(23,5),(29,6),(29,0),(38,-20),(36,-23),(29,-23),(26,-14),(22,-4)],.35,s.rubber,.45,y=side*7.5)
    for i in range(9):
        z=2-i*2.5;x=26+max(0,-z)*.26
        s.line('Grip fine raised chevron','grip',(x-2,side*7.74,z),(x+2,side*7.74,z+.65),.22,s.metal)
    s.screw('Grip lower cosmetic pin','grip',33,-20,side*7.68,.78)
guard=s.poly('Fixed round guard silhouette','controls',[(-4,11),(22,12),(24,6),(21,-6),(17,-10),(3,-10),(-4,-5),(-6,2)],6.5,s.metal,.6)
s.cut(guard,s.poly('Guard silhouette gap','controls',[(0,8),(17,8),(20,4),(17,-5),(13,-7),(4,-7),(0,-3)],20,s.dark,.6))
s.poly('Fixed curved trigger ornament','controls',[(11,10),(14,10),(15,5),(14,-2),(10,-5),(8,-4),(11,-1),(12,4)],3,s.polymer,.45)
for side in [-1,1]:
    s.cyl('Fixed receiver selector','controls',(23,side*9.7,17),2.2,.85,s.metal,'Y',.2)
    s.poly('Fixed selector pointer','controls',[(22,17),(21,14),(14,13),(14,14.5),(20,17)],.75,s.steel,.25,y=side*10)
    s.box('Fixed bolt catch face','controls',(-1,side*10.2,23),(3.8,1.7,7),s.steel,.6)
    s.box('Fixed charging handle stalk','controls',(-29,side*11.5,29),(5.5,5.6,2.1),s.metal,.45)
    s.box('Fixed charging handle tip','controls',(-29,side*14.3,29),(6.4,1.9,3.7),s.polymer,.5)
# Open triangle is only an exterior silhouette; rear cuff is a solid block.
s.box('Fixed stock hinge block','stock',(44,0,26),(9,16,19),s.polymer,.65)
s.poly('Brace shoulder transition','stock',[(43,36),(53,34),(62,28),(76,28),(77,22),(52,21),(43,19)],15,s.metal,.6)
stock=s.poly('Triangular brace exterior','stock',[(60,29),(113,29),(113,-5),(104,-5),(62,18),(55,20)],12.5,s.polymer,.75)
s.cut(stock,s.poly('Brace triangle open silhouette','stock',[(70,24),(105,24),(103,1),(72,18)],25,s.dark,.6))
s.box('Solid rear brace pad','stock',(113,0,12),(4,16,36),s.rubber,.7)
for side in [-1,1]:
    s.box('Brace rear wrap band','stock',(105.5,side*6.45,13),(5.4,.9,28),s.rubber,.4)
    s.screw('Brace rear cosmetic screw','stock',104.8,24,side*7.1,.8)
    s.cyl('Fixed hinge cover','stock',(45,side*8.1,26),3.4,.7,s.metal,'Y',.3)
# Default flip-like sights are fixed miniature sculptures.
s.rail('sights',-100,38,37.5,7.8,3.6)
for xx in [-92,25]:
    s.box('Sight foot','sights',(xx,0,40.2),(8,9.3,2.8),s.polymer,.35)
    s.poly('Sight fixed pedestal','sights',[(xx-2,40),(xx-2,46.5),(xx,49),(xx+2,47),(xx+2,40)],3.9,s.metal,.3)
    for side in [-1,1]:s.box('Sight protective wing','sights',(xx,side*2.75,46.2),(2.4,1.7,4.2),s.metal,.25)
optic(s,'optic',-2,40.0,1)
result=finish(s,'https://www.imfdb.org/images/thumb/5/58/DFHO_SMG45.jpg/600px-DFHO_SMG45.jpg',['按游戏默认长护木五段盲槽、细长略弯弹匣和镂空三角支撑托重建；托尾封闭袖口与束带为表面装饰。','护木槽为有底浅凹；机匣口、前端及附件镜片均封闭。前后数字分段选在护木平直段，避开弹匣和握把。'])
