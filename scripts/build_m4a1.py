"""Game-picture M4A1 miniature exterior sculpture. No functional gun geometry."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('m4a1',300)
for k,l,v in [('upper','上机匣外观',True),('lower','下机匣与固定护圈',True),('handguard','四面纹路护木外观',True),('barrel','封闭前端',True),('magazine','弧形弹匣外观',True),('grip','握把外观',True),('stock','三角枪托外观',True),('front_sight','前瞄具装饰',True),('rear_sight','后瞄具装饰',True),('optic','可选红点装饰',False)]:s.part(k,l,v)
body=s.mat('Black anodized upper',(.056,.067,.073),.68,.4)
railmat=s.mat('Rail gunmetal',(.078,.084,.085),.72,.45)

# The game default is a long quad-rib handguard and flat top, not a carry handle.
s.cyl('Solid front cylinder','barrel',(-132.0,0,24),3.2,36,body,'X',.28,64)
s.cyl('Capped nose collar','barrel',(-148.3,0,24),3.4,3.4,s.metal,'X',.2)
s.cyl('Sealed front face','barrel',(-149.85,0,24),2.5,.3,s.dark,'X',.03)
for x in [-146.5,-145.6,-144.7,-143.8]:s.cyl('Shallow nose ring relief','barrel',(x,0,24),3.28,.34,s.edge,'X',.05)
s.cyl('Front shoulder','barrel',(-118,0,24),4.2,6,body,'X',.2)

s.poly('Upper closed receiver','upper',[(-25,32),(46,32),(55,28),(57,14),(50,10),(-23,10)],16,body,.9)
s.poly('Upper top ridge','upper',[(-25,33),(-12,33),(-9,36),(5,36),(8,33),(49,33),(54,29),(-25,29)],12,body,.55)
s.poly('Left receiver shallow contour panel','upper',[(-20,27),(43,27),(50,23),(50,17),(3,16),(-19,18)],.45,body,.45,y=-8.05)
s.poly('Left receiver rear angled accent','upper',[(35,26),(43,26),(48,23),(48,19),(41,19),(37,21)],.35,s.metal,.35,y=-8.29)
s.rail('upper',-23,52,35,7.6,3.7)
# Receiver's visible right-side port is a blind layered relief.
s.box('Blind rectangular port border','upper',(13,8.0,25),(30,.6,9),s.dark,.9)
s.box('Closed port face','upper',(13,8.35,25),(27.8,.35,6.5),s.steel,.55)
s.box('Fixed port cover lower lip','upper',(13,8.65,21.3),(29,.8,1.1),body,.22)
s.cyl('Cover hinge cosmetic rod','upper',(13,8.75,20.7),.55,29,s.metal,'X',.1)
s.poly('Receiver angular deflector','upper',[(29,25),(35,29),(39,25),(37,18),(32,18)],4.0,body,.65,y=8.7)
s.cyl('Fixed rear control boss','upper',(45,8.7,24),2.5,4.8,body,'Y',.3)
s.cyl('Rear control button','upper',(45,11.2,24),2.1,.6,s.polymer,'Y',.2)
for sign in [-1,1]:
    s.box('Upper long contour line','upper',(11,sign*8.05,29),(57,.25,.55),s.edge,.1)
    s.box('Rear charging ornament wing','upper',(52,sign*6.4,32),(7,4,2.4),s.metal,.35)
    for z in [31.4,32.1,32.8]:s.box('Charging wing grooves','upper',(53,sign*8.45,z),(3.8,.22,.25),s.edge,.06)

s.poly('Lower receiver closed mass','lower',[(-22,14),(55,14),(57,6),(49,0),(31,-2),(13,-1),(-21,3)],15.2,body,.7)
s.poly('Angled magazine well sculpture','lower',[(-21,6),(8,3),(8,-8),(-22,-5)],16.1,body,.6)
guard=s.poly('Fixed guard silhouette','lower',[(6,6),(40,6),(42,-7),(36,-13),(17,-13),(8,-7)],7.3,body,.9)
s.cut(guard,s.poly('Guard exterior opening','lower',[(12,2),(36,2),(37,-5),(33,-9),(19,-9),(13,-5)],18,s.dark,.85))
s.poly('Fixed trigger ornament','lower',[(24,3),(27,3),(29,-3),(26,-8),(24,-8),(26,-3)],2.8,s.steel,.35)
for sign in [-1,1]:
    s.box('Receiver seam','lower',(13,sign*7.73,12),(64,.2,.4),s.dark,.06)
    for x,z in [(-16,9),(16,5),(40,7),(51,9)]:s.screw('Receiver flush cosmetic pin','lower',x,z,sign*7.72,.85)
    s.cyl('Selector circular relief','lower',(36,sign*8,4),2.15,.7,s.metal,'Y',.15)
    s.line('Fixed selector paddle','lower',(36,sign*8.6,4),(31.5,sign*8.6,1.8),.78,s.metal)
    s.box('Magazine release surface','lower',(-2,sign*8.25,3),(6,1,2),s.steel,.3)
    s.box('Blind emblem plate','lower',(-11,sign*7.87,9),(5,.3,3),s.edge,.35)
    for i in range(4):s.box('Abstract receiver small line','lower',(-10+i*1.6,sign*7.88,6),(.8,.2,.3),s.steel,.06)

# Quad-rib handguard with closed shadow slots. Purely artistic ribs.
s.poly('Solid octagonal handguard','handguard',[(-120,31),(-117,34),(-27,34),(-24,31),(-24,14),(-28,12),(-117,12),(-120,15)],15.8,railmat,.65)
s.rail('handguard',-120,-25,35,7.6,3.7)
s.box('Handguard lower rail base','handguard',(-72,0,12.1),(95,7,1.6),body,.35)
for sign in [-1,1]:
    s.box('Handguard blind side rail bed','handguard',(-72,sign*8.05,23),(92,.9,8.1),s.dark,.45)
    s.box('Handguard side spine','handguard',(-72,sign*8.5,23),(89,1.3,6),railmat,.3)
    for i in range(24):
        x=-116+i*3.7
        s.box('Handguard transverse side rib','handguard',(x,sign*9.03,23),(2.05,2.0,8.6),railmat,.3)
        s.box('Upper blind cooling dash','handguard',(x,sign*7.76,31),(1.8,.7,1.2),s.dark,.2)
        s.box('Lower blind cooling dash','handguard',(x,sign*7.76,14.8),(1.8,.7,1.0),s.dark,.18)
    for x in [-114,-73,-33]:s.screw('Handguard side decorative fastener','handguard',x,23,sign*10.05,1.05)
    for x in [-119,-27]:s.box('Handguard end frame','handguard',(x,sign*8.0,23),(2,2.2,17),body,.3)
for i in range(24):s.box('Bottom rail transverse ridge','handguard',(-116+i*3.7,0,11.5),(2.05,8.4,1.5),railmat,.25)

# Curved black metal magazine silhouette, closed at every end.
s.poly('Curved magazine solid sculpture','magazine',[(-22,-4),(7,-7),(7,-25),(3,-44),(-4,-63),(-32,-56),(-26,-38),(-23,-19)],12.8,s.metal,.8)
s.poly('Magazine capped heel','magazine',[(-33,-55),(-4,-62),(-3,-65),(-34,-58)],14,s.polymer,.6)
for sign in [-1,1]:
    s.poly('Magazine side inset','magazine',[(-20,-11),(4,-13),(3,-28),(-1,-43),(-6,-59),(-28,-54),(-23,-36)],.5,body,.7,y=sign*6.35)
    for j in range(4):
        x=-20+j*5.9
        s.line('Magazine vertical embossed groove','magazine',(x,sign*6.7,-13),(x-1.4,sign*6.7,-31),.44,s.edge)
        s.line('Magazine curved embossed groove','magazine',(x-1.4,sign*6.7,-31),(x-5.4,sign*6.7,-51),.44,s.edge)
    for z,x in [(-14,-8),(-28,-9),(-42,-12)]:s.box('Magazine horizontal seam','magazine',(x,sign*6.73,z),(21,.3,.55),s.dark,.12)

s.poly('Angled polymer grip','grip',[(38,3),(51,1),(56,-10),(67,-39),(52,-43),(41,-21),(36,-4)],14.4,s.polymer,1.2)
for sign in [-1,1]:
    s.poly('Grip stipple panel','grip',[(43,-7),(50,-8),(62,-35),(53,-37),(44,-19)],.45,s.rubber,.6,y=sign*7.17)
    for row in range(12):
        z=-10-row*2.05;x=45+row*.67
        for j in range(4):s.box('Grip small stipple cell','grip',(x+j*1.18,sign*7.43,z),(.62,.34,.7),s.polymer,.12)
    s.screw('Grip base ornamental pin','grip',57,-36,sign*7.28,.7)
s.poly('Grip heel cap','grip',[(51,-40),(66,-37),(68,-41),(52,-45)],14.9,s.rubber,.5)

# Long exposed neck and compact triangular butt as seen in both game views.
s.cyl('Solid stock neck','stock',(73,0,24),5.5,45,body,'X',.35)
s.cyl('Stock neck collar','stock',(57,0,24),6.1,4,s.metal,'X',.2)
s.poly('Stock outer triangular sculpture','stock',[(82,30.4),(147,30.4),(148,-22),(142,-22),(123,-7),(98,1),(83,12)],17.4,s.polymer,1.0)
s.cut(s.col.objects.get('Stock outer triangular sculpture'),s.poly('Stock triangle open silhouette','stock',[(91,12),(142,12),(141,-13),(125,-2),(100,5)],30,s.dark,.8))
s.poly('Stock cheek comb','stock',[(82,31),(145,31),(145,24),(84,24)],18.4,s.polymer,.7)
s.poly('Rubber buttpad','stock',[(146,32),(150,31),(150,-23),(146,-24)],19.0,s.rubber,.8)
s.poly('Stock angled support','stock',[(99,3),(102,7),(142,-13),(143,-19)],9,s.polymer,.6)
for sign in [-1,1]:
    s.box('Stock side longitudinal rail','stock',(114,sign*8.9,18),(57,.6,3.2),body,.35)
    for i in range(6):s.box('Stock side blind vent','stock',(92+i*8.1,sign*9.03,20),(5.2,.4,2),s.dark,.25)
    for x,z in [(96,9),(136,-11)]:s.screw('Stock flush ornament','stock',x,z,sign*8.7,.9)
for i in range(18):s.box('Cheek comb subtle surface texture','stock',(87+i*3.25,0,30.93),(.7,17.1,.26),s.polymer,.08)
for z in range(-20,31,3):s.box('Buttpad rib','stock',(149.6,0,z),(.75,19.3,1.0),s.polymer,.2)

for key,x in [('front_sight',-111),('rear_sight',36)]:
    s.box('Fixed sight foot',key,(x,0,36.7),(7.5,9,3.0),body,.55)
    s.poly('Upright fixed sight silhouette',key,[(x-2.3,37),(x-2.3,49),(x-.9,52),(x+1.7,52),(x+3,47),(x+3,37)],5.6,body,.6)
    s.cyl('Sight blind ring relief',key,(x,-2.9,47.8),2.3,.8,s.edge,'Y',.15)
    s.cyl('Sight dark inset',key,(x,-3.35,47.8),1.2,.2,s.dark,'Y',.02)
    s.cyl('Sight side hinge',key,(x,-4.3,37.8),1.55,1.6,s.steel,'Y',.22)

s.box('Opaque optic foot','optic',(8,0,38.7),(16,10,4),body,.5)
s.poly('Compact solid optic hood','optic',[(1,40),(1,52),(4,56),(13,56),(16,52),(16,40)],10,body,.75)
s.box('Opaque green optic face','optic',(1,-.0,48),(1.1,6.7,10),s.glass,.65)
for sign in [-1,1]:s.screw('Optic cosmetic screw','optic',11,42,sign*5.1,1.0)
s.scene['print_segment_breaks_x_mm']='[-45]'
result=s.finish(['https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops','https://www.imfdb.org/images/thumb/1/1c/DFHO_M4.jpg/600px-DFHO_M4.jpg'],['以实际查看的游戏默认双侧截图为主：长四面纹路护木、平顶机匣、窄露出前端、弧形黑弹匣与带长颈的三角枪托。','截图透视与像素限制下，宽度、倒角、隐藏面及细纹为独立艺术推断；无游戏提取网格或纹理、无品牌标识。','实心微缩外观，无功能内构、膛孔或真实适配接口；网页组件是外观分组。可选红点是艺术化数字配件。'])
