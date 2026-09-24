"""SCAR-H game-reference miniature sculpture; solid exterior, no real interfaces."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('scarh',300)
for k,l,v in [('upper','长矩形上机匣外观',True),('lower','下机匣与固定护圈',True),('handguard','短护木外观',True),('barrel','封闭长前端',True),('magazine','直身弹匣外观',True),('grip','握把外观',True),('stock','厚枪托外观',True),('front_sight','前瞄具装饰',True),('rear_sight','后瞄具装饰',True),('optic','可选紧凑瞄具装饰',False)]:s.part(k,l,v)
body=s.mat('Charcoal grey alloy',(.09,.099,.1),.7,.42)
lower=s.mat('Cool charcoal polymer',(.066,.077,.079),.12,.65)
stockmat=s.mat('Dark grey stock polymer',(.082,.09,.09),.03,.62)

# Default game reference has a long plain front and no projecting muzzle brake.
s.cyl('Solid long front sculpture','barrel',(-112,0,22),2.85,76,body,'X',.22,64)
s.cyl('Front sealed disc','barrel',(-149.8,0,22),2.9,.4,s.metal,'X',.1)
s.cyl('Blind front inset','barrel',(-150,0,22),2.0,.12,s.dark,'X',.03)
s.cyl('Front thicker shoulder','barrel',(-85,0,22),3.4,19,s.metal,'X',.18)
s.cyl('Front block collar','barrel',(-76,0,22),4.1,4.2,body,'X',.25)

# Long flat rectangular alloy upper is the key distinctive profile.
s.poly('Long closed upper receiver','upper',[(-75,32),(64,32),(68,28),(68,8),(61,4),(-71,4),(-76,8)],17.2,body,.95)
s.poly('Upper chamfer band','upper',[(-75,30),(66,30),(68,27),(-76,27)],16.2,s.edge,.4)
s.rail('upper',-73,66,32.3,7.8,3.8)
for sign in [-1,1]:
    s.box('Upper recessed long channel border','upper',(-2,sign*8.57,23.8),(113,.55,3.2),s.dark,.5)
    s.box('Closed channel inner metallic surface','upper',(-1,sign*8.86,23.7),(110,.22,1.5),s.metal,.25)
    s.box('Upper thin seam','upper',(1,sign*8.62,13.3),(123,.25,.5),s.dark,.08)
    s.poly('Upper lower front bevel detail','upper',[(-72,7),(-42,7),(-37,10),(-23,10),(-20,8),(57,8),(61,5),(-71,5)],.35,s.edge,.15,y=sign*8.55)
    for x,z in [(-65,11),(-28,11),(17,10),(55,11),(63,23)]:s.screw('Upper countersunk ornament','upper',x,z,sign*8.68,1.05)
    for i in range(9):s.box('Top rail interrupted flat indicator','upper',(-66+i*14.5,sign*4.9,33.9),(1.2,.7,.8),s.edge,.15)
# Distinctive short exposed handle is fixed and sealed against the body.
s.cyl('Fixed side handle stem','upper',(-30,-10.1,23.5),1.55,5.8,s.metal,'Y',.2)
s.poly('Fixed side handle paddle','upper',[(-32,26),(-25,25),(-24,22),(-31,21)],3.7,s.metal,.55,y=-12.5)
for i in range(4):s.box('Handle finger relief','upper',(-29.9+i*1.35,-14.3,23.3),(.5,.3,2.2),s.edge,.1)
s.box('Blind opposite port shadow','upper',(9,8.95,18.6),(37,.35,6),s.dark,.55)
s.box('Sealed opposite port plate','upper',(9,9.18,18.5),(35,.25,4.5),s.steel,.4)

# Short fore-end, side transverse grip ribs and shallow circular recesses.
s.poly('Short handguard shell','handguard',[(-76,23),(-27,23),(-22,19),(-22,7),(-29,4),(-73,4),(-77,8)],18.6,body,.75)
s.box('Handguard underside spine','handguard',(-50,0,4.4),(52,8.2,2),s.metal,.35)
for sign in [-1,1]:
    s.box('Handguard side rail shadow bed','handguard',(-51,sign*9.3,13.0),(45,.8,8.2),s.dark,.5)
    s.box('Handguard side rail solid bed','handguard',(-51,sign*9.75,13),(43,1.0,6.2),s.metal,.35)
    for i in range(12):
        x=-72+i*3.75
        s.box('Short handguard transverse rib','handguard',(x,sign*10.15,13),(2.3,1.55,8.4),body,.3)
        s.cyl('Blind handguard upper recess','handguard',(x,sign*8.88,28),.65,.25,s.dark,'Y',.07,20)
    for x in [-72,-31]:s.screw('Handguard outer ornament','handguard',x,13,sign*10.85,.95)
    s.box('Front handguard end rim','handguard',(-76,sign*9.2,13),(2,1.7,17),body,.4)
for i in range(13):s.box('Handguard bottom rib','handguard',(-74+i*3.8,0,3.7),(2.3,9.6,1.6),body,.25)

s.poly('Lower closed receiver body','lower',[(-18,9),(64,9),(66,0),(56,-5),(36,-7),(10,-7),(-19,-2)],16.0,lower,.85)
s.poly('Angled magazine well','lower',[(-20,1),(9,-5),(9,-15),(-21,-9)],16.5,lower,.7)
guard=s.poly('Squared fixed guard silhouette','lower',[(7,-2),(42,-2),(43,-15),(36,-21),(20,-20),(10,-15)],7.5,lower,.95)
s.cut(guard,s.poly('Guard open silhouette','lower',[(13,-5),(36,-5),(38,-13),(33,-17),(21,-16),(15,-12)],20,s.dark,.8))
s.poly('Fixed trigger decoration','lower',[(25,-4),(28,-4),(30,-10),(28,-16),(25,-15),(27,-10)],2.8,s.steel,.35)
for sign in [-1,1]:
    s.cyl('Selector low relief','lower',(49,sign*8.2,0),2.4,.65,s.metal,'Y',.15)
    s.line('Selector fixed paddle','lower',(49,sign*8.6,0),(46,sign*8.6,-3),.75,s.metal)
    s.cyl('Rear receiver round cosmetic pin','lower',(61,sign*8.3,1.8),1.85,.65,body,'Y',.15)
    s.box('Magazine release surface plate','lower',(5,sign*8.35,-1),(8,1.1,3.8),body,.4)
    s.box('Fixed receiver control ornament','lower',(14,sign*8.4,4),(4.1,1.3,3.3),s.metal,.4)
    for x,z in [(-14,3),(27,3),(40,-3)]:s.screw('Lower receiver small ornamental pin','lower',x,z,sign*8.1,.83)
    s.box('Plain receiver identity plaque','lower',(31,sign*8.02,4),(9,.2,2.3),body,.25)
    for i in range(5):s.box('Abstract plaque line','lower',(28+i*1.4,sign*8.22,4),(.7,.15,.6),s.edge,.05)

# Dark box magazine: much shorter and straighter than the M4A1 silhouette.
s.poly('Straight magazine solid body','magazine',[(-20,-7),(8,-13),(7,-47),(-19,-44)],12.8,s.metal,.65)
s.poly('Magazine closed heel','magazine',[(-20,-42),(8,-45),(9,-49),(-21,-46)],14.2,s.polymer,.5)
for sign in [-1,1]:
    s.poly('Magazine flat side panel','magazine',[(-18,-13),(5,-17),(4,-44),(-17,-42)],.4,lower,.35,y=sign*6.37)
    for i in range(5):
        x=-16+i*4.4
        s.line('Magazine vertical pressed rib','magazine',(x,sign*6.7,-18),(x,sign*6.7,-40),.36,s.edge)
    s.line('Magazine upper side seam','magazine',(-17,sign*6.7,-15),(5,sign*6.7,-19),.32,s.dark)
    s.line('Magazine heel side seam','magazine',(-18,sign*6.7,-41),(4,sign*6.7,-44),.28,s.dark)

s.poly('Angled grip solid silhouette','grip',[(39,-3),(51,-4),(54,-14),(66,-42),(52,-45),(41,-26),(35,-10)],14.2,s.polymer,1.05)
s.poly('Grip closed heel','grip',[(50,-43),(65,-40),(67,-44),(51,-47)],14.7,s.rubber,.6)
for sign in [-1,1]:
    s.poly('Grip rough panel','grip',[(41,-13),(50,-14),(61,-39),(53,-40),(44,-27)],.5,s.rubber,.55,y=sign*7.1)
    for row in range(12):
        z=-16-row*1.8;x=44+row*.7
        for j in range(4):s.box('Grip fine stipple cell','grip',(x+j*1.18,sign*7.39,z),(.63,.3,.7),s.polymer,.12)
    s.screw('Grip small side inset','grip',56,-40,sign*7.15,.7)

# Game black folding stock with descending comb and slanted boot-like heel.
s.poly('Stock hinge block','stock',[(64,27),(72,27),(73,3),(65,1)],18,body,.6)
s.cyl('Stock hinge decorative pin','stock',(68,0,14),2.5,31,s.metal,'Z',.3)
s.poly('Stock solid outer silhouette','stock',[(70,29),(116,22),(143,23),(147,20),(148,-27),(141,-29),(129,-25),(120,-7),(73,-2)],18.2,stockmat,1.3)
s.poly('Stock descending cheek comb','stock',[(71,30),(117,23),(116,18),(73,23)],18.7,stockmat,.9)
s.poly('Stock lower inset panel','stock',[(73,7),(120,7),(129,-4),(124,-8),(117,-4),(74,-1)],.65,s.polymer,.5,y=-9.1)
s.poly('Stock lower inset panel opposite','stock',[(73,7),(120,7),(129,-4),(124,-8),(117,-4),(74,-1)],.65,s.polymer,.5,y=9.1)
s.poly('Stock rear rubber buttpad','stock',[(144,24),(150,23),(150,-28),(144,-31)],20,s.rubber,.9)
for sign in [-1,1]:
    s.poly('Stock length seam','stock',[(116,22),(118,22),(121,2),(119,1)],.35,s.dark,.2,y=sign*9.1)
    s.box('Stock rear adjustment plate','stock',(136,sign*9.2,7),(11,.8,6.2),s.dark,.6)
    s.box('Stock rear adjustment relief','stock',(136,sign*9.6,7),(7.8,.65,4.1),stockmat,.5)
    s.poly('Stock front blind sling panel','stock',[(77,20),(86,18),(84,12),(78,12)],.45,s.dark,.5,y=sign*9.1)
    s.poly('Stock front solid inner relief','stock',[(79,18),(84,17),(83,14),(80,14)],.5,stockmat,.4,y=sign*9.3)
    s.screw('Stock hinge cosmetic pin face','stock',68,7,sign*9.1,1.1)
    for j in range(9):
        z=-24+j*2.4
        s.box('Butt side texture notch','stock',(145,sign*9.55,z),(2.4,.6,.7),s.polymer,.15)
for z in range(-27,23,3):s.box('Buttpad horizontal tread','stock',(149.7,0,z),(.7,20.2,1.2),s.polymer,.2)

# Tall front post at the shoulder, low rear folded aperture.
s.poly('Front sight tower','front_sight',[(-83,23),(-82,43),(-80,48),(-76,48),(-73,43),(-73,23)],6.7,body,.65)
s.box('Sight front foot','front_sight',(-77,0,29),(10.5,12,3.6),body,.6)
s.cyl('Front sight blind ring edge','front_sight',(-78,-3.6,43),2.5,.75,s.steel,'Y',.15)
s.cyl('Front sight blind center','front_sight',(-78,-4.03,43),1.25,.15,s.dark,'Y',.04)
s.cyl('Front sight wide fixed hinge','front_sight',(-77,0,31),2.3,13,s.metal,'Y',.25)
s.box('Rear sight low base','rear_sight',(49,0,35.4),(12,8.3,3.1),body,.5)
s.poly('Rear sight sloped upright','rear_sight',[(44,35),(47,42),(48,47),(51,47),(54,39),(55,35)],5.3,body,.6)
s.cyl('Rear sight dark relief ring','rear_sight',(49,-2.9,43.5),1.65,.6,s.edge,'Y',.1)
s.cyl('Rear sight blind face','rear_sight',(49,-3.3,43.5),.7,.15,s.dark,'Y',.01)
s.screw('Rear sight base ornament','rear_sight',49,36,-4.35,.9)

s.box('Optional optic solid foot','optic',(13,0,36.3),(23,10,4.5),body,.6)
s.box('Optional optic lower riser','optic',(13,0,41),(15,8.6,6),body,.65)
s.cyl('Optional optic solid scope exterior','optic',(13,0,47),6.1,26,body,'X',.45)
s.cyl('Opaque optic front face','optic',(-.2,0,47),4.8,.6,s.glass,'X',.2)
s.cyl('Opaque optic rear face','optic',(26.1,0,47),4.3,.5,s.glass,'X',.2)
s.cyl('Optic cosmetic dial','optic',(14,-6.5,47),2.5,2.5,s.polymer,'Y',.25)
for x in [2,23]:s.cyl('Optic decorative ring','optic',(x,0,47),6.45,1.8,s.metal,'X',.18)
for obj in s.parts['optic'].children_recursive:obj.location.z-=.7
s.scene['print_segment_breaks_x_mm']='[-42]'
result=s.finish(['https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops','https://www.imfdb.org/images/thumb/a/a4/DFHO_SCARH.jpg/600px-DFHO_SCARH.jpg'],['以实际查看的游戏默认双侧截图为主，保留全黑外观、长矩形上机匣、短护木、长露出前端、直身黑弹匣和下斜厚枪托。','视角、像素与隐藏面不足使宽度、浅纹理和背面细节含艺术推断；未使用游戏提取网格、纹理或商标。','模型为实心缩比外观雕塑，无内部机构、贯通膛孔和真实接口；各件为网页外观展示分组，可选紧凑瞄具为数字外观配件。'])
