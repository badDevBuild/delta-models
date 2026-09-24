import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('m82',360)
panel(s,'body',[(-64,36),(141,36),(149,31),(149,17),(72,17),(54,12),(-7,12),(-8,19),(-69,19)],22,s.metal,.8)
panel(s,'handguard',[(-67,36.8),(6,36.8),(6,20),(-67,20)],23,s.metal,.7)
for sign in [-1,1]:
 for x in range(-60,5,8):s.box('Blind cooling upper slot','handguard',(x,sign*11.5,32),(5,.65,2.4),s.dark,.6)
 s.box('Long lower groove','handguard',(-32,sign*11.6,24),(61,.5,1.5),s.dark,.3)
 s.box('Closed long body panel','details',(70,sign*11.1,25),(120,.8,10),s.polymer,.4)
 s.box('Closed side ejection art','details',(61,sign*11.6,25),(27,.5,6),s.dark,.45)
 pins(s,'details',[12,37,128],25,sign*11.4)
front(s,-144,-60,30,3.3)
s.box('Sealed twin-port looking front block','barrel',(-145,0,30),(10,14,10),s.metal,.5)
for sign in [-1,1]:
 for x in [-148,-143]:s.box('Blind muzzle dark recess','barrel',(x,sign*7.05,30),(3,.4,6),s.dark,.5)
s.box('Solid front end face','barrel',(-150,0,30),(.5,13,9),s.metal,.3)
folded_bipod(s,'barrel',-61,-103,14)
magazine(s,30,15,32,30,s.polymer)
pistol_grip(s,74,15)
o=panel(s,'stock',[(106,21),(147,24),(149,18),(149,-7),(143,-9),(110,-1)],20,s.polymer,.8)
s.cut(o,s.poly('Rear exterior shoulder opening','stock',[(114,15),(141,15),(141,-1),(115,4)],30,s.dark,.8))
s.box('Tall butt cushion','stock',(149,0,15),(4,23,47),s.rubber,1)
s.box('Raised cheek face','stock',(119,0,37),(42,23,3),s.polymer,.6)
sights(s,-59,125,38)
result=finalize(s)
