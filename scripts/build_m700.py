"""M700 game-default wooden exterior; solid miniature, no mechanical content."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch4_long_helpers import scope,grain,finish
s=Sculpture('m700',350)
for key,label,show in [('body','红棕木质前床',True),('stock','弯颈木整托与绑带',True),('receiver','封闭圆弧机匣',True),('barrel','封闭细长前杆',True),('magazine','短底片装饰',True),('guard','固定椭圆护圈',True),('sights','短顶轨与固定瞄具',True),('optic','可选望远瞄具',False)]:s.part(key,label,show)
wood=s.mat('Red brown walnut',(.24,.078,.032),0,.42)
light=s.mat('Warm wood highlights',(.31,.115,.052),0,.5)
dark=s.mat('Fine wood pores',(.13,.030,.014),0,.65)
strap=s.mat('Khaki woven strap',(.26,.24,.115),0,.87)
s.scene['print_segment_breaks_x_mm']='[10]'
s.poly('Long rounded wood forebed','body',[(-98,27),(-95,30),(55,30),(66,27),(75,24),(79,15),(73,11),(61,14),(-92,17),(-98,21)],17.5,wood,1.8)
for sign in [-1,1]:
    s.poly('Raised forebed edge','body',[(-93,27),(51,27),(57,25),(-93,25)],.35,light,.4,y=sign*8.76)
    s.screw('Forebed end pin','body',-90,22,sign*8.7,.75)
grain(s,'body',-90,58,20,3,8.8,light,dark)
s.poly('Downturned walnut wrist and stock','stock',[(65,28),(75,25),(90,18),(99,14),(103,24),(111,26),(164,26),(172,22),(173,-14),(165,-16),(111,-3),(101,0),(91,0),(86,7),(78,12),(66,15)],19.5,wood,2.1)
s.poly('Stock upper comb rubbed edge','stock',[(108,25),(113,28),(160,28),(170,24),(168,22),(111,24)],18.9,light,.7)
s.poly('Black rubber heel','stock',[(172,24),(175,23),(175,-16),(172,-17)],20.2,s.rubber,.55)
s.poly('Khaki butt wrap','stock',[(158,26),(166,25),(168,-15),(159,-13)],20.25,strap,.45)
for sign in [-1,1]:
    for x in [159,162,165]:
        s.line('Strap woven edge','stock',(x,sign*10.17,-11),(x-1,sign*10.17,23),.12,s.polymer)
    s.screw('Stock lower stud','stock',150,-10,sign*9.74,.7)
grain(s,'stock',114,155,0,10,9.8,light,dark)
# Round upper body stays completely filled. Silver side inset is shallow art.
s.cyl('Closed round receiver','receiver',(23,0,31),5.1,86,s.metal,'X',.4,64)
s.box('Receiver base','receiver',(25,0,28),(90,11.5,5.7),s.metal,.6)
s.box('Closed silver side shutter','receiver',(13,-5.6,31.5),(21,.5,5.5),s.steel,.65)
s.box('Shutter shadow border','receiver',(13,-5.36,31.4),(24,.3,7),s.dark,.65)
s.cyl('Round rear cap','receiver',(66,0,31),4.1,5,s.steel,'X',.35)
s.line('Fixed curved handle root','receiver',(58,-3.5,30),(60,-10,24),1.45,s.steel)
s.line('Fixed curved handle lower','receiver',(60,-10,24),(57,-10.5,18),1.5,s.steel)
s.cyl('Solid fixed handle knob','receiver',(57,-10.5,17.2),2.5,4.6,s.polymer,'Y',.5)
s.cone('Tapered sealed long front','barrel',(-97,0,31),2.45,3.7,156,s.metal,'X',.25)
s.cyl('Muzzle closed dark face','barrel',(-175.08,0,31),1.7,.18,s.dark,'X',.02)
s.poly('Shallow underside base plate','magazine',[(1,17),(32,16),(33,13),(1,14)],10.5,s.metal,.45)
for sign in [-1,1]:s.box('Base plate soft edge','magazine',(16,sign*5.2,14.3),(27,.7,.8),s.steel,.25)
g=s.poly('Fixed oval guard','guard',[(37,17),(65,16),(65,4),(61,0),(42,0),(37,5)],6,s.metal,1)
s.cut(g,s.poly('Guard exterior opening','guard',[(41,14),(61,13),(61,5),(58,3),(44,3),(41,6)],16,s.dark,.8))
s.poly('Fixed trigger silhouette','guard',[(51,16),(54,15),(54,9),(50,4),(48,4),(51,9)],2.5,s.steel,.4)
s.rail('sights',-4,52,37,7.2,3.6)
s.box('Fixed rear blade','sights',(50,0,39.6),(4,8,3),s.metal,.4)
s.box('Front blade base','sights',(-169,0,33),(7,5,2.3),s.metal,.35)
s.box('Front fixed blade','sights',(-169,0,35),(3,2.5,3.6),s.metal,.3)
scope(s,'optic',25,40,60)
result=finish(s,'https://www.imfdb.org/images/thumb/5/5f/DFHO_R700.jpg/600px-DFHO_R700.jpg',['保留游戏默认红棕木整托、尾部卡其绑带、细长前杆、短顶轨与机械瞄具；默认无望远瞄具。','木纹为可移植 PBR 色块与微浮雕，不依赖 Blender 程序纹理；微纹理仅用于数字展示。'])
