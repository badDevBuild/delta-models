import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('vss',300)
box_receiver(s,-10,63,24)
s.cyl('Rounded upper crown','body',(27,0,33),5.2,72,s.metal,'X',.35)
for x in range(-4,62,10):s.box('Stamped upper shallow rib','body',(x,0,36.4),(1.8,8,1.3),s.edge,.2)
panel(s,'handguard',[(-48,29),(-11,29),(-8,13),(-46,15)],19,s.polymer,1.1)
for sign in [-1,1]:
 for x in range(-43,-14,4):s.box('Handguard narrow relief','handguard',(x,sign*9.5,22),(1.4,.75,10),s.edge,.2)
front(s,-150,-43,26,7.2)
for x in [-146,-115,-91,-65,-49]:s.cyl('Closed front external band','barrel',(x,0,26),7.8,4,s.metal,'X',.25)
for sign in [-1,1]:
 for x in [-122,-118,-114]:s.box('Front shallow dark score','barrel',(x,sign*7.1,26),(1.1,.6,5),s.dark,.12)
o=panel(s,'stock',[(60,28),(74,25),(146,24),(149,20),(149,-19),(143,-22),(68,-22),(60,-13),(53,5)],19,s.wood,1.1)
for pts in [[(72,18),(96,18),(88,-15),(70,-15),(65,-2)],[(101,18),(139,17),(139,-13),(137,-16),(93,-16)]]:s.cut(o,s.poly('Wood open sculpture cutout','stock',pts,30,s.dark,1.7))
s.box('Wood grip heel','grip',(64,0,-21),(14,19.5,3),s.wood,1)
s.box('Rubber shoulder edge','stock',(149,0,1),(3,20,45),s.rubber,.65)
for sign in [-1,1]:
 s.line('Wood top longitudinal relief','stock',(77,sign*9.5,22),(141,sign*9.5,21),.15,s.woodlight)
 s.line('Wood lower longitudinal relief','stock',(77,sign*9.5,-19),(140,sign*9.5,-19),.15,s.woodlight)
magazine(s,6,13,23,24,s.polymer,5)
guard(s,29,11,23)
sights(s,-141,55,35,False)
# Sight at the front has a pedestal intersecting the sealed cylinder.
s.box('Front blade extended pedestal','sights',(-138,0,33),(5,5,8),s.metal,.4)
result=finalize(s)
