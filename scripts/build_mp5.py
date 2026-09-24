"""MP5 game-reference exterior miniature. Filled surfaces, no mechanism or interfaces."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('mp5',198)
for k,l,v in [('receiver','冲压机匣外观',True),('handguard','宽护木外观',True),('stock','固定聚合物枪托',True),('grip','握把与固定护圈',True),('magazine','弧形实心弹匣外观',True),('muzzle','封闭短前端',True),('front_sight','前环形固定瞄具',True),('rear_sight','后固定瞄具',True),('optic','可选微型瞄具装饰',False)]:s.part(k,l,v)
body=s.mat('Blackened stamped steel',(.048,.061,.068),.8,.37)
poly=s.mat('MP5 fine charcoal polymer',(.057,.066,.070),.025,.67)
relief=s.mat('Molded black surface relief',(.070,.078,.081),.035,.73)
red=s.mat('Faded oxide red abstract marks',(.26,.049,.039),.06,.67)

# Upper receiver tube overlaps its pressed lower cover; all cavities remain blind.
s.cyl('Rounded upper receiver spine','receiver',(2.7,0,4.9),6.2,65.8,body,'X',.3,64)
s.poly('Stamped receiver lower silhouette','receiver',[(-30,4),(35,4),(35,-5),(28,-9),(-19,-9),(-23,-6),(-30,-6)],12.2,body,.75)
s.box('Receiver flattened upper bridge','receiver',(2,0,9.4),(64,7.2,2),body,.35)
for sign in [-1,1]:
    s.poly('Pressed receiver side surface','receiver',[(-29,3),(33,3),(33,-4),(26,-7),(-24,-7),(-29,-4)],.7,body,.45,y=sign*6)
    s.box('Receiver longitudinal blind shadow','receiver',(-1,sign*6.37,1.9),(57,.18,1.1),s.dark,.25)
    s.box('Pressed receiver upper highlight rib','receiver',(-2,sign*6.55,3.1),(56,.42,.74),s.edge,.17)
    s.box('Pressed receiver lower rib','receiver',(0,sign*6.55,-3.3),(61,.54,.8),body,.23)
    s.box('Sealed side recess','receiver',(-2,sign*6.58,5.7),(22,.18,2.45),s.dark,.45)
    s.box('Sealed side recess floor','receiver',(-1,sign*6.72,5.55),(18,.18,1.34),body,.3)
    for x in [-24,26]:s.screw('Receiver cosmetic mounting stud','receiver',x,-4.6,sign*6.3,.72)
    for x in [-27,-21,22,28]:
        s.poly('Stamped diagonal corner detail','receiver',[(x,-5.8),(x+1.8,-5.8),(x+3,-3.9),(x+1.5,-3.9)],.3,s.edge,.15,y=sign*6.39)
    s.box('Blank origin identification plate','receiver',(15,sign*6.38,-1),(13,.25,1.25),body,.2)
    for i in range(8):
        s.box('Abstract shallow identification dash','receiver',(9.2+i*1.4,sign*6.57,-1),(.61,.14,.21),s.edge,.04)
s.rail('receiver',-29,28,11,7,3.3)
for x in [-24,23]:s.box('Rail clamp ornamental bridge','receiver',(x,0,9.5),(4.8,12.8,2),body,.4)

# The game base reference has a broad smooth handguard with long molded flutes.
guard=s.poly('Solid broad polymer handguard','handguard',[(-80,6.7),(-75,8),(-31,8),(-27,5),(-28,-6.2),(-33,-7.6),(-77,-5.6),(-80,-3.9)],15.3,poly,1.2)
s.cyl('Upper handguard solid spine','handguard',(-55,0,8.3),2.45,53,s.metal,'X',.3)
for sign in [-1,1]:
    s.poly('Handguard molded elongated panel','handguard',[(-74,4.9),(-34,4.9),(-32,2.8),(-33,-3.2),(-74,-2.5)],.65,relief,.7,y=sign*7.45)
    for z in [-1.3,.1,1.5,2.9]:
        s.box('Long shallow grip flute','handguard',(-53.5,sign*7.87,z),(38,.19,.48),s.dark,.19)
    for x in [-78,-29.4]:s.box('End collar molded seam','handguard',(x,sign*7.65,.1),(.68,.3,9),poly,.23)
    s.screw('Front handguard blind pin','handguard',-76.7,4.3,sign*7.69,.75)
    # Compact fixed charging-handle ornament attached to the solid upper rod.
    if sign==-1:
        s.cyl('Fixed handle short bridge','handguard',(-51,-3.9,9),1.35,5.9,body,'Y',.2)
        s.box('Fixed handle paddle','handguard',(-51,-6.5,10.2),(5.7,3.3,3.1),poly,.7)
        for x in [-52.8,-51.6,-50.4]:s.box('Handle molded ridge','handguard',(x,-8.08,10.2),(.36,.18,1.7),relief,.12)
for x in [-71,-60,-49,-38]:s.box('Handguard lower mold division','handguard',(x,0,-6.3),(.45,10.5,.28),poly,.12)

# Fixed stock mirrors the broad lower wedge and narrow neck of the screenshot.
stock=s.poly('Fixed buttstock silhouette','stock',[(33.4,9.2),(40,11.2),(47,7.5),(57,.6),(64,-.9),(96,-.9),(98,-3),(98,-27),(94,-28),(62,-15),(52,-11),(43,-9),(33.4,-10)],15.5,poly,1.9)
for sign in [-1,1]:
    s.poly('Stock side molded broad panel','stock',[(46,5.8),(59,-1.9),(67,-3.5),(95,-3.5),(95,-24.5),(66,-13.7),(54,-9.4),(45,-8)],.4,poly,.8,y=sign*7.59)
    s.poly('Stock blind sling recess backing','stock',[(77,-12),(80,-8),(89,-8),(92,-11),(89,-15),(80,-15)],.44,s.dark,.5,y=sign*7.94)
    s.poly('Stock shallow sling inset plate','stock',[(78,-12),(81,-9.2),(88,-9.2),(90.5,-11.6),(88,-14),(81,-14)],.32,body,.4,y=sign*8.18)
    s.box('Stock closed central sling slot','stock',(84.5,sign*8.40,-11.5),(2.1,.16,4),s.dark,.27)
    for x in [80,89]:s.screw('Stock plate cosmetic rivet','stock',x,-11.5,sign*8.29,.44)
    s.screw('Stock fixed neck pin','stock',39,-6.5,sign*7.7,.83)
s.poly('Rubber butt cap','stock',[(95.9,-1.5),(98,-2.8),(98,-26.8),(95.9,-27.5)],16.0,s.rubber,.55)
for z in [-5,-8,-11,-14,-17,-20,-23]:s.box('Butt pad cross relief','stock',(97.82,0,z),(.62,13.3,.85),poly,.21)

# Grip and open outer guard are decorative, with a fixed solid trigger silhouette.
s.poly('Lower control housing','grip',[(-22,-6),(34,-6),(33,-17),(27,-21),(-15,-21),(-20,-18)],12.7,poly,.7)
s.poly('Angled MP5 pistol grip','grip',[(15,-18),(27,-18),(29,-23),(39,-43),(37,-47),(25,-51),(23,-46),(21,-36),(16,-27)],13.1,poly,1.25)
for sign in [-1,1]:
    s.poly('Grip inset side face','grip',[(20,-24),(26,-23),(35.5,-43),(34,-45.7),(27,-48),(25.4,-43),(23,-34)],.4,relief,.7,y=sign*6.43)
    for row in range(14):
        z=-27.5-row*1.25;x=22.8+row*.32
        for j in range(5):
            s.box('Fine grip polymer stipple','grip',(x+j*1.15,sign*6.76,z),(.55,.24,.55),poly,.12)
    s.cyl('Fixed fire-selector disk','grip',(21,sign*6.65,-14.4),1.45,.5,body,'Y',.1,32)
    s.poly('Fixed selector raised pointer','grip',[(20.2,-14),(18.4,-17.5),(19.6,-18),(22,-14.4)],.45,body,.2,y=sign*7)
    for j,(x,z) in enumerate([(10,-11.5),(10,-14.5),(12,-17.3)]):
        for n in range(2+j):s.box('Abstract faded selector mark','grip',(x+n*1.4,sign*6.5,z),(.74,.13,.3),red,.06)
    s.screw('Grip frame fixed pin','grip',-17,-12,sign*6.5,.78)
    s.box('Fixed magazine catch ornament','grip',(-9,sign*6.61,-13.5),(6.3,.9,3.3),body,.35)
    for x in [-11,-9.5,-8]:s.box('Catch raised grip relief','grip',(x,sign*7.14,-13.5),(.45,.18,2.4),s.edge,.08)
outer=s.poly('Fixed trigger guard outer frame','grip',[(-12,-19),(20,-19),(21,-25),(16,-31),(-6,-31),(-11,-27)],6.5,poly,.65)
s.cut(outer,s.poly('Guard silhouette opening','grip',[(-8,-20.7),(16,-20.7),(17.2,-25),(13.7,-28.4),(-4.5,-28.4),(-8,-25.2)],18,s.dark,.7))
s.poly('Fixed curved trigger artwork','grip',[(1,-19),(4,-19),(5,-23),(2,-27.7),(-.5,-28.2),(-2,-27),(.3,-25.9),(1.8,-22.5)],2.5,body,.4)
s.box('Solid magazine paddle ornament','grip',(-13,0,-21.2),(3.2,9,3.2),body,.45)

# Curved magazine profile follows the game image rather than a straight stick.
mp=[(-23,-18),(-12,-18),(-14,-31),(-17,-43),(-23,-57),(-30,-68),(-39,-65),(-32,-52),(-27,-38)]
s.poly('Solid curved magazine sculpture','magazine',mp,10.7,body,.85)
for sign in [-1,1]:
    s.poly('Magazine recessed central pressed panel','magazine',[(-22,-23),(-15.3,-23),(-18,-36),(-21,-46),(-27,-60),(-30.8,-65),(-35.5,-63),(-29.3,-51),(-24.5,-37)],.3,s.dark,.4,y=sign*5.33)
    for dx in [0,3.7]:
        s.poly('Magazine curved stamped longitudinal flute','magazine',[(-21+dx,-23),(-20+dx,-23),(-22.6+dx,-36),(-26+dx,-47),(-31.5+dx,-59),(-34+dx,-63),(-35+dx,-62.8),(-32.4+dx,-58.5),(-27+dx,-46),(-23.5+dx,-35.5)],.5,s.edge,.16,y=sign*5.55)
    for x,z in [(-19,-26),(-22,-38),(-26,-49),(-31,-60)]:
        s.cyl('Magazine small blind witness dot','magazine',(x,sign*5.45,z),.44,.14,s.dark,'Y',.03,20)
s.poly('Magazine rounded floorplate','magazine',[(-39.7,-64.3),(-30.2,-68.8),(-29,-67),(-38.5,-62.6)],11.4,poly,.5)

# Closed muzzle, with a visibly solid front disc.
s.cyl('Short solid front stem','muzzle',(-87.2,0,0),2.75,17.8,body,'X',.22)
s.cyl('Solid front nose cap','muzzle',(-96.7,0,0),3.3,2.5,body,'X',.3)
s.cyl('Opaque closed front face','muzzle',(-98.0,0,0),2.2,.16,s.dark,'X',.04)
for x in [-95.2,-91.6,-86.5]:s.cyl('Front circular ornamental seam','muzzle',(x,0,0),2.89,.45,s.edge,'X',.08)
s.cyl('Front sight mounting collar','front_sight',(-82.0,0,.2),5.2,4.2,body,'X',.3)
s.poly('Front sight triangular fixed foot','front_sight',[(-84,1),(-80,1),(-80,13),(-81.5,17.2),(-83.5,17.2),(-85,13)],7.2,body,.55)
ring=s.cyl('Front sight solid outer hood','front_sight',(-82,0,17),4.75,2.7,body,'X',.2)
s.cut(ring,s.cyl('Front sight exterior ring opening','front_sight',(-82,0,17),3.15,8,s.dark,'X',.05))
s.box('Fixed front sight post','front_sight',(-82,0,14.8),(2.4,1.45,5),body,.2)
s.box('Front sight ring buried bridge','front_sight',(-82,0,12.2),(2.2,3.2,3),body,.35)
s.box('Rear sight anchored base','rear_sight',(24,0,11.8),(10,9,3),body,.45)
s.cyl('Rear fixed sight drum','rear_sight',(25,0,14.4),3.4,4.2,body,'Z',.35)
s.cyl('Rear closed sight face','rear_sight',(25,-3.18,14.4),1.12,.21,s.dark,'Y',.05)
for sign in [-1,1]:s.screw('Rear sight fixed adjustment ornament','rear_sight',22,12.5,sign*4.4,.7)

# Optional digital sight: opaque lens and arbitrary sculpture-only mounting foot.
s.box('Optic closed solid mounting block','optic',(0,0,14.6),(14.5,8,4.6),body,.5)
s.poly('Micro optic outer housing','optic',[(-6,16),(7,16),(6.5,25),(4.5,27),(-4.5,27),(-6.3,24)],9.6,poly,.75)
s.box('Opaque optic forward glass','optic',(-6.4,0,22),(0.6,6.5,6.5),s.glass,.8)
s.box('Opaque optic rear glass','optic',(6.8,0,22),(.5,6.5,6.5),s.glass,.8)
for sign in [-1,1]:
    s.cyl('Optic exterior adjustment cap','optic',(1,sign*4.9,20.2),1.6,.8,body,'Y',.15)
    s.screw('Optic fixed foot bolt','optic',0,15,sign*4.4,.85)
result=s.finish(['https://zilliongamer.com/delta-force/c/weapons/best-mp5-build-delta-force','https://zilliongamer.com/uploads/delta-force/weapons-builds/submachine-gun/mp5/mp5-delta-force.jpg','https://deltaforcedb.com/assets/images/weapons/mp5.webp'],['实际查看 780×408 游戏基础侧视图：固定黑色宽枪托、宽光面护木、圆弧上机匣、顶部导轨和长弯弹匣。','背面、顶部、底部和纹理密度依据可见轮廓做艺术推断；商标及文字以抽象短纹替代。','约 198 mm 实心微缩外观雕塑；前端封闭，扳机与控制件固定，数字外观组不提供真实安装接口。','可选微型瞄具为独立数字装饰。首版实体打印仅基础配置，按整体融合后左右胶合分件。'])
