"""PKM visual reconstruction as a sealed, nonfunctional miniature sculpture."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_long_helpers import scope,grain,finish
s=Sculpture('pkm',330)
for key,label,show in [('receiver','大型封闭机匣',True),('cover','棱面顶盖',True),('barrel','阶梯双前杆',True),('stock','镂空木质整托',True),('grip','木握把与固定护圈',True),('box','橄榄绿侧挂盒',True),('belt','抽象链纹浮雕',True),('handle','棕色提手装饰',True),('sights','固定机械瞄具',True),('optic','可选数字瞄具',False)]:s.part(key,label,show)
wood=s.mat('Dark red walnut',(.225,.065,.027),0,.45)
light=s.mat('Wood warm edge',(.29,.093,.037),0,.5)
dark=s.mat('Fine wood pores',(.115,.021,.009),0,.65)
olive=s.mat('Olive steel box',(.16,.185,.067),.4,.53)
oliveedge=s.mat('Box rubbed edges',(.29,.32,.13),.42,.48)
brass=s.mat('Muted bronze chain plaque',(.20,.17,.072),.62,.44)
s.scene['print_segment_breaks_x_mm']='[-30]'
s.poly('Large closed receiver block','receiver',[(-33,33),(-28,38),(55,38),(70,32),(73,29),(73,12),(-28,12),(-34,18)],23,s.metal,1)
for sign in [-1,1]:
    s.box('Receiver deep side panel','receiver',(24,sign*11.6,23),(69,.6,13),s.polymer,.8)
    s.box('Receiver lower pressed edge','receiver',(19,sign*12,14),(98,.8,1.8),s.edge,.35)
    s.poly('Rear diagonal side crease','receiver',[(35,29),(47,34),(61,32),(47,28)],.55,s.edge,.4,y=sign*11.7)
    for x,z in [(-26,20),(-17,31),(26,18),(66,18),(63,29)]:s.screw('Side receiver rivet','receiver',x,z,sign*12.1,.9)
s.box('Sealed side shutter','receiver',(34,-12.2,25),(29,.6,6),s.dark,.6)
s.box('Side shutter reflection','receiver',(34,-12.6,24.5),(25,.3,1.2),s.steel,.25)
s.box('Fixed side control bridge','receiver',(51,-14,19),(13,5.6,2.8),s.metal,.6)
s.cyl('Fixed side knob','receiver',(55,-16.5,19),2.3,4.5,s.metal,'Y',.3)
s.poly('Long raised top cover','cover',[(-28,36),(-23,43),(48,43),(63,39),(67,35)],20,s.metal,.85)
s.box('Cover ridge','cover',(10,0,43),(62,14.2,1.4),s.edge,.55)
for sign in [-1,1]:
    s.poly('Top cover stepped side groove','cover',[(-16,38),(-13,41),(28,41),(34,38)],.65,s.dark,.35,y=sign*10.05)
    s.box('Top cover front tab','cover',(-23,sign*10.3,38.5),(6,.9,3.1),s.steel,.35)
    for x in [38,49,59]:s.screw('Top cover edge screw','cover',x,38,sign*10.4,.75)
# Default reference has no deployed bipod and no flared muzzle device.
s.cyl('Long solid forward rod','barrel',(-96,0,29),2.9,138,s.metal,'X',.2,64)
s.cyl('Opaque closed muzzle face','barrel',(-165.08,0,29),2,.18,s.dark,'X',.02)
s.cyl('Rear stepped front collar','barrel',(-38,0,29),4.8,17,s.metal,'X',.35)
s.cyl('Front gas collar sculpture','barrel',(-112,0,29),4.5,6,s.metal,'X',.3)
s.cyl('Lower closed secondary rod','barrel',(-73,0,20),2.7,84,s.metal,'X',.25)
s.box('Front dual-rod bridge','barrel',(-113,0,24),(5.5,6.5,12),s.metal,.6)
s.box('Rear dual-rod bridge','barrel',(-34,0,24),(8,10,17),s.metal,.7)
for x in [-106,-92,-56,-42]:s.cyl('Secondary rod pressed collar','barrel',(x,0,20),3.3,3.2,s.edge,'X',.25)
s.box('Lower narrow contact web','barrel',(-41,0,24),(15,3.6,7),s.polymer,.4)
# The wooden stock is its own polygonal exterior, not the prior M249 outline.
s.poly('Wood open buttstock','stock',[(70,29),(91,29),(102,36),(159,36),(165,32),(164,-1),(161,-3),(135,1),(123,1),(115,-7),(108,-6),(104,6),(93,13),(72,14)],18.3,wood,1.4)
frame=next(o for o in s.parts['stock'].children if o.name=='Wood open buttstock')
s.cut(frame,s.poly('Large wood stock window','stock',[(109,29),(152,29),(154,24),(152,9),(125,9),(116,12),(108,21)],30,s.dark,1))
s.poly('Rubber end heel','stock',[(162,36),(165,35),(165,-4),(162,-4)],19.6,s.rubber,.45)
for sign in [-1,1]:
    s.poly('Stock root black inset','stock',[(76,23),(92,23),(96,20),(94,16),(77,17)],.45,s.dark,.7,y=sign*9.2)
    for x,z in [(79,19),(158,29),(158,4)]:s.screw('Stock wood fastener','stock',x,z,sign*9.3,.9)
grain(s,'stock',112,155,31,2,9.2,light,dark)
s.poly('Red wood slanted grip','grip',[(55,15),(69,14),(70,5),(78,-20),(75,-25),(62,-27),(57,-21),(53,0)],14.3,wood,1.1)
for sign in [-1,1]:
    for x in [59,63,67]:s.line('Long grip carving','grip',(x,sign*7.21,4),(x+6,sign*7.21,-20),.23,dark)
    s.screw('Grip wood screw','grip',64,-3,sign*7.3,.8)
g=s.poly('Fixed curved guard','grip',[(27,14),(56,14),(59,3),(55,-3),(32,-3),(27,2)],6.5,s.metal,.8)
s.cut(g,s.poly('Guard exterior aperture','grip',[(31,11),(52,11),(55,3),(52,0),(34,0),(31,3)],17,s.dark,.6))
s.poly('Fixed trigger silhouette','grip',[(43,13),(46,13),(46,7),(43,2),(40,2),(43,7)],2.7,s.steel,.3)
# Closed olive display box, connected to the underside of the sculpture.
s.box('Solid green side box','box',(4,-6,-15),(37,20,57),olive,1.5)
s.box('Box light folded upper lid','box',(4,-6,11),(39,21.2,6),oliveedge,.8)
s.box('Box lower rolled lip','box',(4,-6,-42),(37.8,20.7,2.2),oliveedge,.45)
for sign in [-1,1]:
    y=-6+sign*10.2
    s.poly('Box stamped inset','box',[(-10,4),(18,4),(18,-35),(-10,-35)],.55,s.polymer,.9,y=y)
    s.poly('Box inset olive surface','box',[(-8,2),(16,2),(16,-33),(-8,-33)],.55,olive,.6,y=y+sign*.25)
    for x in [-5,12]:s.box('Box tall pressed reinforcement','box',(x,y+sign*.55,-16),(2.4,1,34),oliveedge,.55)
    s.box('Box central strap','box',(4,y+sign*.7,-15),(4.5,1.2,50),s.rubber,.4)
    s.box('Box buckle upper','box',(4,y+sign*1.2,4),(7,1.8,4.5),s.steel,.5)
# Abstract connected chain sculpture: plain plaques, no cartridge geometry.
s.poly('Solid curved chain strip','belt',[(-4,38),(-14,29),(-23,17),(-24,-25),(-17,-25),(-16,13),(-10,23),(3,34)],3.6,s.polymer,.7,y=-15)
s.box('Chain to receiver connection','belt',(-2,-11.5,35),(10,11,5),s.metal,.55)
s.box('Chain to sidebox contact','belt',(-16,-14.7,-2),(5,5,28),s.metal,.55)
for j in range(10):
    z=12-j*3.7
    s.box('Abstract chain rectangular plaque','belt',(-20,-17,z),(7.7,2.1,1.8),brass,.35)
for j in range(5):
    x=-12+j*2.7;z=26+j*2.1
    s.box('Upper chain rectangular plaque','belt',(x,-17,z),(7,2,1.8),brass,.3)
s.poly('Carrying handle front stem','handle',[(-28,36),(-28,45),(-24,48),(-21,45),(-22,37)],6,s.metal,.6)
s.poly('Carrying handle rear stem','handle',[(-3,39),(-3,45),(2,47),(6,44),(6,40)],6,s.metal,.6)
s.poly('Curved wooden carry grip','handle',[(-27,46),(-19,49),(-1,50),(5,47),(3,44),(-19,43),(-26,43)],8.7,wood,1)
s.box('Handle rubbed top edge','handle',(-11,0,48),(24,8,1.5),light,.65)
s.box('Tall front sight root','sights',(-158,0,32),(6,6,5.5),s.metal,.4)
s.poly('Tall front tapered tower','sights',[(-161,32),(-160,46),(-156,46),(-154,32)],5.4,s.metal,.5)
s.box('Front tower fixed crest','sights',(-158,0,46.5),(4.5,6.1,1.8),s.edge,.3)
s.box('Rear tangent sight base','sights',(33,0,44),(19,10,3),s.metal,.5)
s.poly('Rear sight ramp','sights',[(24,45),(24,47),(40,48),(44,46)],7,s.edge,.4)
s.box('Rear fixed notch','sights',(43,0,48),(3,10,3.4),s.metal,.35)
s.box('Digital optic solid riser','optic',(32,0,44.5),(28,8.5,5),s.metal,.45)
scope(s,'optic',32,47,38)
result=finish(s,'https://www.imfdb.org/images/thumb/b/b6/DFHO_PKM.jpg/600px-DFHO_PKM.jpg',['依照默认双侧图建立木镂空托、绿色侧挂盒、大型封闭顶盖与双前杆，不加入默认图没有的展开脚架或前端喇叭件。','侧边链带仅为抽象连续矩形浮雕，不建立弹药、内部供弹机构或可用接口。木纹为显式 PBR 色块和微浮雕。'])
