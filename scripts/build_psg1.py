import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('psg1',350)
box_receiver(s,-1,74,25)
s.cyl('Rounded longitudinal top cover','body',(33,0,32),5.2,81,s.metal,'X',.4)
panel(s,'handguard',[(-89,29),(-81,36),(-1,34),(4,28),(3,17),(-88,18)],16,s.polymer,1)
for sign in [-1,1]:
 s.line('Long handguard molded seam','handguard',(-84,sign*8,22),(-4,sign*8,23),.3,s.edge)
 pins(s,'handguard',[-79,-7],20,sign*8)
front(s,-150,-82,28,2.8)
s.cyl('Raised closed carrier bar','details',(-38,0,36),2.2,92,s.steel,'X',.2)
s.box('Fixed rear bar grip','details',(-74,-8.8,36),(8,3.5,5),s.polymer,.4)
magazine(s,16,13,25,22,s.metal)
pistol_grip(s,57,11,s.wood,True)
s.cyl('Stock smooth neck','stock',(93,0,27),6,47,s.polymer,'X',.6)
panel(s,'stock',[(108,34),(135,34),(142,30),(142,-7),(111,-7),(106,-1)],20,s.polymer,1.1)
panel(s,'stock',[(106,35),(139,35),(135,17),(111,17)],21,s.metal,.7)
s.box('Adjustable looking sealed butt','stock',(149,0,14),(4,21,41),s.rubber,.7)
s.box('Fixed butt spacer','stock',(143,0,14),(10,13,23),s.metal,.4)
pins(s,'stock',[117,130],1,10)
sights(s,-82,70,38,False)
result=finalize(s)
