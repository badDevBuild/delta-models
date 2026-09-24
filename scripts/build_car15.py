"""CAR-15 game-default miniature: compact round guard, carry handle, short box."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('car15',270)
front(s,-134,-87,23,2.4,False)
s.cyl('Front collar lip','front',(-91,0,23),3.9,6,s.metal,'X',.22)
s.cyl('Closed ribbed carbine forearm','handguard',(-55,0,23),9.1,72,s.polymer,'X',.7,64)
for x in range(-88,-19,5):s.cyl('Circular molded guard rib','handguard',(x,0,23),9.55,1.4,s.polymer,'X',.22,48)
for x in [-89,-18]:s.cyl('Handguard end retaining collar','handguard',(x,0,23),9.85,3,s.metal,'X',.3)
for sign in [-1,1]:
 s.box('Guard side molded seam','handguard',(-55,sign*9.05,23),(65,.4,.8),s.dark,.17)
 for x in range(-83,-23,9):s.box('Blind upper guard vent','handguard',(x,sign*4,31),(4.2,2,.4),s.dark,.3)
receiver(s,[(-18,33),(40,33),(52,27),(54,15),(-18,15)],17)
lower(s,-10,10);grip(s,27,3)
s.poly('Short straight solid box','magazine',[(-17,8),(5,6),(6,-22),(-17,-22)],13,s.metal,.6)
for sign in [-1,1]:
 for x in [-12,-5,2]:s.box('Magazine shallow press flute','magazine',(x,sign*6.5,-10),(1.5,.5,17),s.dark,.25)
s.box('Closed magazine base','magazine',(-5.5,0,-22),(24,14.1,2),s.metal,.4)
buffer_stock(s,50,134,23,'wedge')
s.poly('Carry handle attached base','sights',[(-18,32),(50,32),(48,36),(-18,36)],11,s.metal,.5)
o=s.poly('High fixed carry handle','sights',[(-17,34),(-15,47),(33,51),(44,47),(50,34)],8,s.metal,.6)
s.cut(o,s.poly('Carry silhouette cutter','sights',[(-10,38),(-10,44),(32,47),(39,44),(42,38)],24,s.dark,.45))
s.box('Rear carry sight crown','sights',(41,0,47),(9,9,4),s.metal,.5)
s.cyl('Rear fixed sight dial','sights',(41,-5,47),2.2,2,s.polymer,'Y',.2)
o=s.poly('Front triangular sight silhouette','sights',[(-95,24),(-95,46),(-92,50),(-88,50),(-80,25)],5,s.metal,.5)
s.cut(o,s.poly('Front triangular opening','sights',[(-92,31),(-92,43),(-89,44),(-84,31)],16,s.dark,.2))
s.box('Front fixed sight crossfoot','sights',(-91,0,28),(9,9,10),s.metal,.45)
optic(s,13,48)
s.scene['print_segment_breaks_x_mm']='[-28]'
result=finish(s,'依据游戏双侧图制作短圆肋护木、高提把、短直匣与细长伸缩式外观后托；没有复制 M16A4 的长护木与固定整托。')
