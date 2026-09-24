"""KC17 / AM-17: compact integral upper, rounded long slot guard and cell mag."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('kc17',300)
body=s.mat('KC17 satin carbon gray alloy',(.072,.087,.094),.52,.47)
front(s,-149,-124,25,2.8)
ventguard(s,-124,-51,25,20,21,'mlok',body)
receiver(s,[(-53,36),(49,36),(63,30),(64,13),(-37,13),(-53,19)],20,body)
s.poly('Angular lower polymer frame','lower',[(-49,22),(61,23),(62,12),(44,6),(21,4),(-26,6),(-48,12)],18,s.polymer,.75)
for sign in [-1,1]:
 s.poly('Angular lower embossed relief','lower',[(-47,18),(-33,10),(13,10),(20,15),(-30,15)],.7,body,.4,y=sign*9.05)
 s.box('KC17 long shallow upper step','receiver',(-8,sign*10,28),(79,.6,2.2),s.edge,.3)
 s.box('Fixed front side handle root','receiver',(-43,sign*10.7,29),(8,2.3,4),s.metal,.4)
 s.cyl('Fixed side handle round knob','receiver',(-43,sign*12,29),1.8,2,s.polymer,'Y',.2)
 s.cyl('Static selector roundel','lower',(41,sign*9,16),2.4,1,s.edge,'Y',.2)
 s.poly('Static selector embossed fin','lower',[(40,17),(36,12),(38,10),(44,15)],.7,s.metal,.3,y=sign*9.6)
magazine(s,[(-26,12),(0,9),(-4,-10),(-14,-35),(-31,-59),(-55,-49),(-40,-24),(-31,-4)],14,'grid',s.polymer)
grip(s,38,7)
guard(s,'lower',[(0,9),(43,9),(44,-8),(36,-15),(13,-15),(3,-9)],[(6,5),(39,5),(39,-6),(33,-11),(15,-11),(7,-6)],6)
s.poly('Fixed sculptural trigger','lower',[(21,6),(24,6),(24,-5),(21,-8),(19,-7),(21,-2)],3,s.metal,.25)
buffer_stock(s,60,149,25,'triangle')
s.rail('sights',-123,51,37,6,4)
s.box('Long guard rail support','handguard',(-88,0,35.5),(72,8,3.7),body,.4)
sight(s,'sights',-112,38,True);sight(s,'sights',48,38)
optic(s,5,38.5)
s.scene['print_segment_breaks_x_mm']='[0]'
result=finish(s,'依据 KC17 对应游戏 AM17 双侧图重建紧凑一体上壳、长条盲槽护木、突出静态侧钮、格纹长弧匣及三角伸缩外观尾托。')
