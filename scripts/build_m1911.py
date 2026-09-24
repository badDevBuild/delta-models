"""Independent game-inspired M1911 miniature exterior, not functional geometry."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_compact_helpers import finish,optic
s=Sculpture('m1911',85)
for k,l,v in [('frame','纤细下框与固定护圈',True),('slide','斜纹上壳外观',True),('front','封闭前端与短下颏',True),('grip_panels','橄榄棕格纹握把面板',True),('base','实心握把底缘',True),('controls','固定侧面操控装饰',True),('sights','低矮机械瞄具',True),('optic','可选微型光学装饰',False)]:s.part(k,l,v)
blue=s.mat('Blued satin steel',(.058,.074,.083),.78,.32)
olive=s.mat('Olive brown grip',(.22,.20,.125),0,.7)
check=s.mat('Olive raised checkering',(.16,.145,.091),0,.73)
slide=s.poly('Long rounded closed slide','slide',[(-42.5,24),(-42.5,30),(-40,33),(-9,33),(-6,32.3),(28,32.3),(31,28),(31,22.5),(-40,22.5)],11.8,blue,.75)
s.box('Long slide upper reflection','slide',(-8,0,32.8),(70,7.0,.7),s.metal,.3)
for side in [-1,1]:
    for start,count in [(-39,8),(15,9)]:
        for i in range(count):
            x=start+i*1.35
            s.cut(slide,s.poly('Blind angled slide serration','slide',[(x,30.8),(x+.65,30.8),(x+2.7,24),(x+2.05,24)],.7,s.dark,.12,y=side*5.83))
    s.box('Unlettered shallow side field','slide',(-6,side*5.88,27.7),(26,.12,2),s.metal,.16)
# Right-sided shallow top port relief remains a filled surface.
s.poly('Closed upper panel inset','slide',[(-1,32.1),(12,32.1),(12,29),(10,28.2),(0,28.2)],.25,s.steel,.25,y=5.9)
s.box('Top panel shallow seam','slide',(5.5,0,33.1),(13,6.1,.18),s.steel,.22)
s.poly('Solid lower exterior frame','frame',[(-41,22.6),(27,22.6),(31,20),(36,19.8),(42.5,22.5),(42.3,20.5),(35,17),(28,16),(20,15),(13,18),(-39,18)],10.7,blue,.6)
s.poly('Angled complete grip core','frame',[(21,19),(32,18),(31,8),(34,-4),(41,-25),(39,-28),(22,-28),(20,-23),(16,-9),(14,1),(15,12)],11.0,s.metal,.8)
s.poly('Backstrap sculpted edge','frame',[(30,16),(32,14),(33,4),(36,-8),(41,-24),(38,-27),(34,-23),(29,-5)],11.5,blue,.65)
guard=s.poly('Fixed exterior trigger guard','frame',[(-4,19),(18,18),(20,10),(17,2),(13,0),(2,0),(-4,4),(-6,10)],6.2,blue,.6)
s.cut(guard,s.poly('Exterior guard silhouette opening','frame',[(-2,16),(13,15),(16,10),(13,4),(4,3),(-1,6)],15,s.dark,.65))
s.poly('Fixed sculpted trigger','controls',[(9,17),(12,16),(13,12),(12,6),(9,5),(8,6),(10,9),(10,13)],3.0,s.steel,.4)
for z in [8,11,14]:
    for side in [-1,1]:s.cyl('Trigger blind decorative spot','controls',(11,side*1.51,z),.65,.12,s.dark,'Y',.05,24)
s.cyl('Filled upper muzzle face','front',(-42.6,0,28),4.35,.32,s.steel,'X',.22)
s.cyl('Opaque closed muzzle inset','front',(-42.79,0,28),2.7,.10,s.dark,'X',.1)
s.cyl('Lower closed rounded chin','front',(-40,0,20.4),3.3,5.1,blue,'X',.25)
for side in [-1,1]:
    s.poly('Olive grip outer cover','grip_panels',[(20,14),(29,14),(29,6),(32,-4),(38,-23),(35,-25),(24,-25),(21,-20),(17,-3),(17,6)],1.4,olive,.6,y=side*5.45)
    s.poly('Inset grip checkering field','grip_panels',[(21,11),(27,11),(28,3),(31,-8),(35,-22),(25,-23),(23,-18),(19,-2),(19,5)],.25,check,.45,y=side*6.17)
    for row in range(19):
        z=9-row*1.6;shift=max(0,-z)*.20
        for col in range(5):
            x=20.0+shift+col*1.35
            obj=s.box('Small grip diamond relief','grip_panels',(x,side*6.34,z),(.66,.20,.66),olive,.1);obj.rotation_euler[1]=math.pi/4
    s.screw('Upper grip panel screw','grip_panels',24,11,side*6.3,.94)
    s.screw('Lower grip panel screw','grip_panels',29.5,-21.5,side*6.3,.94)
    s.poly('Fixed slide stop lever','controls',[(5,21),(16,21),(16,19),(12,18.5),(5,19)],.7,s.metal,.3,y=side*5.5)
    s.cyl('Fixed lower round button','controls',(16.8,side*5.8,13),1.15,.65,s.steel,'Y',.15)
    s.poly('Fixed thumb ledge','controls',[(25,21),(32,21),(33,19.4),(28,18.8),(25,19.5)],.9,blue,.3,y=side*5.7)
    s.screw('Small frame cosmetic pin','controls',22,18,side*5.6,.55)
s.poly('Solid rear crest silhouette','controls',[(31,23),(32,26),(36,28),(39,26),(38,23),(36,22)],4.1,s.metal,.45)
# Filled dark marking gives the ring appearance without a functional opening.
for side in [-1,1]:s.cyl('Crest blind round inset','controls',(35.7,side*2.1,25.1),1.4,.12,s.dark,'Y',.1)
s.poly('Solid black grip bottom','base',[(22,-27),(40,-27),(42,-29),(41,-30),(21,-30),(20,-28)],12.5,s.polymer,.5)
s.box('Front low sight','sights',(-39,0,34),(3.9,2.4,2.2),s.polymer,.28)
s.poly('Sloping rear sight','sights',[(24,32),(25,36),(29,35),(31,32)],6,s.polymer,.35)
for side in [-1,1]:s.box('Rear sight bright pin','sights',(28.3,side*2,35.1),(.75,.75,.25),s.steel,.12)
optic(s,'optic',9,33.7,.63)
result=finish(s,'https://www.imfdb.org/images/thumb/a/a3/DFHO_M1911.jpg/600px-DFHO_M1911.jpg',['保留游戏黑色纤细上壳、前后斜纹、橄榄棕格纹双侧握把、薄护圈与后方固定环状装饰轮廓。','握把菱纹为几何浅浮雕；光学附件为自定缩比外观，底座贴合上壳。'])
