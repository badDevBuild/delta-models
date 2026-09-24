"""Chrome-and-walnut game-inspired Desert Eagle miniature, closed exterior art."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch3_mixed_helpers import finish
s=Sculpture('desert_eagle',90)
for key,label,show in [('frame','银色厚框架外观',True),('barrel','封闭方棱前端',True),('slide','银色后段外壳',True),('grip_panels','棕色格纹握把面板',True),('base','黑色实心底座',True),('sights','固定机械瞄具',True),('light','可选灯具装饰',False)]:s.part(key,label,show)
chrome=s.mat('Brushed pale chrome',(.52,.57,.60),.82,.29)
edge=s.mat('Cool chrome facets',(.36,.41,.44),.82,.35)
wood=s.mat('Brown grip polymer',(.20,.072,.028),0,.60)
woodlight=s.mat('Raised copper-brown checkering',(.285,.126,.054),0,.57)
black=s.mat('Black steel components',(.025,.032,.036),.5,.43)
# The distinctive long squared front is solid all the way through.
front=s.poly('Solid squared forward exterior','barrel',[(-45,30),(-44,34),(1,34),(4,32),(5,23),(-41,23),(-44,25)],15.0,chrome,.65)
s.poly('Forward upper bevel plane','barrel',[(-44,32),(-43,34),(1,34),(3,32)],11.8,edge,.23)
s.box('Long front top flat','barrel',(-21,0,34.05),(43,7.6,.35),chrome,.15)
s.box('Front closed black inset','barrel',(-45.1,0,29.2),(.20,7.7,5.8),black,.9)
s.box('Front solid reflected face','barrel',(-45.22,0,29.2),(.12,4.8,3.6),s.dark,.65)
for side in [-1,1]:
    s.poly('Long forward side shoulder','barrel',[(-35,29),(-3,29),(0,31),(0,26),(-39,26)],.36,edge,.35,y=side*7.51)
    s.box('Blind short top transition','barrel',(2.5,side*7.48,32),(3.8,.45,3.4),s.dark,.3)
# Filled rear cover with deep-looking but blind diagonal serrations.
rear=s.poly('Solid silver rear cover','slide',[(2,32),(7,34),(31,34),(34,31),(36,22),(7,22),(5,25)],15.5,chrome,.65)
for side in [-1,1]:
    for i in range(9):
        x=9+i*2.1
        s.cut(rear,s.poly('Rear blind diagonal serration','slide',[(x,32.5),(x+.75,32.5),(x+3.1,23.7),(x+2.35,23.7)],.65,s.dark,.12,y=side*7.65))
    s.poly('Black selector plate','slide',[(25,31),(28,33),(33,32),(34,28),(31,27),(27,28)],.8,black,.55,y=side*7.81)
    s.cyl('Fixed round selector stud','slide',(30,side*8.46,30),1.3,.7,s.steel,'Y',.2)
    s.box('Fixed selector lower lever','slide',(27.1,side*8.5,28.5),(5.5,.85,1.15),black,.3)
s.box('Closed top transition shadow','slide',(5.2,0,33.8),(7.8,8.3,.7),black,.3)
s.box('Closed top transition chrome','slide',(5.2,0,34.15),(4.9,5.2,.5),s.steel,.2)
s.poly('Fixed rear crest ornament','slide',[(33,24),(36,23),(40,24),(40,25.5),(37,27),(34,27)],6.5,black,.4)
# One filled frame carries the lower front rail and broad backstrap.
s.poly('Silver lower frame','frame',[(-43,23.4),(33,23.4),(35,20),(37,18),(45,17),(39,15),(31,15),(25,13),(18,13),(14,16),(2,17),(-43,18)],14.6,chrome,.65)
s.poly('Silver grip core','frame',[(19,19),(32,18),(33,10),(34,0),(39,-19),(37,-22),(21,-22),(16,-19),(16,-13),(17,-3),(16,9)],13.8,chrome,.9)
s.poly('Black front grip strap','frame',[(17,12),(20,11),(20,1),(19,-10),(20,-19),(18,-20),(15,-17),(15,-11),(16,-2),(15,8)],12.8,black,.6)
for side in [-1,1]:
    s.screw('Frame tiny cosmetic pin','frame',-2,19.8,side*7.34,.64)
    s.box('Blank receiver engraving field','frame',(-17,side*7.36,20.8),(16,.15,1.8),edge,.22)
    s.poly('Fixed frame side lever','frame',[(15,21),(24,21),(26,19),(23,18),(16,19)],.8,black,.35,y=side*7.3)
    s.cyl('Fixed round frame button','frame',(18,side*7.65,14),1.1,.8,black,'Y',.18)
s.box('Solid lower decorative rail','frame',(-24,0,18.0),(36,9.1,2.0),edge,.4)
for i in range(12):s.box('Lower rail shallow cross relief','frame',(-41+i*2.9,0,17.05),(1.6,10,.6),black,.15)
guard=s.poly('Fixed thick exterior guard','frame',[(-2,18),(18,18),(20,11),(17,2),(13,1),(-1,2),(-3,5)],7.0,chrome,.65)
s.cut(guard,s.poly('Open exterior guard silhouette','frame',[(1,15),(14,15),(16,11),(14,5),(11,4),(1,5)],18,s.dark,.6))
s.poly('Fixed black trigger ornament','frame',[(8,16),(11,16),(12,11),(10,6),(7,5),(6,6.3),(8.5,9),(9,12)],2.8,black,.4)
# Separate brown covers with inset perimeter and fine raised checkering.
for side in [-1,1]:
    s.poly('Brown grip panel outer','grip_panels',[(20,12),(30,13),(30.5,5),(32,-4),(36,-18),(34,-20),(22,-20),(19,-17),(19,-8)],1.6,wood,.7,y=side*7.2)
    s.poly('Grip checkering field','grip_panels',[(21,10),(28.5,11),(29,3),(31,-5),(34,-17),(23,-18),(21,-15),(21,-7)],.3,woodlight,.5,y=side*8.04)
    for row in range(20):
        z=9-row*1.3
        shift=max(0,-z)*.10
        for col in range(6):
            x=21.7+shift+col*1.15
            obj=s.box('Grip fine diamond checkering','grip_panels',(x,side*8.23,z),(.65,.25,.65),wood,.1)
            obj.rotation_euler[1]=math.pi/4
    s.screw('Grip top chrome pin','grip_panels',24.6,10.2,side*8.22,.88)
    s.screw('Grip bottom chrome pin','grip_panels',27.8,-17.5,side*8.22,.88)
s.poly('Solid black grip base','base',[(20,-21),(37,-21),(39,-23),(37,-24),(20,-24),(18,-22.5)],15.7,black,.5)
s.box('Base slim chrome edge','base',(28.8,0,-23.4),(18.3,16.0,.6),edge,.22)
# Small low default sights; solid inlays rather than viewing channels.
s.box('Front sight foot','sights',(-41,0,34.8),(3.8,3.8,1.3),black,.25)
s.poly('Front sight angled crest','sights',[(-42,35),(-41,37.2),(-39,37.2),(-38.5,35)],2.2,black,.25)
s.box('Rear sight foot','sights',(29,0,35),(4.7,8.1,1.5),black,.3)
for side in [-1,1]:s.box('Rear fixed sight wing','sights',(29,side*2.4,36.2),(2.8,1.8,2.3),black,.3)
# Optional small solid light, artist-scale foot seats against the lower rail.
s.box('Optional light contact base','light',(-24,0,16),(16,9,2.8),black,.45)
s.box('Optional light shell','light',(-24,0,11.5),(14,11,7),s.polymer,.9)
s.cyl('Optional light front ring','light',(-32,0,11.5),4.9,3.5,black,'X',.35)
s.cyl('Optional light opaque lens','light',(-33.85,0,11.5),3.7,.28,s.glass,'X',.1)
for side in [-1,1]:s.box('Optional light button','light',(-20,side*5.7,11.6),(3.6,.65,2.2),s.metal,.3)
result=finish(s,'https://www.imfdb.org/images/thumb/f/f9/DFHO_DesertEagle.jpg/600px-DFHO_DesertEagle.jpg',['依据游戏默认银色厚前端、斜切后壳、黑色固定小件、棕色格纹握把和底部短轨重新雕塑；未采用纯黑现实参考替代。','可选灯具为封闭不发光的数字外观附件；所有握把与壳体组均为无内部构造的实心装饰。'])
