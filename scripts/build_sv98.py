"""SV-98 default metal-chassis silhouette, sculpted as a solid desk miniature."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_long_helpers import scope,finish
s=Sculpture('sv98',350)
for key,label,show in [('chassis','长条金属底盘',True),('receiver','封闭矩形机匣',True),('barrel','螺旋纹封闭前杆',True),('handguard','镂空上护框',True),('magazine','短楔形匣装饰',True),('grip','弧形握把与护圈',True),('stock','骨架托与托腮板',True),('sights','短顶轨与固定瞄具',True),('optic','可选短望远瞄具',False)]:s.part(key,label,show)
chassis=s.mat('Warm gunmetal chassis',(.155,.155,.144),.6,.43)
silver=s.mat('Spiral satin silver',(.31,.34,.34),.77,.34)
s.scene['print_segment_breaks_x_mm']='[-15]'
s.poly('Angular lower chassis','chassis',[(-105,18),(-21,19),(-16,24),(61,24),(68,20),(68,11),(-105,11)],19,chassis,.9)
for sign in [-1,1]:
    s.poly('Front chassis inner side panel','chassis',[(-99,16),(-27,16),(-24,19),(-21,19),(-24,12.5),(-99,12.5)],.55,s.dark,.45,y=sign*9.46)
    for x in range(-98,-33,13):s.box('Chassis elongated shallow recess','chassis',(x,sign*9.8,14.3),(8.5,.6,1.8),s.polymer,.55)
    s.screw('Chassis root fastener','chassis',-20,17,sign*9.7,1.1)
s.poly('Closed receiver angular shell','receiver',[(-23,19),(-18,32),(45,33),(56,29),(62,27),(64,16),(-20,16)],20.5,s.metal,.85)
s.poly('Closed receiver rear slope','receiver',[(42,33),(55,29),(61,26),(68,26),(68,17),(58,17)],18,s.edge,.75)
for sign in [-1,1]:
    s.poly('Side receiver pressed rectangle','receiver',[(-16,18),(-16,29),(12,29),(12,18)],.5,chassis,.55,y=sign*10.28)
    s.poly('Side receiver back plate','receiver',[(15,18),(15,29),(43,29),(45,27),(46,18)],.4,s.polymer,.6,y=sign*10.4)
    for x,z in [(-13,21),(42,21),(57,24)]:s.screw('Receiver visible screw','receiver',x,z,sign*10.46,.85)
s.box('Sealed narrow side shutter','receiver',(29,-10.77,25),(18,.35,3.4),s.steel,.4)
s.line('Fixed silver handle root','receiver',(46,-7,27),(49,-14,29),1.6,s.steel)
s.line('Fixed handle droop','receiver',(49,-14,29),(47,-15,22),1.4,s.steel)
s.cyl('Fixed handle dark knob','receiver',(47,-15,21.5),2.7,5.5,s.polymer,'Y',.45)
# Solid front cylinder with a shallow silver/dark helix as exterior sculpture.
s.cyl('Solid spiral front core','barrel',(-91,0,30),3.7,158,silver,'X',.25,64)
for j in range(104):
    x=-163+j*1.3; xx=x+1.3; a=j*.62; b=(j+1)*.62
    s.line('Spiral surface rib','barrel',(x,3.55*math.cos(a),30+3.55*math.sin(a)),(xx,3.55*math.cos(b),30+3.55*math.sin(b)),.46,s.metal)
s.cyl('Solid front collar','barrel',(-168,0,30),4.6,7,s.metal,'X',.3)
s.cyl('Closed short muzzle','barrel',(-173,0,30),3.4,4,s.metal,'X',.25)
s.cyl('Opaque muzzle face','barrel',(-175.08,0,30),2.4,.18,s.dark,'X',.02)
# A bracket bridges the underbed and the top guard; actual silhouette holes only.
for x in [-99,-62]:s.box('Handguard vertical contact','handguard',(x,0,27),(4.3,15.4,22),chassis,.55)
s.poly('Short perforated upper guard','handguard',[(-109,30),(-101,40),(-60,40),(-57,33),(-64,29)],14.8,chassis,.65)
for x in [-96,-84,-72]:
    cutter=s.poly('Angled upper opening','handguard',[(x-4,33),(x-2,37),(x+5,37),(x+3,33)],25,s.dark,.3)
    shell=next(o for o in s.parts['handguard'].children if o.name=='Short perforated upper guard')
    s.cut(shell,cutter)
for sign in [-1,1]:s.box('Lower handguard edge reflection','handguard',(-81,sign*7.5,30),(42,.65,1.3),s.edge,.25)
s.poly('Short sloped solid magazine','magazine',[(-5,14),(26,14),(26,-3),(20,-6),(-5,2)],11.5,s.polymer,.8)
for sign in [-1,1]:s.poly('Magazine inset side','magazine',[(-1,10),(22,10),(22,-2),(18,-3),(-1,3)],.6,chassis,.5,y=sign*5.8)
s.poly('Integral ergonomic grip','grip',[(59,16),(69,14),(74,7),(72,0),(76,-8),(75,-13),(79,-21),(78,-25),(65,-26),(60,-22),(57,-14),(59,-6),(54,5)],14,s.polymer,1)
for sign in [-1,1]:
    s.poly('Raised grip side pad','grip',[(62,9),(68,8),(67,1),(71,-9),(71,-14),(74,-21),(66,-22),(62,-13),(64,-3)],.55,s.rubber,.6,y=sign*7.05)
    for z in [-17,-10,-3]:s.box('Grip shallow finger band','grip',(67,sign*7.4,z),(7,.4,.8),s.edge,.25)
g=s.poly('Fixed low guard','grip',[(29,15),(58,15),(61,3),(58,-3),(35,-3),(29,2)],6.6,s.metal,.7)
s.cut(g,s.poly('Guard exterior opening','grip',[(33,12),(54,12),(57,3),(55,0),(36,0),(33,3)],16,s.dark,.5))
s.poly('Fixed small trigger','grip',[(46,14),(49,14),(49,8),(46,3),(43,3),(46,8)],2.5,s.steel,.3)
s.box('Stock hinge block','stock',(72,0,23),(14,18,16),s.metal,.7)
for sign in [-1,1]:s.cyl('Hinge circular sculpture','stock',(74,sign*9.3,23),4.3,.7,s.edge,'Y',.3)
s.cyl('Solid stock support rod','stock',(112,0,24),3.5,72,s.metal,'X',.35)
s.poly('Skeleton stock frame','stock',[(97,25),(99,29),(165,29),(173,25),(173,-25),(160,-27),(148,-22),(149,-13),(128,-11),(124,-3),(117,0),(109,0),(106,17),(97,19)],17.6,s.polymer,1.05)
frame=next(o for o in s.parts['stock'].children if o.name=='Skeleton stock frame')
s.cut(frame,s.poly('Stock exterior window','stock',[(135,15),(160,15),(160,-7),(136,-7)],30,s.dark,.9))
s.box('Thick comb on top','stock',(135,0,29),(37,19.6,5.5),s.rubber,.85)
s.box('Stock fixed rear buttpad','stock',(173,0,1),(4,20.2,55),s.rubber,.7)
for sign in [-1,1]:
    s.screw('Stock lower adjustment ornament','stock',154,-14,sign*8.9,2.3)
    s.box('Comb shallow groove','stock',(135,sign*9.85,29),(29,.45,.7),s.polymer,.2)
    for x in [113,118,123]:s.box('Stock forward short rib','stock',(x,sign*8.82,16),(1.1,.45,8),s.edge,.3)
s.rail('sights',-16,46,33.3,7.8,3.5)
s.box('Rear fixed blade','sights',(45,0,35),(3.5,8.2,3),s.metal,.3)
s.box('Front pillar contact','sights',(-158,0,33),(6,6.3,6.6),s.metal,.4)
s.poly('Front tapered pillar','sights',[(-161,33),(-160,42),(-156,43),(-155,33)],5.4,s.metal,.4)
s.box('Front fixed crest','sights',(-158,0,43),(3,3,2.5),s.edge,.3)
scope(s,'optic',16,36.1,55)
result=finish(s,'https://www.imfdb.org/images/thumb/1/13/DFHO_SV98M.jpg/600px-DFHO_SV98M.jpg',['按默认截图建立金属长底盘、螺旋纹前杆、短镂空上护框、短楔形匣和骨架枪托。','页面文字提及瞄具，但所观察的默认双侧截图不带瞄镜，故默认采用机械瞄具，望远瞄具为数字可选。'])
