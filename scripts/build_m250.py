import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_long_helpers import *
s=new('m250',330)
box_receiver(s,-28,89,26,s.tan)
panel(s,'handguard',[(-79,36),(-68,44),(-26,43),(-18,32),(-21,14),(-77,14)],22,s.tan,.9)
for sign in [-1,1]:
 for x in [-69,-56,-43,-30]:
  s.box('Blind horizontal ventilation','handguard',(x,sign*11,29),(8,.75,2.4),s.dark,.9)
  panel(s,'handguard',[(x-2,39),(x+3,39),(x+1,35),(x-4,35)],.7,s.dark,.4).location.y=sign*11
 s.box('Long lower forebed ridge','handguard',(-50,sign*8.5,16),(58,7,7),s.tan,.75)
front(s,-150,-72,29,3.2)
folded_bipod(s,'barrel',-74,-118,15)
s.cyl('Fore-end rod collar','barrel',(-111,0,27),5.2,7,s.metal,'X',.4)
skeleton_stock(s,88,149,s.tan)
pistol_grip(s,65,12,s.tan)
# Solid decorative ribbons evoke the exposed belt without separate ammunition.
s.box('Closed external belt ribbon','details',(9,-14.2,20),(27,13,38),s.metal,1.4)
for z in range(4,37,5):s.box('Bronze belt shallow relief','details',(9,-20.7,z),(23,.8,2.3),s.mat('Brass relief '+str(z),(.30,.26,.12),.65,.4),.75)
s.box('Inert fabric pouch core','magazine',(4,-7,-10),(36,31,42),s.fabric,4)
s.box('Pouch upper lid','magazine',(4,-7,9),(36.5,31.5,12),s.polymer,3)
s.box('Pouch stitched face','magazine',(4,-22.2,-14),(30,1,25),s.fabric,2)
for x in [-9,17]:s.line('Fabric edge piping','magazine',(x,-22.6,-25),(x,-22.6,-4),.3,s.woodlight)
s.box('Plain fabric badge','magazine',(4,-23,-9),(19,.5,5),s.tan,.3)
sights(s,-69,81,46)
s.box('Receiver upper rail foundation','sights',(26,0,40),(117,13,10),s.tan,.6)
# Keep this purely decorative glue plane clear of shallow surface details.
result=finalize(s,cutplane_mm=-25.7)
