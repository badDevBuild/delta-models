"""AWM miniature exterior artwork; execute through Blender MCP."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('awm',390)
for k,l,v in [('chassis','橄榄绿主体外壳',True),('stock','拇指孔枪托外观',True),('barrel','封闭长前端',True),('receiver','机匣及固定柄外观',True),('magazine','实心弹匣外观',True),('scope','望远瞄具装饰',True),('bipod','装饰支架',False)]:s.part(k,l,v)
olive=s.mat('Olive grey molded shell',(.225,.252,.159),.06,.68)
olive2=s.mat('Molded panel highlight',(.29,.305,.20),.04,.67)

# Long front silhouette, permanently filled; no internal path.
s.cyl('Long tapered barrel sculpture','barrel',(-61,0,21),2.65,144,s.metal,'X',.15,64)
s.cone('Forward barrel taper','barrel',(-142,0,21),3.6,2.65,18,s.metal)
s.cyl('Solid muzzle sleeve','barrel',(-170,0,21),4.1,49,s.metal,'X',.3,64)
s.cyl('Closed muzzle end face','barrel',(-194.7,0,21),3.4,.6,s.dark,'X',.08)
s.cyl('Muzzle edge lip','barrel',(-193.8,0,21),4.22,1.2,s.edge,'X',.12)
for x in [-151,-148,-145]:s.cyl('Front sleeve collar','barrel',(x,0,21),4.25,1.4,s.metal,'X',.15)
s.box('Muzzle sleeve side maker inset','barrel',(-178,-4.02,21),(8,.18,2.4),s.dark,.2)

# Broad front olive shell and underside steps.
s.poly('Front chassis shell','chassis',[(8,20),(76,20),(100,17),(114,10),(114,-8),(99,-12),(92,-5),(71,-5),(69,1),(8,5)],15.5,olive,1.05)
s.poly('Lower contour lip','chassis',[(8,5),(69,1),(71,-5),(95,-5),(99,-12),(109,-8),(111,-4),(100,0),(71,0),(68,6),(8,10)],13.8,olive2,.6)
for sign in [-1,1]:
    s.poly('Long fore-end inset','chassis',[(12,16),(64,16),(64,10),(12,10)],.35,olive2,.25,y=sign*7.75)
    for x in [15,42,65,89,105]:s.screw('Chassis fastener','chassis',x,8 if x<70 else 4,sign*7.95,1.2)
    s.box('Front lower seam','chassis',(39,sign*7.83,7),(49,.2,.42),s.dark,.1)
    # Unbranded molded identification plate, not copied lettering.
    s.box('Blank exterior identification plate','chassis',(87,sign*7.86,12),(18,.23,2.4),s.metal,.25)
    for i in range(4):s.box('Small decorative score','chassis',(81+i*2,sign*8.02,12),(.8,.15,.3),s.edge,.05)
s.box('Front sling tab ornament','chassis',(16,0,4),(8,8,4),s.metal,.6)

# Thumbhole outline; all wall thicknesses are chosen for an inert miniature.
stock=s.poly('Olive thumbhole stock silhouette','stock',[(108,17),(185,17),(191,12),(191,-21),(161,-20),(145,-29),(127,-35),(119,-33),(114,-16),(109,-8)],16.2,olive,1.0)
s.cut(stock,s.poly('Thumbhole silhouette cutter','stock',[(131,11),(143,10),(149,3),(148,-8),(142,-13),(133,-12),(126,-3),(126,5)],24,s.dark,2.2))
s.poly('Raised cheek rest','stock',[(151,20),(181,20),(185,17),(182,14),(149,14),(147,17)],16.4,s.polymer,1.3)
s.poly('Grip sculpted palm surface','stock',[(119,-8),(128,-10),(135,-19),(139,-28),(128,-32),(122,-30)],14.3,olive2,.9)
s.poly('Rubber butt pad','stock',[(187,18),(195,17),(195,-23),(188,-23)],18.0,s.rubber,.9)
s.box('Rear stock spacer','stock',(186,0,-2),(2.2,16.8,37),s.metal,.35)
for sign in [-1,1]:
    s.poly('Rear stock panel relief','stock',[(151,12),(183,12),(183,-12),(158,-12),(149,-18),(146,-12),(151,-4)],.45,olive2,.45,y=sign*8.12)
    for x,z in [(119,12),(155,10),(179,10),(178,-13),(127,-25)]:s.screw('Stock fastener','stock',x,z,sign*8.4,1.15)
    s.cyl('Stock adjustment dial','stock',(179,sign*8.5,-17),2.2,1.25,s.metal,'Y',.2)
    s.box('Cheek underside trim','stock',(166,sign*8.3,14),(32,.5,.9),s.dark,.15)
for z in range(-19,15,3):s.box('Butt pad rib','stock',(194.6,0,z),(.75,18.2,1.15),s.polymer,.22)
s.cyl('Fixed monopod collar decoration','stock',(180,0,-22.5),3.1,6,s.metal,'Z',.25)
for z in [-24.8,-23.4,-22]:s.cyl('Monopod external groove','stock',(180,0,z),3.25,.45,s.edge,'Z',.1)

# Closed receiver exterior and fixed ornamental bolt handle.
s.cyl('Solid receiver top','receiver',(65,0,21),4.6,105,s.metal,'X',.3)
s.box('Receiver lower spine','receiver',(66,0,17),(105,10,5),s.metal,.4)
s.rail('receiver',12,116,25,5.6,4.4)
s.box('Sealed receiver side window','receiver',(87,-4.7,22),(24,.32,3.5),s.dark,.65)
s.box('Closed side window face','receiver',(87,-4.9,22),(19,.22,2.7),s.steel,.45)
s.cyl('Fixed handle root','receiver',(112,-4.9,22),2.25,2.3,s.metal,'Y',.15)
s.line('Fixed exterior handle stem','receiver',(112,-5,22),(116,-11,13),1.3,s.metal)
s.cyl('Fixed handle knob','receiver',(116,-12.2,12),3.1,5,s.polymer,'Y',.8)
for i in range(6):s.cyl('Handle knob grip relief','receiver',(116,-10.4-i*.6,12),3.15,.2,s.metal,'Y',.06)
s.box('Buried solid sculpture guard bridge','receiver',(111,0,7),(7,6,20),s.metal,.4)
guard=s.poly('Trigger guard outer ornament','receiver',[(94,-1),(119,-1),(120,-20),(115,-26),(97,-26),(93,-19)],6.2,s.metal,.8)
s.cut(guard,s.poly('Open exterior trigger guard','receiver',[(98,-7),(114,-7),(116,-19),(112,-22),(99,-22),(96,-18)],15,s.dark,.7))
s.poly('Permanently fixed trigger decoration','receiver',[(107,-1),(111,-1),(112,-14),(107,-21),(104,-21),(108,-14)],2.8,s.steel,.4)

s.poly('Solid magazine exterior','magazine',[(71,-4),(95,-4),(95,-17),(91,-19),(73,-18)],11.7,s.metal,.65)
s.box('Magazine base rim','magazine',(83,0,-18),(25,12.5,2),s.polymer,.45)
for sign in [-1,1]:
    s.box('Magazine panel inset','magazine',(83,sign*5.94,-11),(16,.25,8),s.dark,.5)
    for x in [77,89]:s.box('Magazine vertical rib','magazine',(x,sign*6.12,-11),(1,.55,9),s.metal,.2)

# Opaque optical sculpture, no usable lens channel.
s.cyl('Scope tube solid','scope',(65,0,42),4.4,56,s.metal,'X',.25)
s.cone('Scope objective flare','scope',(30,0,42),8.1,4.4,26,s.metal)
s.cyl('Scope front hood','scope',(12,0,42),8.1,11,s.polymer,'X',.35)
s.cyl('Scope objective opaque glass','scope',(6.3,0,42),6.7,.6,s.glass,'X',.05)
s.cyl('Scope objective protective rim','scope',(6.6,0,42),8.2,1,s.metal,'X',.12)
s.cyl('Scope ocular housing','scope',(103,0,42),6.0,25,s.polymer,'X',.4)
s.cyl('Scope rear lens closed surface','scope',(115.7,0,42),4.8,.3,s.glass,'X',.06)
for x in [89,93,107,111]:s.cyl('Scope ring ridge','scope',(x,0,42),6.15,1.1,s.metal,'X',.16)
for x in [45,79]:
    s.box('Scope pedestal solid foot','scope',(x,0,29.8),(7,10.5,6.8),s.metal,.4)
    s.cyl('Scope exterior mount ring','scope',(x,0,42),5.7,5.0,s.metal,'X',.3)
    s.box('Scope ring bridge','scope',(x,0,34),(5,10.6,6),s.metal,.35)
    for sign in [-1,1]:s.screw('Scope ring fastener','scope',x,35,sign*5.1,.8)
s.cyl('Scope elevation housing','scope',(66,0,48),4.8,5,s.metal,'Z',.25)
s.cyl('Scope elevation dial','scope',(66,0,51.5),5.1,2.6,s.polymer,'Z',.2)
s.cyl('Scope windage housing','scope',(66,-5.1,42),4.2,4.2,s.metal,'Y',.2)
s.cyl('Scope windage cap','scope',(66,-7.4,42),4.4,1.2,s.polymer,'Y',.2)
for i in range(32):
    a=i*math.tau/32
    s.box('Elevation dial knurl','scope',(66+5*math.cos(a),5*math.sin(a),51.5),(.43,.43,2.0),s.metal,.08)
    s.line('Windage dial tick','scope',(66+3.8*math.cos(a),-8.02,42+3.8*math.sin(a)),(66+4.1*math.cos(a),-8.02,42+4.1*math.sin(a)),.08,s.edge)
for i in range(13):s.box('Optic zoom marker','scope',(99+i*.6,-5.96,42),(.23,.15,.9 if i%3 else 1.5),s.edge,.04)

# Optional decorative support, non-articulated and no standard mounting interface.
s.box('Support sculpted connector','bipod',(20,0,1),(9,11,5),s.metal,.6)
for sign in [-1,1]:
    s.cyl('Support ornamental hinge','bipod',(20,sign*5,-1),3.4,3.2,s.metal,'Y',.3)
    s.line('Support leg upper','bipod',(20,sign*6,-1),(10,sign*17,-24),1.9,s.metal)
    s.line('Support leg lower','bipod',(10,sign*17,-24),(7,sign*21,-34),1.5,s.steel)
    for i in range(7):
        q=i/8;s.cyl('Support collar detail','bipod',(20-10*q,sign*(6+11*q),-1-23*q),2.05,.65,s.polymer,'Z',.1)
    s.box('Support foot','bipod',(7,sign*21,-35),(6,4,2.8),s.rubber,.6)
result=s.finish([
 'https://0xzx.com/2025030900175343137.html',
 'https://0xzx.com/wp-content/uploads/i0.wp.com/gamingonphone.com/wp-content/uploads/2025/02/IMG_7327.jpg',
 'https://www.sportskeeda.com/esports/best-awm-build-delta-force',
 'https://staticg.sportskeeda.com/editor/2025/01/049b0-17367045609664-1920.jpg'
],['基础截图低分辨率，按长前端、橄榄灰绿拇指孔托、望远瞄具轮廓重新绘制。', '右侧、顶部与底部细节为对称或艺术推断；瞄具采用参考可见外观的近似组合。', '支架为单独可选装饰，所有机械细节固定且封闭；无真实尺寸、真实接口或内部结构。'])
