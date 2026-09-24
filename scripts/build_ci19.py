"""CI-19 game-default: exposed front rod, curved cell magazine and ribbed guard."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('ci19',300)
body=s.mat('CI19 warm graphite alloy',(.07,.079,.081),.6,.46)
front(s,-149,-78,24,2.4)
s.cyl('Long front shoulder sleeve','front',(-90,0,24),3.3,8,body,'X',.2)
s.poly('Ribbed polymer lower forearm','handguard',[(-78,29),(-9,29),(-6,15),(-71,15),(-78,19)],19,s.polymer,.8)
s.cyl('Rounded forearm lower contour','handguard',(-41,0,21),8.7,69,s.polymer,'X',.55)
for sign in [-1,1]:
 for x in range(-71,-12,4):s.box('Molded forearm rib','handguard',(x,sign*9.65,21),(1.3,.8,11),s.polymer,.35)
 for x in range(-70,-13,12):s.box('Upper blind forearm slot','handguard',(x,sign*9.35,28),(7,.4,2),s.dark,.35)
 s.box('Forward short side slab','handguard',(-73,sign*10,22),(8,1.1,13),body,.45)
 s.screw('Forward side closed stud','handguard',-74,22,sign*10.5,.95)
receiver(s,[(-11,32),(54,32),(64,28),(64,14),(-9,14)],19,body)
s.poly('CI19 distinct lower envelope','lower',[(-10,22),(64,22),(64,9),(48,4),(18,4),(-8,8)],18,body,.65)
for sign in [-1,1]:
 s.poly('Lower sloping well ornament','lower',[(-12,12),(14,9),(14,1),(-13,2)],.7,s.metal,.4,y=sign*9)
 s.box('Angular flat rear side panel','lower',(43,sign*9.1,14),(18,.55,6),body,.35)
 s.cyl('Static selector blind pivot','lower',(43,sign*9.1,10),2.3,.9,s.edge,'Y',.2)
 s.poly('Static selector tab','lower',[(43,11),(39,7),(40,5),(46,9)],.7,body,.25,y=sign*9.7)
magazine(s,[(-12,9),(12,7),(9,-14),(-1,-37),(-21,-57),(-40,-46),(-26,-27),(-17,-9)],14,'grid',s.polymer)
grip(s,44,5)
guard(s,'lower',[(12,8),(46,8),(47,-9),(40,-15),(23,-15),(14,-8)],[(17,4),(42,4),(42,-7),(37,-11),(25,-11),(18,-6)],6)
s.poly('Attached static trigger form','lower',[(28,5),(31,5),(31,-4),(28,-8),(26,-6),(28,-2)],3,body,.25)
buffer_stock(s,61,149,24,'triangle')
s.rail('sights',-73,53,33,6,4)
s.box('Guard upper rail support','handguard',(-42,0,31),(72,8,4),body,.45)
sight(s,'sights',-71,34,True);sight(s,'sights',52,34)
optic(s,12,35)
s.scene['print_segment_breaks_x_mm']='[-44]'
result=finish(s,'依据游戏更新后的 CI-19 双侧图，制作细长外露前杆、短圆肋护木、长弧格纹匣、斜握把、开窗伸缩外观尾托。')
