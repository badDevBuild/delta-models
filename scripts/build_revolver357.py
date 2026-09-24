"""Solid miniature .357 game revolver exterior: closed cylinder and front."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_compact_helpers import finish,optic
s=Sculpture('revolver357',100)
for k,l,v in [('barrel','封闭长前端与肋条',True),('frame','银灰外框',True),('cylinder','实心圆筒外观',True),('grip','棕木色弧形握把',True),('inlays','黑色握把嵌片',True),('controls','固定操控与护圈',True),('sights','低矮固定瞄具',True),('optic','可选短光学装饰',False)]:s.part(k,l,v)
silver=s.mat('Brushed cool revolver steel',(.24,.29,.32),.83,.30)
darksteel=s.mat('Dark polished steel',(.085,.106,.119),.75,.34)
wood=s.mat('Warm walnut brown grip',(.21,.086,.038),0,.6)
woodedge=s.mat('Walnut grain accent',(.14,.051,.022),0,.62)
# Long front sculpture is a full solid cylinder with closed shaded face.
s.cyl('Long solid forward exterior','barrel',(-27.2,0,30.5),4.25,45.5,silver,'X',.3)
s.cyl('Closed front rounded lip','barrel',(-49.1,0,30.5),4.5,1.8,silver,'X',.22)
s.cyl('Opaque front colour inset','barrel',(-50.06,0,30.5),2.8,.14,s.dark,'X',.12)
s.box('Full length top rib','barrel',(-27.5,0,36.0),(44,5.4,3.1),darksteel,.45)
s.box('Top rib polished plane','barrel',(-27.5,0,37.35),(44,4.7,.55),silver,.2)
for side in [-1,1]:
    for i in range(5):
        x=-44+i*8.2
        s.box('Top rib blind dark recess','barrel',(x,side*2.71,36),(5.6,.15,1.25),s.dark,.35)
        s.box('Top rib recess silver bottom','barrel',(x,side*2.83,35.45),(5.4,.10,.18),s.steel,.05)
under=s.poly('Solid sculpted lower shroud','barrel',[(-49,28),(-5,28),(-4,24),(-11,22.2),(-45,22.2),(-48,23.6)],7.4,darksteel,.55)
for side in [-1,1]:
    for x in [-41,-30,-19]:
        s.cut(under,s.box('Underlug blind pill recess','barrel',(x,side*3.68,24.9),(8.2,1.1,2.8),s.dark,1.1))
        s.box('Blind recess bottom face','barrel',(x,side*3.19,24.9),(7.0,.15,1.8),s.dark,.8)
# All-around external frame built as a solid artistic shape, without internal cavities.
s.poly('Outer frame silhouette','frame',[(-6,34),(-5,39),(18,39),(23,36),(27,29),(27,22),(34,16),(31,9),(18,7),(8,8),(-4,10),(-7,17)],11.8,silver,.75)
s.box('Cylinder upper bridge facet','frame',(6,0,37.8),(25,9.7,3.2),darksteel,.45)
s.poly('Frame front lower shoulder','frame',[(-6,25),(1,24),(2,11),(-4,11),(-7,14)],13,silver,.6)
for side in [-1,1]:
    s.poly('Rear frame side plate','frame',[(18,35),(22,33),(26,25),(26,21),(33,16),(28,12),(20,15),(17,20)],.4,darksteel,.55,y=side*6.0)
    s.screw('Frame cosmetic side screw','frame',23,19.8,side*6.24,.72)
    s.box('Blank frame engraving field','frame',(24.2,side*6.31,25),(7,.15,1.8),s.metal,.2)
# Cylinder is one closed solid, no bores/chambers/axle interface.
cyl=s.cyl('Closed solid rotating-form sculpture','cylinder',(6.6,0,26.2),9.65,18.0,darksteel,'X',.4,64)
for i in range(6):
    a=i*math.tau/6+.20
    y=11.0*math.sin(a);z=26.2+11.0*math.cos(a)
    s.cut(cyl,s.cyl('Shallow outer cylinder flute','cylinder',(5.2,y,z),2.15,12.5,s.dark,'X',.65,32))
s.cyl('Cylinder closed front band','cylinder',(-2.15,0,26.2),9.68,.85,silver,'X',.22)
s.cyl('Cylinder closed rear band','cylinder',(15.4,0,26.2),9.7,1.3,silver,'X',.22)
# Small external blocks suggest surface indexing without holes or moving parts.
for side in [-1,1]:
    s.box('Cylinder blind surface notch','cylinder',(10.5,side*9.48,26.8),(2.6,.18,2.1),s.dark,.25)
# Sculpted warm grip extends in a clear back-curved shape.
s.poly('Full walnut grip sculpture','grip',[(25,19),(34,15),(36,7),(39,-2),(46,-13),(50,-25),(47,-29),(30,-29),(29,-24),(28,-14),(23,-4),(22,3),(19,8)],13.8,wood,1.15)
for side in [-1,1]:
    s.poly('Walnut shoulder highlight','grip',[(25,16),(31,13),(32,6),(28,1),(24,3),(22,8)],.35,woodedge,.55,y=side*6.88)
    s.poly('Black grip inset panel','inlays',[(27,4),(32,1),(35,-6),(41,-16),(44,-26),(32,-26),(32,-20),(30,-12),(25,-2)],1.0,s.rubber,.65,y=side*6.85)
    for row in range(14):
        z=0-row*1.8;x0=28.3+max(0,-z)*.20
        for col in range(4):
            x=x0+col*1.15
            o=s.box('Black inset diamond checkering','inlays',(x,side*7.4,z),(.57,.18,.57),s.polymer,.09);o.rotation_euler[1]=math.pi/4
    s.screw('Grip central slotted cosmetic pin','inlays',32,-9.8,side*7.45,.8)
    # Thin coloured grain accents are surface art, deliberately excluded from geometry union.
    for row in range(4):
        o=s.line('Walnut shallow colour grain','grip',(44+row*.6,side*6.83,-15),(46+row*.4,side*6.83,-24),.08,woodedge);o['print_skip']=True
# Sculpted guard and rear crest are fixed, not a mechanism.
guard=s.poly('Fixed oval guard outside','controls',[(0,13),(22,12),(25,8),(24,0),(20,-5),(10,-6),(3,-3),(-1,3)],6.0,darksteel,.65)
s.cut(guard,s.poly('Open exterior guard silhouette','controls',[(3,10),(19,10),(21,7),(20,1),(17,-2),(10,-3),(5,0),(3,4)],20,s.dark,.65))
s.poly('Fixed curved trigger art','controls',[(12,13),(15,12),(15,8),(14,3),(11,-.5),(9,0),(11,3),(12,8)],2.6,silver,.4)
s.poly('Fixed rear crest ornament','controls',[(21,35),(23,40),(26,42),(30,43),(32,42.3),(29,41),(26,38),(25,33)],4.0,darksteel,.45)
for side in [-1,1]:
    s.poly('Fixed rear side lever','controls',[(19,29),(23,29),(24,27),(22,25),(18,26)],.7,s.metal,.5,y=side*6.18)
    s.screw('Fixed side lever cosmetic pin','controls',21,27.5,side*6.62,.6)
s.poly('Front low ramp sight','sights',[(-49,37),(-48,40),(-45,40),(-41,37)],2.5,s.polymer,.28)
s.box('Rear sight plinth','sights',(16,0,40),(7.5,6.5,1.6),s.polymer,.3)
for side in [-1,1]:s.box('Rear fixed sight shoulder','sights',(18,side*2.3,41.3),(2.6,1.5,2.3),darksteel,.22)
# Digital accessory rests on a solid lower saddle, no standardized interface.
s.box('Optional optic lower saddle','optic',(-2,0,39),(18,7.5,2.8),darksteel,.4)
optic(s,'optic',-2,40.5,.72)
result=finish(s,'https://www.imfdb.org/images/thumb/b/bf/DFHO_Magnum.jpg/600px-DFHO_Magnum.jpg',['依据游戏默认长银灰前端、顶部短槽肋、下颏浅凹、棕色弧形握把及黑色嵌片重建。','圆筒为不可转动的封闭实心外观体，仅外表浅凹，无弹巢通孔、内部构造和可用接口。少量木纹线作为数字表面色彩，默认融合排除这些细线。'])
