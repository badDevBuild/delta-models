"""M870 miniature exterior art from public game screenshots, not gun components."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('m870',330)
for k,l,v in [('receiver','灰钢机匣外观',True),('stock','木质枪托外观',True),('barrel','封闭长前端',True),('pump','木质泵动护木外观',True),('front_sight','前机械瞄具装饰',True),('rear_sight','后机械瞄具装饰',True),('optic','可选红点装饰',False)]:s.part(k,l,v)
wood=s.mat('Warm walnut base',(.255,.098,.035),.0,.4)
woodlight=s.mat('Walnut light grain',(.335,.151,.062),.0,.45)
wooddark=s.mat('Walnut dark grain',(.132,.039,.015),.0,.5)
receiver=s.mat('Weathered silver grey steel',(.34,.36,.36),.8,.43)

# Game silhouette: long plain front, short lower tube, wood pump.
s.cyl('Capped barrel sculpture','barrel',(-53,0,21),3.7,223,s.metal,'X',.3,64)
s.cyl('Closed muzzle cap','barrel',(-164.5,0,21),3.76,1,s.edge,'X',.16)
s.cyl('Blind muzzle surface','barrel',(-165,0,21),2.7,.18,s.dark,'X',.02)
s.cyl('Solid lower tube exterior','barrel',(8,0,12),3.35,98,s.metal,'X',.22)
s.cyl('Lower tube end ornament','barrel',(-41.8,0,12),4.0,2.0,s.metal,'X',.2)
s.cyl('Lower tube capped face','barrel',(-43.0,0,12),2.4,.4,s.steel,'X',.1)
s.box('Front decorative tube bridge','barrel',(-39,0,16.0),(3.2,5.2,5.5),s.metal,.5)
s.cyl('Barrel rear collar','barrel',(49,0,21),4.4,9,s.metal,'X',.2)

rec=s.poly('Closed receiver sculpture','receiver',[(49,25),(86,25),(96,20),(96,6),(85,3),(55,3),(49,7)],15.6,receiver,1.1)
s.poly('Receiver top facet','receiver',[(49,25),(86,25),(95,20),(93,19),(85,23),(49,23)],14.4,s.steel,.3)
for sign in [-1,1]:
    # Surface-only port relief: sealed metal face, no chamber.
    s.box('Blind side panel border','receiver',(64,sign*7.83,17),(20,.4,7.2),s.dark,.65)
    s.box('Closed side panel face','receiver',(64,sign*8.1,17),(18.8,.4,6.1),s.steel,.55)
    for x in [83.5,92]:s.screw('Receiver pin','receiver',x,8,sign*7.96,.82)
    s.box('Lower receiver seam','receiver',(71,sign*7.88,6),(31,.18,.35),s.dark,.08)
    for i in range(7):s.box('Panel grip notch','receiver',(58+i*1.6,sign*8.33,17),(.25,.12,3.7),s.edge,.05)
    s.box('Receiver blank maker plate','receiver',(83,sign*7.85,19),(7,.14,2.0),s.edge,.2)
guard=s.poly('Fixed guard outer silhouette','receiver',[(72,5),(96,5),(96,-5),(90,-11),(80,-10),(73,-6)],7.2,s.metal,.85)
s.cut(guard,s.poly('Guard negative silhouette','receiver',[(77,2),(92,2),(92,-4),(88,-7),(81,-7),(77,-4)],18,s.dark,.8))
s.poly('Fixed trigger decoration','receiver',[(85,4),(88,4),(89,-2),(87,-6),(84,-6),(86,-2)],2.8,s.steel,.35)
s.cyl('Fixed round guard ornament','receiver',(93,-4.5,1),1.4,1.3,s.metal,'Y',.2)

# Smooth walnut fore-end with long inlaid grip contours.
s.poly('Walnut pump body','pump',[(-37,17),(-32,19),(19,19),(23,17),(23,3),(18,1),(-31,1),(-37,5)],17.7,wood,2.5)
for sign in [-1,1]:
    s.poly('Pump long grip relief','pump',[(-32,13),(-26,15),(15,15),(19,12),(18,6),(-27,6),(-32,8)],.45,wooddark,.7,y=sign*8.75)
    s.poly('Pump contoured wood surface','pump',[(-31,12),(-25,14),(13,14),(17,12),(16,7),(-26,7),(-31,9)],.5,woodlight,.7,y=sign*9.05)
    for z in [8.2,9.8,11.4,13.0]:
        for i in range(9):
            a=-27+i*4.7
            s.line('Pump subtle grain','pump',(a,sign*9.33,z+math.sin(i*.8)*.2),(a+4.5,sign*9.33,z+math.sin((i+1)*.8)*.2),.075,wooddark)
    for x in [-30,18]:s.box('Pump end grip line','pump',(x,sign*8.85,10),(.55,.25,9.8),wooddark,.18)
s.box('Pump underside relief','pump',(-5,0,1.3),(41,11,1.2),wooddark,.55)
for i in range(14):s.box('Pump underside transverse grip','pump',(-29+i*3.6,0,1.2),(.6,11.4,.5),wood,.18)

# Sculpted sporting stock. Non-standard miniature outline from the game image.
s.poly('Walnut butt stock','stock',[(93,20),(104,16),(111,16),(121,21),(158,24),(162,21),(162,-15),(158,-19),(123,-13),(111,-8),(106,-8),(104,-16),(99,-16),(96,-6),(97,6),(93,9)],17.5,wood,2.1)
s.poly('Upper stock comb','stock',[(111,16),(122,21),(157,24),(160,21),(159,19),(123,18),(114,13)],16.8,woodlight,1.2)
s.poly('Black rubber buttpad','stock',[(160,25),(165,24),(165,-19),(160,-21)],19,s.rubber,1.0)
s.poly('Buttpad slim spacer','stock',[(159,24),(161,24),(161,-20),(159,-20)],18.5,s.metal,.35)
for sign in [-1,1]:
    s.poly('Stock wrist dark checkering field','stock',[(99,11),(107,12),(114,9),(110,-4),(105,-10),(101,-9),(102,0)],.48,wooddark,.9,y=sign*8.72)
    for row in range(11):
        z=8-row*1.45;x=102+max(0,5-row)*.35
        for j in range(5):
            xx=x+j*.95
            s.box('Wrist checkered relief','stock',(xx,sign*9.0,z),(0.58,.3,.58),woodlight,.12)
    # Fine wood grain accents follow the butt's contour and remain shallow.
    for j in range(7):
        z=-7+j*3.4
        for i in range(8):
            x=119+i*4.7;z1=z+math.sin(i*.63+j)*.55;z2=z+math.sin((i+1)*.63+j)*.55
            s.line('Butt wood grain relief','stock',(x,sign*8.81,z1),(x+4.6,sign*8.81,z2),.065,woodlight if j%2 else wooddark)
    s.screw('Stock wrist ornamental pin','stock',99,12,sign*8.75,.8)
for z in range(-17,23,3):s.box('Buttpad soft transverse rib','stock',(164.5,0,z),(.75,19.2,1.2),s.polymer,.25)
s.cyl('Rear sling stud ornament','stock',(149,0,-17),1.5,4,s.metal,'Z',.3)
s.box('Rear sling solid loop relief','stock',(149,0,-19.7),(5,6,1.9),s.metal,.6)

# Game front ramp and a short rear sight rail.
s.poly('Front sight protective ramp','front_sight',[(-161,24),(-158,32),(-151,33),(-145,26)],5.1,s.steel,.6)
s.cut(s.col.objects.get('Front sight protective ramp'),s.poly('Front ramp opening','front_sight',[(-157,27),(-156,30),(-152,30),(-149,27)],12,s.dark,.35))
s.box('Front sight fixed bead','front_sight',(-154,0,33),(1.4,1.4,1.5),s.edge,.25)
s.rail('rear_sight',52,81,26.3,6,3.7)
s.box('Rear sight base','rear_sight',(81,0,28.5),(5,7,4.0),s.metal,.45)
for sign in [-1,1]:s.box('Rear sight ear','rear_sight',(81,sign*2,30.6),(2,1.7,3),s.metal,.45)

# Small optional opaque red-dot ornament, separate from the default wood model.
s.box('Optic accessory foot','optic',(66,0,29.4),(15,9,3.4),s.metal,.5)
s.poly('Optic solid hood outline','optic',[(60,30),(60,39),(62,42),(71,42),(73,39),(73,30)],8,s.metal,.65)
s.box('Opaque optic inset','optic',(60,-.01,36),(1.0,5.5,8),s.glass,.55)
for sign in [-1,1]:s.screw('Optic cosmetic screw','optic',68,31,sign*4.7,.8)
# Seat the sight rail on the receiver. This is a closed ornamental contact,
# not a mechanical mounting specification.
for key in ['rear_sight','optic']:
    for obj in s.parts[key].children_recursive:
        obj.location.z -= .8
result=s.finish([
 'https://www.sportskeeda.com/esports/best-m870-build-delta-force',
 'https://staticg.sportskeeda.com/editor/2025/01/08a4c-17373100175601-1920.jpg',
 'https://staticg.sportskeeda.com/editor/2025/01/3ff20-17373100344363-1920.jpg'
],['以已查看的游戏基础木质款截图为主，保留长前端、短下管、木质护木、灰钢机匣和木质枪托。', '截图为透视角度，侧视比例、背面与木纹为艺术推断；未复制游戏纹理或标识。', '所有细节为固定微缩外观装饰，前端实心、侧窗封闭，无内部机构或真实接口。'])
