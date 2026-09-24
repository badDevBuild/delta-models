import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('marlin',320)
box_receiver(s,0,48,24)
# Smooth closed receiver with visual loading plate, not an opening.
for sign in [-1,1]:
 s.box('Blind side plate','details',(24,sign*9.3,24),(23,.7,6),s.dark,1.5)
 s.box('Side plate highlight','details',(24,sign*9.6,23),(17,.25,1.2),s.steel,.3)
panel(s,'handguard',[(-89,29),(-2,29),(2,26),(2,13),(-83,13),(-90,17)],18,s.polymer,1.4)
s.cyl('Front handguard external collar','handguard',(-88,0,22),9.3,4,s.metal,'X',.3)
front(s,-150,-83,28,2.9)
s.cyl('Solid lower decorative rod','barrel',(-95,0,21),2.8,104,s.metal,'X',.2)
s.box('End bridge','barrel',(-144,0,24),(3,6,8),s.metal,.4)
traditional(s,44,149,s.polymer)
guard(s,22,12,24)
o=panel(s,'grip',[(40,6),(53,7),(70,-4),(80,-14),(73,-23),(67,-25),(54,-16),(45,-7)],5.5,s.metal,.8)
s.cut(o,s.poly('Large lever display opening','grip',[(45,3),(52,3),(68,-7),(75,-14),(70,-19),(67,-20),(58,-13),(50,-4)],15,s.dark,.6))
s.box('Lower receiver shallow cover','magazine',(17,0,11),(27,11,3.5),s.metal,.7)
pins(s,'magazine',[7,27],12,5.5)
sights(s,-140,42,36,False)
s.box('Front sight bridge','sights',(-137,0,32),(6,5,9),s.metal,.4)
result=finalize(s)
