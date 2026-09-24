import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('mini14',320)
panel(s,'body',[(-99,27),(44,27),(59,22),(61,13),(26,13),(-20,15),(-97,18)],18,s.wood,1.3)
grain(s,'body',-94,38,18,5,9,s.woodlight,s.wood)
traditional(s,46,149)
s.cyl('Solid receiver round crown','details',(24,0,28),4.8,62,s.steel,'X',.25)
s.box('Stepped receiver top','details',(24,0,28),(44,13,9),s.steel,.6)
s.box('Closed receiver recess','details',(28,-6.6,30),(20,.7,4),s.dark,.4)
s.line('Fixed side handle','details',(43,-5,27),(48,-12,26),1.2,s.steel)
s.cyl('Fixed handle ball','details',(48,-12,26),2,3,s.metal,'Y',.3)
panel(s,'handguard',[(-99,29),(-94,34),(-30,34),(-22,30),(-21,26),(-98,25)],15,s.polymer,.8)
for sign in [-1,1]:
 for x in range(-92,-28,7):s.box('Heat shield blind groove','handguard',(x,sign*7.5,30),(3,.6,4.3),s.dark,.45)
front(s,-150,-90,28,2.6)
s.cyl('Front collar','barrel',(-104,0,28),4,4,s.steel,'X',.3)
magazine(s,21,15,22,14,s.metal)
guard(s,43,14,23)
s.box('Short top display saddle','sights',(17,0,34),(49,7,2),s.metal,.25)
for x in [-141,48]:
 s.box('Blade pedestal','sights',(x,0,31),(6,7,5),s.metal,.45)
 s.box('Fixed sight blade','sights',(x,0,36),(2.7,3.5,7),s.metal,.3)
scope(s,'optic',16,36,52)
result=finalize(s)
