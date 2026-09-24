"""UZI game-reference solid sculpture with the observed fixed wooden stock."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from batch3_smg_helpers import Sculpture,wood,optic,guard,closed_front,finish
s=Sculpture('uzi',160)
for k,l,v in [('receiver','冲压外壳与浅肋',True),('handguard','横纹聚合物护木',True),('stock','固定木制枪托',True),('grip','中央握把及固定护圈',True),('magazine','直形实心弹匣外观',True),('muzzle','封闭细前端',True),('sights','前后固定瞄具',True),('optic','可选数字微型瞄具',False)]:s.part(k,l,v)
w=wood(s);p=s.mat('UZI black molded polymer',(.042,.049,.049),.015,.7);m=s.mat('UZI worn dark steel',(.061,.070,.073),.72,.43)
s.poly('Main stamped rectangular body','receiver',[(-54,13),(-51,16),(11,16),(15,14),(30,14),(30,-1),(-48,-1),(-54,2)],13.6,m,.55)
s.box('Top folded steel lid','receiver',(-12,0,15.4),(77,11.8,1.8),m,.45)
for sign in [-1,1]:
    s.poly('Pressed side edge band','receiver',[(-51,2),(28,2),(28,13),(-49,13)],.4,m,.32,y=sign*6.75)
    for a,b,z in [(-28,-3,10),(-23,-3,6),(11,24,10),(11,24,6)]:
        s.box('Pressed longitudinal blind channel','receiver',((a+b)/2,sign*7,z),(b-a,.25,1.2),s.dark,.42)
        s.box('Channel softened edge','receiver',((a+b)/2,sign*7.08,z+.6),(b-a-1,.35,.42),s.edge,.17)
    s.box('Lower receiver pressed seam','receiver',(-3,sign*7.0,1.3),(62,.35,.62),s.edge,.16)
    for x,z in [(-37,12),(-16,1.5),(5,5),(25,11)]:s.screw('Exterior fixed steel rivet','receiver',x,z,sign*6.98,.55)
    s.cyl('Blind circular receiver ornament','receiver',(1,sign*7.1,7.5),2.9,.25,s.dark,'Y',.1)
    s.cyl('Raised receiver oval core','receiver',(1,sign*7.24,7.5),2.2,.35,m,'Y',.1)
    for n in range(5):s.box('Abstract manufacturer dashes','receiver',(21+n*1.1,sign*7.09,4.3),(.65,.1,.24),s.edge,.03)
s.box('Fixed top handle pedestal','receiver',(-30,0,17.1),(6.7,7.0,2.3),m,.5)
s.cyl('Fixed top charging knob artwork','receiver',(-30,0,18.8),1.45,3.4,m,'Z',.25)
# Black ribbed front handguard remains attached to the body along its full upper edge.
s.poly('Short polymer handguard','handguard',[(-54,8),(-26,8),(-24,5),(-24,-3),(-46,-3),(-54,-1)],15.4,p,.9)
for sign in [-1,1]:
    s.poly('Front grip panel','handguard',[(-50,6),(-28,6),(-27,-1),(-48,-1)],.55,p,.4,y=sign*7.5)
    for i in range(18):s.box('Fine handguard vertical grip rib','handguard',(-47+i*1.05,sign*7.78,2.4),(.42,.35,6.0),s.metal,.14)
    for x in [-49,-27]:s.screw('Handguard closed stud','handguard',x,-.5,sign*7.78,.58)
# The screenshot shows a solid fixed wooden stock, not a folding metal stock.
s.poly('Fixed wooden stock silhouette','stock',[(29,10),(41,10),(52,6.9),(64,7.4),(78,7.8),(80,5),(79,-21),(74,-22),(68,-19),(57,-10),(46,-5),(30,-4),(22,-1)],15.6,w,1.5)
s.poly('Wood stock lower neck','stock',[(22,-.5),(31,-.5),(41,-3),(45,-5),(29,-4)],13.8,w,.65)
s.poly('Stock rubber rear pad','stock',[(78,7.5),(80,6),(79.2,-21),(77.6,-21.7)],16.1,s.rubber,.65)
for sign in [-1,1]:
    s.box('Stock shallow closed sling plate','stock',(56,sign*7.83,-1),(8,.33,2),m,.55)
    for x in [53,59]:s.screw('Stock cosmetic plate screw','stock',x,-1,sign*8.02,.42)
# Straight central grip and extended narrow solid magazine.
s.poly('Grip housing neck','grip',[(-15,1),(4,1),(5,-4),(0,-8),(-13,-8)],13.2,m,.65)
s.poly('Central black pistol grip','grip',[(-12,-4),(0,-4),(1,-13),(2,-25),(0,-29),(-11,-29),(-13,-26)],13.3,p,.8)
for sign in [-1,1]:
    s.poly('Grip molded side panel','grip',[(-10,-8),(-1,-8),(0,-24),(-2,-26),(-10,-26)],.55,p,.6,y=sign*6.5)
    for row in range(14):s.box('Grip narrow transverse traction','grip',(-6,sign*6.86,-9.2-row*1.1),(6.4,.23,.42),s.metal,.13)
    s.screw('Grip side cosmetic fastener','grip',-1,-17,sign*6.79,.68)
    s.box('Fixed grip catch ornament','grip',(-9,sign*6.87,-26),(3,.6,3),m,.3)
guard(s,[(-28,0),(-12,0),(-11,-9),(-15,-13),(-27,-13),(-29,-10)],[(-26,-2),(-14,-2),(-13,-8),(-16,-10.7),(-26,-10.7)])
s.poly('Fixed trigger artwork','grip',[(-20,-1),(-18,-1),(-17,-6),(-20,-9),(-22,-9),(-19,-6)],2.4,m,.3)
s.box('Solid straight magazine','magazine',(-6,0,-32.5),(8.4,9.0,23),m,.55)
s.box('Magazine solid floor cap','magazine',(-6,0,-44),(9.9,10.2,1.9),m,.4)
for sign in [-1,1]:
    s.box('Magazine shallow recessed strip','magazine',(-6,sign*4.5,-36),(5.4,.2,12),s.dark,.25)
    for x in [-8.2,-3.8]:s.box('Magazine raised edge fold','magazine',(x,sign*4.61,-36),(.52,.35,12.2),s.edge,.15)
closed_front(s,'muzzle',-80,-53,5.6,2)
s.cyl('Front receiver decorative collar','muzzle',(-56,0,5.6),3.5,5.8,m,'X',.3)
for x in [-51,24]:
    s.box('Sight foot attached to lid','sights',(x,0,16.5),(7,10,2.1),m,.35)
    for sign in [-1,1]:s.poly('Fixed steel sight protective ear','sights',[(x-2.5,17),(x+2.5,17),(x+2,22),(x-1.4,22)],1.4,m,.25,y=sign*3.4)
    s.box('Fixed sight center post','sights',(x,0,19),(1.5,1.5,5),m,.2)
optic(s,3,17)
result=finish(s,'默认图可见：短方形机匣的横向压筋、中央直握把与外露直弹匣、黑色横纹护木、细短前端，以及棕色固定宽木枪托。','https://zilliongamer.com/uploads/delta-force/weapons-builds/submachine-gun/uzi/uzi-delta-force.jpg')
