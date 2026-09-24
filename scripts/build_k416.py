"""K416 short-front game exterior sculpture; no mechanisms or real interfaces."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rifle_batch3_helpers import *
s=Sculpture('k416',300)
for key,label,show in [('upper','上机匣外观',True),('lower','下机匣与固定护圈',True),('handguard','四面护木外观',True),('front','短封闭前端',True),('magazine','弯曲实心弹匣',True),('grip','斜握把外观',True),('stock','宽肩枪托外观',True),('sights','固定机械瞄具',True),('optic','可选紧凑瞄具',False)]:s.part(key,label,show)
metal=s.mat('K416 grey-black metal',(.072,.082,.088),.72,.4)
poly=s.mat('K416 cool polymer',(.037,.047,.052),.04,.7)
# Default game barrel is short, almost completely under the thick ribbed handguard.
s.cyl('Solid short front tip','front',(-142,0,17),3.2,16,metal,'X',.2)
s.cyl('Closed front end disc','front',(-150,0,17),3,.2,s.dark,'X',.06)
s.cyl('Fixed front shoulder','front',(-134,0,17),4.3,4.4,s.metal,'X',.25)
s.poly('Fore-end solid closed shell','handguard',[(-136,29),(-43,29),(-40,24),(-40,8),(-136,8),(-140,12),(-140,23)],20.2,metal,.75)
s.rail('handguard',-136,-42,30,8,3.6)
s.box('Fore-end lower ornament base','handguard',(-88,0,7.8),(95,8.3,2),metal,.4)
for sign in [-1,1]:
    s.box('Fore-end side rail continuous shadow bed','handguard',(-88,sign*10,18),(91,1.0,12),s.dark,.5)
    s.box('Fore-end side rail filled bed','handguard',(-88,sign*10.55,18),(88,1.0,10.8),poly,.5)
    for i in range(24):
        x=-132+i*3.85
        s.box('Fore-end close transverse rib','handguard',(x,sign*11.18,18),(2.3,1.7,11.8),metal,.35)
        s.box('Fore-end top blind vent','handguard',(x,sign*8.65,27.5),(1.6,.3,1.3),s.dark,.3)
    for x in [-133,-46]:s.screw('Handguard cosmetic retained pin','handguard',x,11,sign*10.0,1.0)
for i in range(24):s.box('Fore-end bottom fixed rail rib','handguard',(-133+i*3.85,0,6.8),(2.2,10,1.6),metal,.3)
# AR family shape, independently dimensioned from K416 screenshot (shorter front).
s.poly('Upper closed angular receiver','upper',[(-44,30),(25,30),(33,27),(38,18),(32,8),(-43,8)],18,metal,.8)
s.cyl('Upper rounded rear shoulder','upper',(29,0,19),7,13,metal,'X',.5)
s.rail('upper',-41,32,30.3,8,3.6)
for sign in [-1,1]:
    s.box('Upper long bevel seam','upper',(-4,sign*8.9,24),(62,.55,2),s.edge,.35)
    s.box('Upper shallow lower seam','upper',(-4,sign*8.98,11),(66,.4,.6),s.dark,.2)
    s.screw('Upper small fixed fastener','upper',26,17,sign*9,.9)
s.box('Blind receiver port border','upper',(-6,9.18,18),(34,.8,9),s.dark,.7)
s.box('Closed receiver port metallic plate','upper',(-6,9.65,18),(31,.4,6.8),s.steel,.45)
s.line('Closed port lower hinge ornament','upper',(-22,10.0,13.9),(10,10.0,13.9),.7,metal)
s.poly('Fixed rear handle exterior','upper',[(22,29),(33,29),(34,30),(30,31),(22,30)],19,metal,.3)
s.poly('Filled lower receiver contour','lower',[(-44,12),(29,12),(32,4),(26,-3),(4,-6),(-18,-5),(-42,-10)],17,metal,.8)
s.poly('Angled magazine well exterior','lower',[(-45,8),(-15,8),(-15,-13),(-45,-11)],18.4,metal,.75)
g=s.poly('Squared static guard outer rim','lower',[(-17,0),(11,1),(17,-5),(15,-16),(9,-19),(-13,-17),(-18,-12)],7.5,metal,.75)
s.cut(g,s.poly('Guard exterior silhouette window','lower',[(-12,-4),(8,-3),(12,-7),(11,-13),(7,-15),(-10,-13)],20,s.dark,.5))
s.poly('Static trigger detail','lower',[(-1,2),(2,2),(4,-5),(1,-11),(-2,-10),(1,-4)],2.8,s.steel,.3)
for sign in [-1,1]:
    for x,z in [(-38,2),(-21,3),(8,6),(27,6)]:s.screw('Lower cosmetic round pin','lower',x,z,sign*(9.15 if x<-14 else 8.45),.85)
    s.cyl('Fixed selector relief round hub','lower',(17,sign*8.5,2),2.4,.9,metal,'Y',.17)
    s.line('Fixed selector short arm','lower',(17,sign*9,2),(14,sign*9,-1),.72,s.edge)
    s.box('Fixed side release plate','lower',(-19,sign*9.1,-1),(7,.85,3.2),s.polymer,.4)
    s.box('Small abstract maker plate','lower',(-32,sign*9.15,-4),(14,.25,3),metal,.25)
    for j in range(6):s.box('Abstract shallow maker dash','lower',(-37+j*1.8,sign*9.33,-4),(.75,.15,1.2),s.edge,.05)
# Curved long dark magazine, pronounced shallow longitudinal pressed grooves.
s.poly('Closed curved magazine body','magazine',[(-44,-8),(-16,-10),(-16,-27),(-20,-45),(-29,-65),(-53,-60),(-47,-34)],13.8,poly,.8)
side_plate(s,'Magazine shallow pressed side surface','magazine',[(-41,-15),(-19,-16),(-20,-28),(-24,-47),(-30,-60),(-49,-56)],6.8,metal,.4,.45)
for sign in [-1,1]:
    for j in range(4):
        x=-38+j*5.5
        s.line('Magazine long pressed groove upper','magazine',(x,sign*7,-17),(x-2,sign*7,-36),.55,s.dark)
        s.line('Magazine long pressed groove lower','magazine',(x-2,sign*7,-36),(x-9,sign*7,-56),.55,s.dark)
s.poly('Magazine closed floorplate','magazine',[(-53,-59),(-28,-63),(-29,-66),(-54,-62)],15,s.metal,.55)
# Steep modern pistol grip, broad smooth upper shoulder and textured lower panel.
s.poly('Solid angled ergonomic grip','grip',[(18,2),(28,0),(30,-12),(44,-41),(28,-43),(19,-26),(12,-8)],15,poly,1.2)
side_plate(s,'Grip inset panel','grip',[(19,-10),(27,-12),(38,-37),(29,-38),(21,-25)],7.4,s.rubber,.45,.7)
dot_texture(s,'grip',14,21,-13,7.62,.45,4,poly)
s.poly('Grip closed heel cap','grip',[(27,-40),(44,-39),(45,-44),(28,-45)],15.5,s.rubber,.55)
# Broad triangular crane-type stock profile seen in both game default views.
s.cyl('Solid stock connecting spine','stock',(59,0,19),5.2,54,s.metal,'X',.5)
s.cyl('Stock root exterior ring','stock',(36,0,19),7,5,metal,'X',.4)
s.poly('Wide stock cheek shoulder','stock',[(66,29),(145,29),(149,26),(149,9),(139,5),(83,5),(76,12)],23,poly,1.4)
s.poly('Stock fixed lower descending brace','stock',[(88,8),(98,8),(142,-14),(143,-23),(129,-18),(113,-3),(95,-1)],12.2,poly,.75)
s.poly('Stock attached rear butt','stock',[(143,29),(150,27),(150,-23),(143,-23)],24,s.rubber,.85)
s.poly('Stock short internal horizontal support','stock',[(103,4),(143,4),(143,-1),(113,-1)],13,poly,.5)
for sign in [-1,1]:
    s.box('Stock cheek long shallow plane','stock',(111,sign*11.4,20),(59,.4,6.2),poly,.75)
    s.poly('Stock lower small closed relief','stock',[(121,-2),(140,-2),(140,-14),(133,-12)],.5,metal,.5,y=sign*6)
    s.box('Stock blind sling slot','stock',(137,sign*11.5,9),(10,.35,2.5),s.dark,.7)
for z in range(-20,26,3):s.box('Stock buttpad shallow horizontal texture','stock',(150,0,z),(.6,24,.8),poly,.18)
sight(s,'sights',-126,30.5,True)
s.box('Rear sight round base','sights',(13,0,32),(11,9,3),metal,.5)
s.cyl('Rear sight fixed cylindrical turret','sights',(13,0,36),4.8,7,metal,'Z',.4)
s.cyl('Rear turret blind face','sights',(13,-4.8,36),1.2,.3,s.dark,'Y',.07)
optic(s,-18,32)
s.scene['print_segment_breaks_x_mm']='[48]'
result=finish(s,'依据 K416 游戏默认双侧图独立重建，保留很短的露出前端、密横纹四面护木、长弯曲弹匣、较陡握把、宽肩三角开窗枪托和圆形后瞄具；不是改名复用 M4A1 网格。')
