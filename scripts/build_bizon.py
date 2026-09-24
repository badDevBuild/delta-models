"""Bizon inert exterior with filled decorative cylindrical lower volume."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch3_smg_helpers import Sculpture,optic,guard,closed_front,finish
s=Sculpture('bizon',220)
for k,l,v in [('receiver','圆弧顶冲压外壳',True),('handguard','短护木与浅通风纹',True),('stock','三角骨架托外观',True),('grip','倾斜握把及固定护圈',True),('cylinder','实心圆筒装饰体',True),('muzzle','封闭细前端',True),('sights','固定前后瞄具',True),('optic','可选数字微型瞄具',False)]:s.part(k,l,v)
m=s.mat('Bizon dark pressed steel',(.054,.063,.069),.7,.4);p=s.mat('Bizon black polymer',(.027,.032,.034),.02,.72)
s.scene['print_segment_breaks_x_mm']=[-31]
s.poly('Stamped receiver solid base','receiver',[(-26,18),(39,18),(44,14),(44,-5),(-1,-5),(-7,-2),(-26,-2)],14.6,m,.65)
s.poly('Rounded upper dust cover silhouette','receiver',[(-23,18),(-18,23),(33,23),(39,19),(38,16),(-25,16)],13.7,m,.9)
s.box('Upper cover narrow flat spine','receiver',(7,0,22.8),(51,7.6,1.3),m,.35)
for sign in [-1,1]:
    s.poly('Broad stamped side face','receiver',[(-21,15),(40,15),(41,-2),(-1,-2),(-8,1),(-23,1)],.4,m,.4,y=sign*7.23)
    s.box('Long upper cover seam','receiver',(7,sign*7.46,15.4),(64,.24,.7),s.edge,.18)
    s.box('Shallow receiver lower pressed line','receiver',(16,sign*7.48,-1),(43,.3,.7),s.edge,.15)
    for x,z in [(-18,10),(-16,3),(-4,-1),(10,0),(39,3)]:s.screw('Fixed side rivet','receiver',x,z,sign*7.5,.62)
    s.poly('Fixed selector stamped strip','receiver',[(7,10),(36,10),(37,8),(17,8),(8,5),(5,6)],.6,m,.35,y=sign*7.4)
    s.cyl('Selector disk artwork','receiver',(35,sign*7.65,10.2),2.0,.55,m,'Y',.2)
    for i in range(6):s.box('Abstract stamped legend','receiver',(15+i*1.6,sign*7.55,4),(.8,.13,.27),s.edge,.04)
# Wide high-sided foreguard with four observed oblong dark blind recesses.
s.poly('Solid upper foreguard','handguard',[(-86,23),(-30,23),(-21,19),(-23,3),(-84,3)],16.2,m,.7)
s.box('Foreguard upper lip','handguard',(-58,0,22.8),(58,14.8,1.6),m,.4)
for sign in [-1,1]:
    for x in [-78,-69,-60,-51]:
        s.poly('Blind oblong vent backing','handguard',[(x+3.4*math.cos(a*math.pi/16),18.2+1.65*math.sin(a*math.pi/16)) for a in range(32)],.35,s.dark,.08,y=sign*8.1)
        s.box('Raised vent lower lip','handguard',(x,sign*8.32,16.45),(5.6,.38,.6),s.edge,.22)
    s.box('Foreguard broad shallow panel','handguard',(-64,sign*8.17,9),(36,.4,5.3),m,.9)
    s.box('Foreguard panel lower pressed rib','handguard',(-64,sign*8.41,6.5),(33,.42,.7),s.edge,.21)
    for x in [-85,-32]:s.box('Handguard end band','handguard',(x,sign*8.15,12.7),(1.5,.5,18),m,.4)
    s.screw('Foreguard fixed attachment ornament','handguard',-26,17,sign*8.3,.8)
# Solid lower cylinder is sculpture only: closed, no internal helix or interface.
s.cyl('Filled lower cylindrical ornament','cylinder',(-46,0,-3.8),8.7,81,p,'X',.85,64)
s.cone('Closed cylinder rear taper','cylinder',(-3,0,-3.8),8.7,5.8,8,p,'X',.6)
s.cyl('Closed cylinder front band','cylinder',(-85.5,0,-3.8),9.2,3.4,m,'X',.4)
s.cyl('Closed cylinder front face','cylinder',(-87.3,0,-3.8),7.7,.3,p,'X',.1)
s.box('Cylinder buried upper attachment strip','cylinder',(-38,0,3.2),(83,6.5,3.5),p,.8)
for x in [-80,-69,-58,-47,-36,-25,-14]:
    for sign in [-1,1]:s.cyl('Cylinder blind surface dimple','cylinder',(x,sign*8.6,-3.8),.64,.25,s.dark,'Y',.05,24)
for x in [-82,-9]:s.cyl('Cylinder subtle molding ring','cylinder',(x,0,-3.8),8.84,.6,p,'X',.15)
# Open triangular stock is a single fixed artwork; arbitrary thick rods for small-scale durability.
s.box('Stock anchored neck block','stock',(44.5,0,6.5),(6,12,14),m,.65)
for sign in [-1,1]:
    s.line('Stock upper straight metal rod','stock',(45,sign*3.7,9),(105,sign*3.7,5),1.4,m)
    s.line('Stock diagonal metal rod','stock',(45,sign*3.7,3),(107,sign*3.7,-18),1.7,m)
s.poly('Stock fixed rear end plate','stock',[(103,8),(109,7),(109,-21),(104,-20)],11.1,p,.8)
for sign in [-1,1]:
    s.box('Stock rear shallow face strip','stock',(106,sign*5.48,-6),(2.7,.5,23),m,.5)
    s.screw('Stock neck fixed pivot ornament','stock',45,7,sign*6.15,.9)
# Angled black grip and plain fixed exterior guard.
s.poly('Angled pistol grip','grip',[(26,-3),(39,-3),(40,-11),(47,-29),(46,-34),(38,-37),(35,-34),(29,-16),(25,-10)],13.2,p,1.3)
for sign in [-1,1]:
    s.poly('Inset grip side panel','grip',[(29,-10),(36,-10),(43,-28),(42,-31),(38,-32),(32,-17)],.5,p,.65,y=sign*6.45)
    for j in range(10):s.box('Grip shallow traction stipple','grip',(32+j*.64,sign*6.77,-13-j*1.6),(3.2,.26,.46),s.metal,.13)
    s.screw('Grip fixed inset stud','grip',32,-9,sign*6.6,.63)
guard(s,[(0,-3),(28,-3),(30,-10),(26,-16),(7,-16),(2,-12)],[(4,-5),(25,-5),(27,-10),(24,-13.5),(8,-13.5),(5,-10)])
s.poly('Fixed solid trigger ornament','grip',[(14,-3),(17,-3),(18,-8),(15,-12),(12,-12),(15,-8)],2.5,m,.4)
closed_front(s,'muzzle',-110,-84,12.2,2.15)
s.box('Front sight broad fixed collar','sights',(-86,0,13.6),(4.3,16.6,22),m,.6)
s.poly('Front fixed sight blade','sights',[(-88,21),(-84,21),(-84.2,31),(-87.8,31)],3.3,m,.3)
s.box('Front blade top','sights',(-86,0,30.5),(4.2,6.8,2),m,.3)
s.box('Rear sight foot','sights',(-19,0,24),(15,8.5,3),m,.45)
s.poly('Rear leaf sight artwork','sights',[(-27,25),(-13,25),(-11,28),(-13,29),(-19,27),(-27,27)],6.4,m,.35)
optic(s,13,24)
result=finish(s,'默认图可见：四个短椭圆护木侧孔的明暗外观、圆弧顶机匣、下置长圆筒外形、倾斜黑握把和三角骨架托。圆筒仅填满的装饰形体。','https://zilliongamer.com/uploads/delta-force/weapons-builds/submachine-gun/bizon/bizon-delta-force-build.jpg')
