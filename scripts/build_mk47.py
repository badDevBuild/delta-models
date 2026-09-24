"""MK47 Dissent: long M-LOK silhouette, separate rail islands, short curved box."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('mk47',300)
body=s.mat('MK47 pale graphite machined alloy',(.10,.116,.12),.68,.39)
front(s,-149,-126,23,2.7)
ventguard(s,-127,-15,24,19,21,'mlok',body)
for sign in [-1,1]:
 for x in range(-118,-20,15):s.box('Guard shallow upper row vent','handguard',(x,sign*9.5,31),(9,.45,2.1),s.dark,.5)
 for x in [-37,-33,-29]:s.poly('Guard rear diagonal relief','handguard',[(x,26),(x+4,19),(x+5.2,19),(x+1.2,26)],.5,s.edge,.16,y=sign*9.58)
receiver(s,[(-16,35),(54,35),(60,31),(61,15),(-16,15)],18,body)
lower(s,-3,10);grip(s,35,4)
for sign in [-1,1]:
 for x in [24,28,32]:s.poly('Upper receiver shallow diagonal edge','receiver',[(x,33),(x+5,28),(x+6,28),(x+1,33)],.6,s.edge,.18,y=sign*9.05)
 s.box('Static front side slider recess','receiver',(-8,sign*9.15,29),(17,.5,3),s.dark,.45)
 s.box('Attached short front slider knob','receiver',(-12,sign*10,29),(6,2,3.7),s.polymer,.45)
 s.box('Fixed lower side control panel','lower',(25,sign*8.9,10),(4,1.2,9),s.edge,.3)
magazine(s,[(-8,9),(17,7),(14,-9),(5,-27),(-4,-40),(-25,-29),(-16,-12)],14,'grid',s.polymer)
buffer_stock(s,58,149,25,'triangle')
s.box('Forward rail attached closed root','handguard',(-118,0,34.6),(20,8,2.6),body,.35)
s.box('Rear rail attached closed root','receiver',(5,0,35),(107,8,1.8),body,.35)
s.rail('sights',-127,-108,35.7,6,4);s.rail('sights',-54,53,35.7,6,4)
for x in range(-102,-60,12):s.box('Top closed guard long slot','handguard',(x,0,34.35),(8,3,.6),s.dark,.4)
sight(s,'sights',-118,36.7,True);sight(s,'sights',49,36.7)
optic(s,9,37.5)
s.scene['print_segment_breaks_x_mm']='[-45]'
result=finish(s,'依据游戏 MK47 Dissent 默认双侧图，制作长条镂空感盲槽护木、分段顶部装饰脊、短弯格纹匣、斜切机匣浮雕与三角开窗后托。')
