import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('qjb201',330)
box_receiver(s,-29,84,24)
panel(s,'body',[(-39,28),(-23,43),(-7,43),(4,35),(26,35),(29,43),(64,43),(76,36),(85,33),(84,17),(-30,17)],20,s.metal,.8)
panel(s,'handguard',[(-105,29),(-96,34),(-41,34),(-29,23),(-35,14),(-105,16)],21,s.polymer,1)
for sign in [-1,1]:
 panel(s,'handguard',[(-98,28),(-81,28),(-72,20),(-84,24),(-98,22)],.8,s.edge,.4).location.y=sign*10.5
 for x in range(-73,-40,3):s.box('Fine rectangular grip ribs','handguard',(x,sign*10.7,24),(1,.5,8),s.edge,.2)
 s.box('Forebed dark lower seam','handguard',(-70,sign*10.9,18),(59,.35,1.1),s.dark,.15)
front(s,-150,-100,32,2.7)
s.cyl('Lower sealed short rod','barrel',(-95,0,22),2.5,51,s.metal,'X',.2)
s.box('Front rod bridge','barrel',(-118,0,27),(4,8,13),s.metal,.5)
skeleton_stock(s,81,149)
pistol_grip(s,59,12)
s.box('Closed decorative ribbon','details',(8,-11.5,25),(22,8,29),s.metal,.6)
for z in range(14,40,4):s.box('Belt shallow golden bars','details',(8,-15.7,z),(17,.6,1.8),s.tan,.45)
s.box('Olive fabric block','magazine',(6,-3,-11),(28,27,36),s.fabric,3)
s.box('Fixed fabric upper lid','magazine',(6,-3,10),(28.5,27.5,10),s.polymer,2)
s.box('Fabric front overlap','magazine',(6,-16.4,-9),(22,.9,25),s.green,2)
s.box('Fabric closing tongue','magazine',(7,-17,-22),(4,1,8),s.tan,.5)
sights(s,-116,70,44)
# High rail is seated on the angular stepped body and handguard through shallow support.
s.box('Fore rail riser','sights',(-62,0,37),(93,7,13),s.metal,.65)
s.box('Rear rail riser','sights',(38,0,42),(68,8,5),s.metal,.4)
result=finalize(s)
