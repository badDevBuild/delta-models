"""SKS default game exterior as a closed miniature display sculpture."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch3_mixed_helpers import scope,grain,finish
s=Sculpture('sks',350)
for key,label,show in [('body','红棕木质枪身',True),('stock','弯颈木质整托',True),('handguard','上木护盖',True),('receiver','封闭银灰机匣',True),('barrel','封闭阶梯前端',True),('magazine','短斜匣装饰',True),('guard','固定护圈装饰',True),('sights','固定机械瞄具',True),('optic','可选短望远瞄具',False)]:s.part(key,label,show)
wood=s.mat('Red stained walnut',(.265,.073,.029),0,.39)
light=s.mat('Warm rubbed wood',(.34,.121,.053),0,.47)
dark=s.mat('Dark wood pores',(.13,.025,.012),0,.58)
silver=s.mat('Blued silver receiver',(.25,.285,.30),.78,.36)
s.scene['print_segment_breaks_x_mm']='[20]'
# Reference-specific long one-piece wood bed with inset finger channels.
s.poly('Lower walnut bed','body',[(-96,25),(-91,29),(-12,29),(9,26),(73,24),(82,18),(86,10),(77,5),(1,8),(-81,8),(-94,13)],18.5,wood,1.65)
for sign in [-1,1]:
    s.poly('Long finger groove shadow','body',[(-83,22),(-43,23),(-35,19),(-36,17),(-75,17),(-84,19)],.35,dark,.65,y=sign*9.25)
    s.poly('Finger groove inner wood','body',[(-79,21),(-44,22),(-39,19),(-40,18),(-73,18)],.3,light,.5,y=sign*9.44)
    s.screw('Wood bed round pin','body',-24,21,sign*9.34,1.0)
    s.screw('Wood bed rear pin','body',69,16,sign*9.34,.9)
grain(s,'body',-79,64,11,2,9.32,light,dark)
# Separate upper short wood cover; this silhouette distinguishes SKS from M14.
s.poly('Upper walnut handguard','handguard',[(-96,29),(-95,37),(-48,37),(-47,29)],17.3,wood,1.3)
s.box('Upper handguard lower lip','handguard',(-71,0,29.2),(49,18.1,2.2),light,.55)
for xx in [-96,-48]:s.box('Dark handguard retaining band','handguard',(xx,0,32.3),(2.5,18.5,12.2),s.metal,.5)
grain(s,'handguard',-91,-53,32,2,8.69,light,dark)
# Filled receiver top and side; no internals behind shallow shutter patches.
s.poly('Closed receiver rear shell','receiver',[(-47,28),(-44,35),(60,35),(65,33),(66,24),(-47,24)],16.4,silver,.85)
s.box('Receiver top rounded cover','receiver',(26,0,35.0),(75,13.3,1.5),s.steel,.7)
s.poly('Receiver front block','receiver',[(-48,28),(-46,36),(-29,36),(-28,26)],15,s.metal,.6)
for sign in [-1,1]:
    s.box('Closed receiver front dark shutter','receiver',(-18,sign*8.22,31),(21,.4,4.3),s.dark,.45)
    s.box('Closed shutter reflected face','receiver',(-18,sign*8.43,31),(17,.24,2.9),s.steel,.3)
    s.box('Receiver lower seam','receiver',(10,sign*8.23,25.8),(102,.35,.8),s.metal,.2)
    s.screw('Receiver rear cover pin','receiver',62,29,sign*8.34,.75)
s.box('Fixed side handle bridge','receiver',(-24,-10,30.5),(9,5,2.7),s.metal,.4)
s.cyl('Fixed side handle knob','receiver',(-28,-13,31),1.85,4.0,s.metal,'Y',.35)
# Downturned wrist and unbroken traditional stock.
s.poly('Red walnut full buttstock','stock',[(71,25),(78,21),(85,13),(91,10),(99,10),(107,14),(169,15),(174,12),(174,-24),(170,-27),(111,-11),(102,-10),(95,-8),(88,-1),(78,6),(71,8)],19.2,wood,1.9)
s.poly('Stock comb rubbed edge','stock',[(107,13),(108,15),(168,16),(174,13),(172,11),(109,12)],18.7,light,.6)
s.poly('Thin black buttpad','stock',[(173,16),(175,15),(175,-27),(172.5,-28)],20,s.rubber,.55)
grain(s,'stock',115,166,-6,7,9.65,light,dark)
for z in range(-24,15,3):s.box('Butt edge small ribs','stock',(174.5,0,z),(.5,20.1,.55),s.polymer,.15)
# Two closed front rods joined through the visible block and wood-end band.
s.cyl('Solid main forward rod','barrel',(-136,0,28),2.7,78,s.metal,'X',.2,64)
s.cyl('Closed muzzle face','barrel',(-175.05,0,28),1.85,.18,s.dark,'X',.03)
s.cyl('Solid upper short rod','barrel',(-113,0,34),2.15,36,s.metal,'X',.2)
s.poly('Front tube junction sculpture','barrel',[(-135,25),(-135,33),(-131,39),(-126,38),(-126,25)],7.5,s.metal,.65)
s.box('Rear tube sealed contact','barrel',(-96,0,30),(4.5,12,14),s.metal,.55)
s.box('Narrow lower decorative spine','barrel',(-122,0,25.8),(31,3.3,2),s.metal,.3)
# Short wedge base silhouette rather than a long detachable magazine.
s.poly('Filled short sloped magazine','magazine',[(-24,10),(7,10),(7,-6),(3,-9),(-22,1)],10.3,s.metal,.6)
for sign in [-1,1]:s.poly('Magazine recessed side facet','magazine',[(-19,7),(3,7),(3,-5),(-18,2)],.3,s.edge,.4,y=sign*5.19)
s.poly('Magazine lower rim','magazine',[(-24,2),(4,-9),(8,-7),(8,-5),(-22,4)],10.8,s.metal,.35)
guard=s.poly('Fixed guard outer','guard',[(36,10),(64,10),(64,-2),(59,-7),(42,-7),(36,-2)],6.2,s.metal,.7)
s.cut(guard,s.poly('Exterior guard opening','guard',[(40,7),(60,7),(60,-1),(57,-3.7),(43,-3.7),(40,-1)],15,s.dark,.5))
s.poly('Fixed trigger silhouette','guard',[(50,8),(53,8),(53,3),(50,-2),(47,-2),(50,2)],2.5,s.steel,.3)
# Tall front pillar and tangent-style rear exterior sight.
s.box('Front sight contact foot','sights',(-154,0,29.4),(5.2,6,4.5),s.metal,.4)
s.poly('Front sight post bracket','sights',[(-157,30),(-156,43),(-152,43),(-151,30)],5.4,s.metal,.45)
s.box('Front sight fixed crest','sights',(-154,0,43.2),(2.1,2.3,1.8),s.edge,.25)
s.box('Rear tangent sight foot','sights',(-40,0,36),(13,8.5,3.2),s.metal,.4)
s.poly('Rear tangent sight ramp','sights',[(-47,37),(-47,39),(-31,42),(-29,39)],6.0,s.edge,.3)
for i in range(6):s.box('Rear sight shallow graduations','sights',(-43+i*2,0,39.2+i*.13),(.45,5.4,.4),s.metal,.08)
s.box('Rear sight fixed notch block','sights',(-29,0,41),(3.2,8.2,3),s.metal,.35)
# Digital-only arbitrary saddle, embedded into solid top surface.
scope(s,'optic',23,36.6,43)
result=finish(s,'https://www.imfdb.org/images/thumb/c/cb/DFHO_SKS.jpg/600px-DFHO_SKS.jpg',['游戏默认红棕整托、上木护盖、长封闭银灰机匣、护木侧面手指槽和短斜匣分别重建。','保留基础机械瞄具；额外小望远瞄具为数字可选艺术附件。细木纹只用于数字展示。'])
