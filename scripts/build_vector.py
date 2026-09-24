"""Vector exterior sculpture from the game's base silhouette. No functional geometry."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('vector',190)
for k,l,v in [('upper','阶梯形上壳体',True),('lower','下部整体外观壳体',True),('grip','倾斜握把与护圈',True),('stock','固定骨架枪托',True),('magazine','短实心弹匣装饰',True),('muzzle','细长封闭前端',True),('sights','前后固定机械瞄具',True),('optic','可选全息瞄具装饰',False)]:s.part(k,l,v)
body=s.mat('Graphite Vector molded housing',(.075,.083,.087),.16,.57)
upper=s.mat('Cool machined upper rail',(.092,.107,.119),.72,.4)
panel=s.mat('Textured side graphite',(.049,.058,.064),.06,.75)
red=s.mat('Muted selector red',(.28,.049,.042),.08,.65)

# Long upper housing is filled throughout; the side slot is blind decoration.
s.poly('Upper receiver stepped silhouette','upper',[(-61,12.8),(35,12.8),(40,10.4),(42,8),(42,3.2),(21,3.2),(17,5.2),(-10,5.2),(-17,2.2),(-61,2.2)],15.6,upper,.7)
s.poly('Upper left to right raised cover ridge','upper',[(-60,12.1),(34,12.1),(38,9.9),(20,9.9),(-10,10.5),(-60,10.5)],14.7,upper,.25)
s.rail('upper',-59,26,14.1,7.4,3.15)
for sign in [-1,1]:
    s.poly('Upper external plate face','upper',[(-59,11.6),(32.5,11.6),(36,9),(17,7),(-9,7),(-15,4),(-59,4)],.46,body,.3,y=sign*7.72)
    for x,z,r in [(-56,8,.67),(-44,8.3,.78),(-33.5,10,.63),(-23,6.7,.62),(-16,10.3,.58),(-3,7.7,.80),(18,9.2,.63)]:
        s.screw('Upper housing cosmetic blind bolt','upper',x,z,sign*8.0,r)
    s.box('Rear upper fine molding seam','upper',(27,sign*8.05,6.5),(19,.15,.42),s.dark,.12)
    for i in range(6):s.box('Abstract small upper data mark','upper',(-56+i*1.18,sign*8.12,10),(.58,.15,.2),s.edge,.04)
    for i in range(2):s.box('Abstract selector dash','upper',(-11+i*2.4,sign*8.16,10),(.9,.16,.3),red,.07)

# Front box and downward angled body create the distinctive Vector profile.
s.poly('Solid front short forebody','lower',[(-61,3.1),(-17,3.1),(-13,-3.5),(-26,-9),(-59,-9),(-61,-7)],16.2,body,.65)
s.poly('Angled solid lower housing','lower',[(-34,-2),(-8,5.5),(1,5.5),(-1,-7),(7,-23),(15,-29),(13,-31),(-18,-31),(-22,-28),(-25,-19),(-31,-8)],17.6,body,.9)
for sign in [-1,1]:
    s.poly('Angular lower side inset large','lower',[(-29,-4),(-7,3.2),(-2,3.2),(-3.3,-7),(4,-22),(11,-28),(-15,-28),(-18,-25),(-23,-12)],.52,panel,.65,y=sign*8.65)
    s.poly('Lower molded external border panel','lower',[(-25,-9),(-20,-7),(-16,-9),(-10,-25),(-12,-27),(-16,-26),(-23,-12)],.45,body,.45,y=sign*9.03)
    s.poly('Lower side long relief stripe','lower',[(-22,-9.8),(-20.8,-9.8),(-15.5,-24),(-16.7,-24)],.21,s.dark,.19,y=sign*9.3)
    s.poly('Front lower side flat cover','lower',[(-59,1.8),(-35,1.8),(-29,-4),(-31,-7),(-59,-7)],.44,upper,.4,y=sign*8)
    s.box('Closed charging ornament recess','lower',(-46,sign*8.33,1.8),(20,.23,2.5),s.dark,.45)
    s.box('Fixed charging handle bridge','lower',(-53,sign*9.1,1.8),(4.0,2.3,2.25),upper,.35)
    s.box('Fixed charging handle outer paddle','lower',(-53,sign*10.05,1.8),(6,.9,2.25),body,.3)
    for x in [-54.7,-53.4,-52.1]:s.box('Charging paddle raised ridge','lower',(x,sign*10.6,1.8),(.42,.16,1.35),s.edge,.07)
    for x,z,r in [(-56,-3.7,1.0),(-42,-3.5,.95),(-26,-5.3,.8),(-18,-11.5,.70),(-12,-25.5,.83),(-7,-29,.87),(10,-28.6,.85)]:
        s.screw('Lower housing decorative fastener','lower',x,z,sign*(8.15 if x<-35 else 9.0),r)
    s.box('Magazine catch external block','lower',(-27,sign*9.05,-2.8),(10,1.0,5.2),upper,.55)
    for j in range(4):s.box('Catch broad relief ridge','lower',(-30.6+j*1.8,sign*9.64,-1.7),(.8,.3,1.45),s.edge,.16)
    for x in [-29.5,-26.5]:s.cyl('Catch shallow round mark','lower',(x,sign*9.73,-3.4),.66,.17,s.dark,'Y',.05)
    s.poly('Lower side heel cover','lower',[(-24,-24.5),(-20,-24.5),(-17.5,-30),(-22,-30)],.45,body,.45,y=sign*8.9)
    s.box('Lower panel narrow molding cut','lower',(-1.5,sign*9.0,-21),(1.1,.24,9.3),s.dark,.22)
    # Small geometric stipple islands imply the screenshot's molded texture.
    for row in range(12):
        z=-8.7-row*1.35;x=-12+row*.15
        for j in range(6):s.box('Lower polymer fine stipple','lower',(x+j*1.3,sign*8.98,z),(.43,.18,.43),body,.08)
for x in [-58,-54,-50,-46,-42,-38]:s.box('Lower front ornamental rail rib','lower',(x,0,-8.6),(2.2,11.9,1.1),upper,.2)

# The large open grip window is modeled as solid exterior bars, not a mechanism.
s.poly('Vector diagonal pistol grip exterior','grip',[(12,5.5),(25,6),(33,-14),(37,-23),(33,-26),(26,-28),(24,-25),(21,-14)],14.7,body,.9)
s.poly('Lower fixed grip guard link','grip',[(11,-29),(25,-26.7),(33,-23),(33,-26),(24,-30.5),(15,-32),(9,-31)],12.4,body,.55)
s.box('Upper trigger window solid rear bridge','grip',(13.3,0,3.3),(6.5,12,4),body,.5)
s.poly('Fixed trigger guard front arc','grip',[(-1,-4),(1,-4),(2,-6),(13,-6),(14,-4),(15,-4),(15,-7.5),(2,-8.5),(-1,-6)],4.0,upper,.4)
s.poly('Fixed trigger silhouette','grip',[(8.7,4),(10.8,4),(12,0),(10,-4),(7.8,-5),(6.4,-4),(8.8,-2.5),(9.6,0)],2.6,s.metal,.25)
for sign in [-1,1]:
    s.poly('Grip recessed broad side panel','grip',[(18,2),(23.4,2.4),(32.8,-21.8),(29,-24.1),(25.5,-22),(23,-12)],.5,panel,.55,y=sign*7.29)
    for row in range(16):
        z=.2-row*1.35;x=20.5+row*.36
        for j in range(4):s.box('Grip fine molded stipple','grip',(x+j*.95,sign*7.64,z),(.42,.21,.42),body,.09)
    for z,x in [(0,21),(-5,23),(-10,25),(-15,27),(-20,29)]:s.box('Grip side shallow embossed dash','grip',(x,sign*7.71,z),(1.0,.16,.28),s.edge,.07)

# Slender fixed stock arm and broad skeleton butt follow the game base screenshot.
s.poly('Fixed stock upper arm','stock',[(36,10.4),(42,8),(68,8),(72,6.5),(73,3),(70,1.5),(44,3),(40,3)],11.8,body,.8)
s.poly('Stock angled descending brace','stock',[(67,5),(72,5),(78,-24),(75,-27),(70,-12)],10.4,body,.65)
s.poly('Stock solid heel and butt upright','stock',[(76,-23),(90,-25),(91,-1.2),(96,-1.2),(96,-30),(92,-31),(79,-30),(75,-27)],13.8,body,.9)
s.poly('Stock mid upper cross link','stock',[(71,0),(92,0),(92,-6),(73,-6)],10.9,body,.55)
s.poly('Stock lower crossing brace','stock',[(73,-8),(76,-8),(85,-25),(81,-27),(77,-20)],8.7,body,.5)
for sign in [-1,1]:
    s.poly('Stock arm top relief','stock',[(42,7.7),(67,7.7),(70,6),(44,5.8)],.35,s.edge,.2,y=sign*5.86)
    s.box('Stock blind adjustment recess','stock',(83,sign*5.59,-3),(10,.24,2.3),s.dark,.4)
    for x,z in [(87,-3),(86,-25)]:s.screw('Stock decorative attachment bolt','stock',x,z,sign*(5.5 if z>-10 else 7),.9)
    s.poly('Stock open triangle edge ridge','stock',[(75,-9),(76,-9),(80,-22),(79,-23)],.35,s.edge,.17,y=sign*4.3)
s.poly('Fixed stock rubber butt pad','stock',[(94,-1.2),(97,-1.5),(97,-29.4),(94,-30.6)],16.0,s.rubber,.7)
for z in [-4,-7,-10,-13,-16,-19,-22,-25,-28]:s.box('Stock pad transverse traction relief','stock',(96.9,0,z),(.55,14,.68),body,.17)

# Short visible base magazine has a slanted floorplate, all faces closed.
s.poly('Short solid magazine lower sculpture','magazine',[(-23,-28),(-11,-28),(-6,-42.9),(-16,-47),(-18,-46),(-23,-32)],12.5,upper,.6)
for sign in [-1,1]:
    s.poly('Magazine molded panel','magazine',[(-20.9,-32),(-13,-32),(-9.5,-41.4),(-15.7,-43.7)],.45,panel,.4,y=sign*6.2)
    s.poly('Magazine blind identification inset','magazine',[(-16.5,-39),(-11.6,-37.8),(-10.8,-40),(-15.7,-41.5)],.23,s.dark,.23,y=sign*6.51)
    for i in range(3):s.box('Magazine molded notch relief','magazine',(-18.8+i*2.15,sign*6.51,-33.8),(.75,.22,2.2),body,.15)
s.poly('Magazine fixed slanted base cap','magazine',[(-17.6,-45.5),(-6.9,-41.7),(-5.9,-43.7),(-16.6,-47.6)],13.1,body,.4)

# Closed thin exposed front stem, deliberately ornamental with no through bore.
s.cyl('Solid thin front barrel-like ornament','muzzle',(-77.3,0,-1.9),1.78,35.4,s.metal,'X',.16,64)
s.cyl('Solid muzzle collar','muzzle',(-93.2,0,-1.9),2.47,3.6,upper,'X',.18)
s.cyl('Closed dark muzzle disc','muzzle',(-95.08,0,-1.9),1.72,.18,s.dark,'X',.04)
for x in [-94.4,-92.7,-91]:s.cyl('Muzzle shallow exterior ring','muzzle',(x,0,-1.9),2.56,.4,s.edge,'X',.07)
s.cyl('Solid front root shoulder','muzzle',(-61.4,0,-1.9),2.7,3.0,upper,'X',.2)

# Both sights anchored into the top housing. Front ring is strengthened at its foot.
for x,front in [(-53,True),(23,False)]:
    s.box('Fixed sight broad anchored base','sights',(x,0,14.8),(8.5,10,3.6),s.metal,.5)
    s.poly('Fixed upright sight stem','sights',[(x-1.7,15),(x+1.7,15),(x+2.1,24),(x+1,25.2),(x-1.6,25.2)],4.7,body,.35)
    s.cyl('Sight outer circular relief','sights',(x,0,22),2.7,2.5,s.metal,'X',.17,40)
    s.cyl('Sight closed center face','sights',(x-1.29,0,22),1.4,.18,s.dark,'X',.04,32)
    for sign in [-1,1]:s.screw('Sight base fixed side stud','sights',x,15,sign*5.0,.78)

# Optional digital-only holographic accessory with opaque lens.
s.box('Holographic sight sculpture foot','optic',(-18,0,18),(18,10,5),s.metal,.65)
s.poly('Holographic sight hood','optic',[(-27,20),(-10,20),(-11,31),(-14,34),(-24,34),(-27,31)],11.6,body,.85)
s.box('Opaque forward holographic glass','optic',(-27,0,27.5),(.5,8.3,8.1),s.glass,1.0)
s.box('Opaque rear holographic glass','optic',(-10.3,0,27.4),(.5,8.2,7.8),s.glass,1.0)
s.box('Optic control side module','optic',(-17,-6.2,24),(8,2.4,5.3),s.metal,.55)
for x in [-19.3,-15.5]:s.cyl('Optic external control circle','optic',(x,-7.5,24),1.05,.55,body,'Y',.13)
for sign in [-1,1]:s.screw('Optic fixed mounting decoration','optic',-19,18,sign*5.3,.9)
result=s.finish(['https://zilliongamer.com/delta-force/c/weapons/best-vector-build-delta-force','https://zilliongamer.com/uploads/delta-force/weapons-builds/submachine-gun/vector/vector-delta-force-build.jpg','https://deltaforcedb.com/assets/images/weapons/vector.webp'],['实际查看 780×408 游戏基础侧视图：细长前端、阶梯形上壳、倾斜下部壳体、短弹匣、宽握把开窗与骨架枪托。','采用微缩图像比例，隐藏背面、内部遮蔽区、表面颗粒和螺钉槽为艺术推断；抽象图形替代商标与文字。','约 190 mm 实心非功能外观雕塑，前端封闭，无内部机构、真实安装配合或可动作控制件。','瞄具为可选数字外观配件。首版实体打印仅基础配置，整体融合后按左右平面胶合。'])
