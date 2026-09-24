"""MCX LT Rattler default: compact angular handguard and narrow open stock."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('mcxlt',300)
body=s.mat('MCX LT cool gray ceramic metal',(.11,.123,.127),.61,.4)
front(s,-149,-133,23,2.9,False)
s.cyl('Short forward decorative collar','front',(-143,0,23),4,8,s.metal,'X',.25)
ventguard(s,-135,-46,25,22.6,23,'mlok',body)
for sign in [-1,1]:
 for x in range(-127,-54,12):s.poly('Guard diagonal upper blind slot','handguard',[(x,36),(x+4,31),(x+8,31),(x+6,36)],.6,s.dark,.25,y=sign*11.4)
 s.poly('Guard lower angular gusset','handguard',[(-129,19),(-91,18),(-79,15),(-57,15),(-47,22),(-48,12),(-128,12)],.7,body,.4,y=sign*11.5)
receiver(s,[(-49,39),(47,39),(62,33),(63,15),(-49,15)],22,body)
lower(s,-37,12);grip(s,3,5)
for sign in [-1,1]:
 s.box('Long MCX receiver side step','receiver',(4,sign*11,32),(88,.65,2.1),s.edge,.35)
 s.box('Closed side charging recess','receiver',(-10,sign*11.1,34),(34,.55,3.4),s.dark,.45)
 s.box('Fixed side charging boss','receiver',(-22,sign*12,34),(6,2.2,4),s.metal,.4)
 s.poly('Rear angular receiver panel','receiver',[(22,27),(53,27),(49,18),(27,17)],.6,s.metal,.35,y=sign*11)
magazine(s,[(-46,13),(-18,10),(-20,-19),(-25,-58),(-55,-54),(-50,-16)],15,'grid',s.polymer)
# Match default thin folding stock instead of a bulky buffer-tube stock.
s.box('Stock hinge-style solid shoulder','stock',(64,0,28),(11,16,22),s.metal,.75)
s.line('Stock upper solid graphic rod','stock',(67,0,31),(143,0,31),2.6,s.metal)
s.poly('Slim stock raised cheek piece','stock',[(85,35),(138,35),(140,30),(136,24),(94,24)],14,s.polymer,.7)
s.line('Stock lower diagonal solid strut','stock',(70,0,22),(139,0,25),2.2,s.metal)
s.line('Stock small lower brace','stock',(72,0,22),(87,0,30),1.6,s.metal)
s.poly('Narrow long sealed rear heel','stock',[(141,35),(149,35),(150,-18),(143,-18),(139,23)],16,s.rubber,.85)
for sign in [-1,1]:
 s.screw('Stock shoulder blind pivot','stock',64,28,sign*8,1.4)
 for z in range(-13,29,6):s.box('Heel side molded indent','stock',(145,sign*8,z),(2.7,.5,2.5),s.polymer,.3)
s.rail('sights',-133,50,39.7,6,4)
s.box('Guard top filled narrow ridge support','handguard',(-91,0,38),(90,8,5),body,.45)
sight(s,'sights',-125,40.7,True);sight(s,'sights',46,40.7)
optic(s,3,41.3)
s.scene['print_segment_breaks_x_mm']='[0]'
result=finish(s,'依据 GameWith 的 MCX LT 默认游戏大图，重建短折面护木、宽上机匣、长直格纹匣和细杆开窗后托；该图为单侧视角，背面细节含更大艺术推断。')
