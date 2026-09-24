"""ASh-12 miniature: wide bullpup box, tall handle and rear short slab magazine."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_rifles_helpers import *
s=setup('ash12',280,[('receiver','宽长无托机匣'),('lower','下缘与固定护圈'),('handguard','前部槽纹护木'),('front','封闭短前端'),('magazine','后置实心短匣'),('grip','前置斜握把'),('stock','一体尾托与垫'),('sights','高提把与装饰脊'),('optic','可选紧凑瞄具')])
body=s.mat('ASh12 dark slate gunmetal',(.061,.074,.081),.57,.47)
front(s,-139,-122,24,3.6,False)
s.cyl('Short massive front collar','front',(-135,0,24),5.3,7,body,'X',.2)
ventguard(s,-132,-60,24,25.6,28,'quad',body)
for sign in [-1,1]:
 s.poly('Guard rear relief plate','handguard',[(-92,34),(-62,34),(-61,18),(-96,18),(-98,26)],.8,body,.5,y=sign*12.8)
 for x in [-126,-63]:s.screw('Wide guard blind round stud','handguard',x,22,sign*12.75,1.6)
receiver(s,[(-63,39),(127,39),(135,34),(135,8),(-64,8)],25,body)
s.poly('Long lower solid edge','lower',[(-68,15),(122,15),(129,8),(86,2),(54,4),(12,9),(-66,9)],23,body,.65)
for sign in [-1,1]:
 s.box('Upper long shoulder seam','receiver',(41,sign*12.46,35),(172,.4,.9),s.edge,.2)
 s.box('Blank receiver shallow label','receiver',(20,sign*12.58,21),(14,.35,4.5),s.edge,.25)
 s.poly('Rear magazine well angled cover','lower',[(21,13),(71,13),(72,4),(38,-2),(24,2)],.75,s.metal,.5,y=sign*12.2)
 for x in [-47,77,116]:s.screw('Bullpup envelope inset stud','receiver',x,17,sign*12.45,1)
 s.box('Front static control fin','lower',(-59,sign*12.5,17),(7,1,2.6),s.edge,.35)
magazine(s,[(25,12),(66,10),(60,-13),(55,-44),(18,-36),(23,-8)],19,'ribs',body)
# Deliberately broad, nearly featureless stamped sides of the default box.
for sign in [-1,1]:
 s.poly('Magazine shallow plain central field','magazine',[(29,4),(60,2),(52,-37),(23,-31)],.6,body,.5,y=sign*9.75)
 s.screw('Magazine broad side blind stud','magazine',35,-6,sign*10,1.2)
grip(s,-30,10)
guard(s,'lower',[(-68,11),(-31,11),(-29,-7),(-35,-13),(-59,-13),(-68,-8)],[(-64,7),(-35,7),(-34,-5),(-38,-9),(-58,-9),(-64,-5)],7)
s.poly('Attached short trigger relief','lower',[(-50,8),(-47,8),(-47,-3),(-50,-7),(-52,-5),(-50,0)],3,body,.25)
s.poly('Rear stock lower cheek body','stock',[(89,11),(137,13),(139,6),(139,-23),(108,-21),(101,-6),(91,0)],26,s.polymer,.95)
s.box('Rear wide stock heel','stock',(138.2,0,9),(3.5,27,61),s.rubber,.9)
for sign in [-1,1]:
 for z in [-10,-1,8,17,26,34]:s.cyl('Blind stock heel side round detail','stock',(138,sign*13.3,z),1.8,.45,s.dark,'Y',.13,32)
 s.box('Stock long side separation','stock',(124,sign*13,2),(1,.45,46),s.metal,.2)
# Carry handle bridged to top body: silhouette opening only, no optical aperture.
s.box('Carry handle lower attached plinth','sights',(-29,0,40),(86,14,4),body,.6)
o=s.poly('Tall carry handle fixed frame','sights',[(-69,39),(-69,61),(-65,66),(-59,64),(-58,57),(5,57),(8,63),(14,61),(17,39)],10,body,.6)
s.cut(o,s.poly('Carry handle silhouette opening','sights',[(-59,43),(-56,50),(-48,54),(0,54),(7,49),(7,43)],30,s.dark,.45))
s.rail('sights',-60,9,59,7,4)
s.box('Carry front broad foot','sights',(-64,0,47),(9,13,15),body,.45)
for sign in [-1,1]:
 for x in [-64,12]:s.screw('Carry handle blind fixing head','sights',x,45,sign*5.1,1.2)
optic(s,-24,61)
s.scene['print_segment_breaks_x_mm']='[-38]'
result=finish(s,'依据游戏 ASh-12 双侧图重建宽扁无托长机匣、前置握把、后置短宽匣、高提把与一体下垂尾托；保持封闭实心艺术形态。')
