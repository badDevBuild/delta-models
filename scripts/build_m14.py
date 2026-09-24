"""M14 game-reference exterior sculpture, independently authored miniature."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
from batch3_mixed_helpers import scope,grain,finish
s=Sculpture('m14',340)
for key,label,show in [('body','木质长枪身外观',True),('stock','木质弯颈枪托',True),('handguard','银灰开槽护罩',True),('receiver','机匣表面层次',True),('barrel','封闭双层前端',True),('magazine','短直匣装饰',True),('guard','固定扳机护圈',True),('sights','固定机械瞄具',True),('optic','可选望远瞄具',False)]:s.part(key,label,show)
wood=s.mat('Reddish walnut',(.23,.087,.033),0,.42)
light=s.mat('Walnut fine light grain',(.29,.13,.061),0,.5)
dark=s.mat('Walnut dark grain',(.12,.043,.018),0,.55)
silver=s.mat('Worn grey handguard',(.31,.34,.35),.7,.39)
s.scene['print_segment_breaks_x_mm']='[0]'
# Long, narrow, gently tapered wood fore-end as seen in the default game image.
s.poly('Wood fore-end and receiver bed','body',[(-109,21),(-103,23),(-17,21),(35,19),(72,15),(82,8),(76,2),(45,4),(-29,8),(-107,11)],18,wood,1.55)
for sign in [-1,1]:
    s.poly('Wood fore-end side shoulder','body',[(-106,18),(-24,17),(-13,14),(40,13),(49,7),(-25,9),(-105,12)],.35,light,.6,y=sign*8.9)
    s.screw('Stock bed screw','body',-10,14,sign*9.13,.8)
    s.screw('Receiver bedding pin','body',37,10,sign*9.13,1.3)
grain(s,'body',-101,-32,12.6,2,9.12,light,dark)
# The silver upper heat-shield is distinct from the lower walnut.
cover=s.poly('Solid vented upper shield','handguard',[(-110,22),(-108,29),(-11,29),(-7,26),(-7,20),(-109,20)],17.8,silver,.75)
for sign in [-1,1]:
    for i in range(9):
        x=-103+i*10.1
        s.box('Blind heat-shield slot','handguard',(x,sign*8.94,25.4),(7.5,.45,1.8),s.dark,.65)
    s.box('Shield lower rolled seam','handguard',(-59,sign*9.03,21.2),(96,.65,.7),s.edge,.25)
s.cyl('Shield front band','handguard',(-109,0,23.5),8.5,3.4,silver,'X',.4)
s.box('Shield band lower tie','handguard',(-109,0,17),(3.5,18,7.5),silver,.5)
# Receiver remains entirely filled beneath the visible reliefs.
s.poly('Closed receiver body','receiver',[(-12,22),(-7,28),(33,28),(41,24),(55,25),(66,21),(66,14),(-12,16)],15.2,s.metal,.75)
s.box('Receiver closed top recess','receiver',(12,0,28.2),(32,9,.7),s.dark,.35)
s.box('Receiver top metal face','receiver',(12,0,28.5),(29,7,.6),s.steel,.3)
for sign in [-1,1]:
    s.box('Receiver lower edge','receiver',(23,sign*7.65,18),(75,.45,1.4),s.edge,.2)
    s.box('Closed receiver side inset','receiver',(11,sign*7.65,24),(27,.4,3.3),s.dark,.4)
    s.box('Closed inset reflected steel','receiver',(12,sign*7.85,24),(23,.28,2.3),s.steel,.3)
s.line('Fixed side rod relief','receiver',(-2,-8.5,19),(38,-8.5,19),.95,s.metal)
s.cyl('Fixed round side control','receiver',(32,-10.5,21.5),2.8,5.5,s.metal,'Y',.35)
s.box('Rear receiver angular crest','receiver',(50,0,27),(15,12,4.7),s.metal,.55)
# Full sporting stock, with the game-visible downturned wrist.
s.poly('Walnut full buttstock','stock',[(65,19),(77,12),(85,6),(91,4),(102,8),(162,8),(168,6),(168,-29),(164,-31),(104,-12),(92,-11),(88,-6),(77,4),(65,7)],18.8,wood,1.8)
s.poly('Butt upper highlight','stock',[(99,6),(105,9),(161,9),(167,7),(166,5),(107,6)],18.3,light,.5)
s.poly('Rubber buttpad','stock',[(167,10),(170,9),(170,-31),(167,-32)],20,s.rubber,.7)
s.poly('Buttpad narrow spacer','stock',[(165.8,9),(167.5,9),(167.5,-31),(165.8,-31)],19.4,s.metal,.25)
grain(s,'stock',112,159,-6,6,9.44,light,dark)
for sign in [-1,1]:
    s.box('Stock wrist shallow side inset','stock',(83,sign*9.35,4),(8,.22,1.2),dark,.3)
for z in range(-28,9,3):s.box('Buttpad soft ribs','stock',(169.5,0,z),(.8,20.1,.7),s.polymer,.2)
s.cyl('Rear sling stud sculpture','stock',(143,0,-26),1.3,5,s.metal,'Z',.25)
s.box('Rear sling tiny solid loop','stock',(143,0,-28),(5,5,1.6),s.metal,.4)
# Capped front assembly includes the lower short decorative tube.
s.cyl('Solid long barrel sculpture','barrel',(-135,0,24),2.75,70,s.metal,'X',.23,64)
s.cyl('Sealed front face','barrel',(-170.05,0,24),1.9,.18,s.dark,'X',.03)
s.cyl('Solid lower tube','barrel',(-116,0,16),2.1,31,s.metal,'X',.2)
s.box('Lower tube artistic contact web','barrel',(-117,0,20),(22,3.4,5.8),s.metal,.4)
s.cyl('Lower front cap','barrel',(-132,0,16),2.5,1.6,s.edge,'X',.2)
s.poly('Short solid magazine','magazine',[(4,9),(27,7),(26,-14),(3,-13)],11.3,s.metal,.7)
for sign in [-1,1]:
    for x in [8,21]:s.box('Magazine shallow fold','magazine',(x,sign*5.7,-3),(.65,.25,17),s.edge,.2)
    s.box('Magazine bottom rim','magazine',(14.8,sign*5.8,-13),(22.8,.6,1),s.metal,.25)
guard=s.poly('Fixed exterior guard','guard',[(35,7),(61,7),(61,-3),(55,-10),(42,-10),(36,-5)],6.3,s.metal,.7)
s.cut(guard,s.poly('Guard silhouette opening','guard',[(39,4),(57,4),(57,-2),(52,-6),(43,-6),(40,-3)],16,s.dark,.6))
s.poly('Fixed trigger silhouette','guard',[(46,5),(49,5),(50,0),(48,-4),(45,-5),(46,-2)],2.4,s.steel,.35)
s.box('Front sight base','sights',(-123,0,27),(8,7,2.8),s.metal,.45)
s.box('Front sight fixed post','sights',(-123,0,31),(1.6,2.2,6),s.metal,.2)
for sign in [-1,1]:s.poly('Front sight protective wing','sights',[(-126,27),(-125,33),(-122,34),(-120,27)],1.7,s.metal,.3,y=sign*2.7)
s.box('Rear sight support','sights',(49,0,30),(8,9,4.0),s.metal,.4)
s.cyl('Rear sight circle','sights',(49,0,34.5),3.5,2.8,s.metal,'X',.25)
s.cyl('Rear sight blind inlay','sights',(47.55,0,34.5),1.6,.15,s.dark,'X',.03)
for sign in [-1,1]:s.cyl('Rear sight fixed dial','sights',(49,sign*5,30),2.7,1.8,s.edge,'Y',.2)
scope(s,'optic',9,29.7,45)
result=finish(s,'https://www.imfdb.org/images/thumb/1/1f/DFHO_M14.jpg/600px-DFHO_M14.jpg',['保留游戏默认木质长身、弯颈整托、银灰长护罩、上方长槽与短直弹匣；可选望远瞄具为独立艺术附件。','木纹颜色细线低于喷嘴尺度，仅用于数字表面；打印融合时省略。'])
