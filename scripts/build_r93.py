import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('r93',350)
panel(s,'body',[(-11,34),(57,34),(73,26),(72,7),(-20,10),(-30,14),(-24,28)],20,s.polymer,1)
s.cyl('Solid straight receiver crown','details',(28,0,33),5,67,s.metal,'X',.35)
for sign in [-1,1]:
 panel(s,'details',[(-12,26),(16,26),(13,13),(-16,15)],.9,s.metal,.4).location.y=sign*10
 panel(s,'details',[(23,26),(58,26),(68,18),(66,12),(20,12)],.9,s.metal,.4).location.y=sign*10
s.line('Fixed diagonal charging handle','details',(49,-3,30),(47,-14,23),1.4,s.steel)
s.cyl('Fixed handle knob','details',(47,-14,23),2.3,4,s.polymer,'Y',.4)
panel(s,'handguard',[(-67,21),(-23,28),(-20,10),(-65,14)],16,s.polymer,.8)
front(s,-150,-14,32,3.1)
folded_bipod(s,'handguard',-28,-65,12)
panel(s,'stock',[(69,21),(83,12),(99,10),(110,22),(148,23),(149,-15),(111,-14),(89,-5),(76,-4)],21,s.polymer,1.4)
s.box('Tall cheek rest','stock',(121,0,22),(32,22,12),s.polymer,.8)
s.box('Wide textured rubber shoulder','stock',(149,0,6),(3,22,41),s.rubber,.6)
for x in [119,129,139]:s.box('Shoulder grip rib','stock',(x,0,3),(1.1,22,17),s.rubber,.25)
panel(s,'grip',[(74,10),(88,10),(88,-23),(76,-22)],14,s.polymer,1.1)
s.box('Fixed grip heel','grip',(83,0,-23),(20,18,3),s.polymer,.6)
guard(s,49,11,24)
s.box('Shallow flush bottom plate','magazine',(23,0,9),(27,13,5),s.metal,.6)
pins(s,'magazine',[14,30],9,6.5)
s.box('Fixed top saddle','sights',(23,0,36),(60,7,6),s.metal,.4)
s.rail('sights',-6,54,39,7,4)
scope(s,'optic',25,42,56)
# Keep this purely decorative glue plane clear of shallow surface details.
result=finalize(s,cutplane_mm=-12.3)
