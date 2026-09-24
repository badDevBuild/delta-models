"""MP7 solid miniature exterior, independently reconstructed from game screenshot."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch3_smg_helpers import Sculpture,optic,guard,closed_front,finish
s=Sculpture('mp7',170)
for k,l,v in [('receiver','分层聚合物外壳',True),('forebody','前护壳与折叠握把外观',True),('stock','细杆伸展托外观',True),('grip','握把及固定护圈',True),('magazine','短实心弹匣底座',True),('muzzle','封闭短前端',True),('sights','固定前后瞄具',True),('optic','可选数字微型瞄具',False)]:s.part(k,l,v)
p=s.mat('MP7 charcoal polymer',(.043,.051,.055),.02,.66)
body=s.poly('Angular receiver silhouette','receiver',[(-67,13),(-63,17),(38,17),(40,14),(40,-7),(-4,-7),(-9,-3),(-67,-3)],13.8,p,.85)
s.box('Receiver upper lid','receiver',(-12,0,16.5),(103,11.9,2.4),p,.5)
for sign in [-1,1]:
    s.poly('Molded upper side recessed surface','receiver',[(-61,12),(-11,12),(-8,7),(24,7),(28,10),(38,10),(38,14),(-61,14)],.42,s.metal,.35,y=sign*6.81)
    s.poly('Receiver side stepped panel','receiver',[(-59,10),(-25,10),(-22,8),(-6,8),(-6,6),(-57,6),(-61,7)],.35,p,.3,y=sign*7.04)
    s.box('Solid side blind long slot','receiver',(17,sign*7.1,8.1),(30,.25,1.5),s.dark,.3)
    s.box('Receiver lower molded stripe','receiver',(18,sign*6.95,-3),(38,.3,1),s.metal,.18)
    for x,z in [(-58,0),(-29,.5),(2,-1),(35,-4.4),(36,13)]:s.screw('Fixed receiver exterior pin','receiver',x,z,sign*6.95,.69)
    s.poly('Raised fixed selector','receiver',[(-6,-1),(0,-1),(2,-2.3),(0,-3.7),(-6,-3.2)],.7,s.metal,.3,y=sign*7)
    for i in range(5):s.box('Abstract side label','receiver',(10+i*1.5,sign*7.12,-.4),(.8,.12,.26),s.edge,.04)
s.rail('receiver',-58,36,18,7,3)
# Folded broad front handgrip represented as joined exterior shell.
s.poly('Angular solid forebody','forebody',[(-69,5),(-65,8),(-9,7),(-6,1),(-13,-3),(-64,-3),(-69,-8)],14.4,p,.65)
for sign in [-1,1]:
    s.box('Front shallow slot','forebody',(-56,sign*7.23,5),(8,.25,2),s.dark,.55)
    s.poly('Folded foregrip upper panel','forebody',[(-64,0),(-15,0),(-11,-2),(-63,-2)],.5,s.metal,.3,y=sign*7.08)
    for x in [-62,-15]:s.screw('Forebody blind pin','forebody',x,-.9,sign*7.25,.62)
# Thin extended stock rods are continuous to receiver; buttplate is a solid thin wedge.
for sign in [-1,1]:s.box('Solid extended stock rail','stock',(58.4,sign*4.4,6.5),(42,2.6,2.5),s.metal,.6)
s.poly('Rear stock upright','stock',[(76.4,11),(82.5,10.5),(84,8),(83,-19),(79,-21),(77,-16)],10.8,p,1.0)
s.box('Rear rubber face','stock',(83.1,0,-4.7),(2.2,11.4,29),s.rubber,.65)
for sign in [-1,1]:
    s.poly('Stock shallow side web','stock',[(78,7),(81,7),(81,-13),(79,-16)],.6,s.metal,.4,y=sign*5.2)
    s.screw('Stock closed mounting ornament','stock',79,7,sign*5.6,.75)
for z in [-15,-11,-7,-3,1,5]:s.box('Stock pad transverse ribs','stock',(84,0,z),(.5,10,.8),p,.2)
# Central grip has a short magazine almost fully hidden by its solid exterior.
s.poly('One piece central grip exterior','grip',[(-5,-5),(9,-5),(10,-11),(8,-26),(8,-38),(4,-40),(-10,-40),(-11,-37),(-8,-23),(-8,-12)],13,p,.9)
for sign in [-1,1]:
    s.poly('Grip subtly raised side panel','grip',[(-5,-13),(6,-13),(5,-36),(-7,-37),(-6,-27)],.55,p,.5,y=sign*6.3)
    for row in range(15):
        z=-15-row*1.3
        s.box('Shallow front grip traction','grip',(-4,sign*6.67,z),(3.1,.2,.45),s.metal,.14)
    for row in range(5):s.box('Grip base lateral relief','grip',(1,sign*6.67,-31-row*1.2),(8,.25,.42),s.metal,.14)
    s.screw('Grip fixed blind button','grip',-5,-11,sign*6.6,.62)
guard(s,[(-25,-2),(-7,-3),(-4,-7),(-7,-13),(-23,-13),(-27,-9)],[(-24,-4),(-9,-4),(-7,-7),(-9,-10.6),(-22,-10.6),(-24,-8)])
s.poly('Fixed trigger silhouette','grip',[(-15,-2),(-12,-3),(-12,-7),(-15,-10),(-17,-10),(-14,-7)],2.8,s.metal,.4)
s.box('Solid magazine bottom','magazine',(-1,0,-40),(20,13.5,3),s.metal,.55)
for sign in [-1,1]:s.box('Magazine bottom seam','magazine',(-1,sign*6.8,-40),(18,.2,.5),s.dark,.1)
closed_front(s,'muzzle',-85,-67,1,2.4)
for x in [-61,29]:
    s.box('Fixed sight broad foot','sights',(x,0,19.6),(9,8.8,2.1),s.metal,.4)
    s.poly('Fixed upright sight blade','sights',[(x-1.8,20),(x+1.8,20),(x+1.3,28),(x-1.3,28)],2.8,s.metal,.3)
    s.box('Fixed sight blade top','sights',(x,0,26.5),(2.9,5.4,2.3),s.metal,.3)
optic(s,-3,20)
result=finish(s,'默认图可见：短矩形阶梯外壳、长顶部浅齿、展开细杆托、短前端、折合前握把外观，以及短弹匣藏入直握把；按该基础配置建模。','https://zilliongamer.com/uploads/delta-force/weapons-builds/submachine-gun/mp7/mp7-delta-force.jpg')
