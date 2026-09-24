import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('sr25',330)
box_receiver(s,-6,62,24)
panel(s,'handguard',[(-121,33),(-7,33),(-5,29),(-5,14),(-118,14),(-123,20)],18,s.metal,.8)
for sign in [-1,1]:
 s.box('Long handguard panel','handguard',(-65,sign*9,22),(104,.65,11),s.polymer,.55)
 for x in range(-110,-12,16):
  s.box('Molded handguard separator','handguard',(x,sign*9.5,22),(1.4,1,11),s.edge,.2)
  s.screw('Handguard round mark','handguard',x-2,21,sign*9.55,.65)
front(s,-150,-115,25,2.8)
s.cyl('Short sealed front collar','barrel',(-141,0,25),3.7,8,s.metal,'X',.3)
for sign in [-1,1]:
 for x in range(-144,-137,3):s.box('Muzzle blind slot','barrel',(x,sign*3.5,25),(1,.4,3),s.dark,.12)
magazine(s,10,11,28,21,s.metal)
pistol_grip(s,47,10)
closed_stock(s,60,149)
sights(s,-118,59,35)
result=finalize(s)
