"""K437: broad continuous upper shell, chevron magazine and folding-style cheek."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('k437',300)
body=s.mat('K437 slate blue graphite',(.098,.117,.13),.62,.39)
front(s,-149,-124,24,2.7)
ventguard(s,-124,-47,25,22,22,'mlok',body)
for sign in [-1,1]:
 for x in range(-114,-54,12):s.poly('Guard diagonal closed upper relief','handguard',[(x,35),(x+4,29),(x+8,29),(x+4,35)],.7,s.dark,.3,y=sign*11.05)
 s.box('Fixed long side slider blind groove','handguard',(-70,sign*10.8,31),(39,.5,3.3),s.dark,.6)
 s.cyl('Fixed solid side handle end','handguard',(-57,sign*12,31),2,3,s.polymer,'Y',.2)
receiver(s,[(-51,37),(54,37),(65,31),(67,16),(-35,16),(-49,21)],21,body)
s.poly('Angular lower shell','lower',[(-46,22),(65,23),(66,11),(47,4),(18,3),(-29,6),(-35,16)],18,body,.7)
for sign in [-1,1]:
 s.poly('Receiver diagonal side shoulder','receiver',[(-44,30),(-27,18),(-13,18),(-33,33)],.8,s.edge,.35,y=sign*10.7)
 s.poly('Blank large lower inset panel','lower',[(-20,17),(8,17),(9,8),(-19,8)],.6,s.metal,.3,y=sign*9)
 s.cyl('Static selector blind dial','lower',(39,sign*9.1,14),2.4,1.2,s.edge,'Y',.18)
 s.poly('Fixed selector side lever','lower',[(38,15),(33,10),(35,8),(42,13)],.8,s.metal,.25,y=sign*9.7)
magazine(s,[(-29,12),(-1,9),(-1,-13),(-8,-53),(-34,-48),(-32,-20)],15,'ribs',s.polymer)
for sign in [-1,1]:
 for z in [-6,-24,-42]:
  s.poly('Magazine shallow broad diagonal chevron','magazine',[(-31,z+7),(-6,z-2),(-6,z-5),(-31,z+4)],.7,s.edge,.25,y=sign*7.55)
  s.poly('Magazine second diagonal chevron','magazine',[(-30,z-4),(-8,z+6),(-7,z+3),(-30,z-7)],.7,s.metal,.25,y=sign*7.85)
grip(s,37,5)
guard(s,'lower',[(-1,8),(40,8),(41,-8),(34,-16),(10,-16),(1,-8)],[(5,4),(36,4),(36,-6),(31,-12),(12,-12),(6,-6)],6)
s.poly('Attached fixed trigger','lower',[(20,5),(23,5),(23,-5),(20,-9),(18,-7),(20,-2)],3,s.metal,.25)
s.box('Stock folding-style solid shoulder','stock',(69,0,26),(9,19,24),s.metal,.8)
s.poly('Stock broad raised cheek','stock',[(70,35),(83,34),(110,28),(136,28),(135,16),(82,16),(72,20)],22,s.polymer,1)
s.poly('Stock lower solid support','stock',[(77,22),(139,23),(140,14),(94,12),(77,15)],16,s.metal,.7)
s.box('Stock rear solid extension','stock',(138,0,22),(15,13,13),s.metal,.65)
s.poly('Stock tall rear rubber heel','stock',[(144,29),(149,29),(150,-21),(142,-21),(140,20)],22,s.rubber,.85)
for sign in [-1,1]:
 s.screw('Stock cheek inset roundel','stock',85,24,sign*10.9,1.5)
 for x in [88,91,94]:s.poly('Stock diagonal shallow rib','stock',[(x,24),(x+2,20),(x+3,20),(x+1,24)],.4,s.edge,.1,y=sign*11)
 for z in range(-16,24,5):s.box('Rear heel side blind square','stock',(146,sign*11,z),(3,.6,2.5),s.polymer,.3)
s.box('Guard upper attached rail spine','handguard',(-86,0,36.5),(77,8,3),body,.4)
s.rail('sights',-121,52,37.7,6,4)
sight(s,'sights',-114,38.5,True);sight(s,'sights',48,38.5)
optic(s,9,39)
s.scene['print_segment_breaks_x_mm']='[-46]'
result=finish(s,'依据游戏 K437 双侧截图重建宽折面上壳、斜槽短护木、交叉斜纹匣、抬高贴腮面与窄连接长尾垫。')
