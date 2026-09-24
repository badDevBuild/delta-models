import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('svch',330)
box_receiver(s,-14,80,23)
panel(s,'handguard',[(-72,31),(-60,36),(-16,36),(-10,29),(-14,12),(-72,13)],20,s.metal,.7)
for sign in [-1,1]:
 s.box('Textured handguard panel','handguard',(-43,sign*10,25),(39,1,8),s.polymer,.75)
 for x in range(-62,-23,4):s.box('Handguard molded rib','handguard',(x,sign*10.5,25),(1.6,.55,7),s.edge,.2)
 for x in range(-61,-18,6):s.cyl('Blind top ventilation circles','handguard',(x,sign*9.7,33),1.4,.5,s.dark,'Y',.1,24)
front(s,-150,-62,28,4)
for i in range(36):
 x=-144+i*2
 for sign in [-1,1]:s.line('Decorative sealed spiral score','barrel',(x,sign*3.7,29.6),(x+1.5,sign*3.7,26.4),.15,s.steel)
s.cyl('Solid front end band','barrel',(-146,0,28),4.5,7,s.metal,'X',.3)
# Integral visual foregrip frame based on the promotional configuration.
o=panel(s,'handguard',[(-62,16),(-14,16),(-18,-10),(-29,-17),(-40,-11),(-54,1)],14,s.polymer,.8)
s.cut(o,s.poly('Decorative foregrip window','handguard',[(-46,10),(-23,10),(-25,-7),(-31,-11),(-37,-6)],25,s.dark,.8))
magazine(s,7,11,27,37,s.polymer,11)
o=panel(s,'grip',[(57,12),(72,12),(86,-23),(66,-28)],14,s.polymer,.8)
for pts in [[(62,6),(70,6),(75,-5),(65,-7)],[(67,-12),(78,-10),(82,-20),(69,-23)]]:s.cut(o,s.poly('Fixed grip sculpture openings','grip',pts,24,s.dark,.5))
guard(s,34,11,24)
skeleton_stock(s,80,149)
s.box('Continuous receiver crown','body',(33,0,34),(86,6,3),s.metal,.3)
sights(s,-60,75,37)
# Keep this purely decorative glue plane clear of shallow surface details.
result=finalize(s,cutplane_mm=-24.13)
