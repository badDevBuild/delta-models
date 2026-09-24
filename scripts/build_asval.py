"""AS Val: inert closed cylindrical front and static skeleton exterior."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rifle_batch3_helpers import *
s=Sculpture('asval',290)
for key,label,show in [('receiver','机匣外观主体',True),('cover','弧形上盖外观',True),('handguard','短带纹护木',True),('front','封闭圆柱前端',True),('magazine','短实心弹匣',True),('grip','握把与固定护圈',True),('stock','固定金属骨架托',True),('sights','前后固定瞄具',True),('optic','可选紧凑瞄具',False)]:s.part(key,label,show)
metal=s.mat('AS graphite aged alloy',(.09,.098,.1),.73,.46)
poly=s.mat('AS dark composite',(.045,.046,.047),.04,.72)
mag=s.mat('AS subtle plum magazine',(.065,.043,.045),.07,.67)
# The game has a long thick cylindrical front with several rail collar ornaments.
# This piece is deliberately filled throughout, with a closed shallow end disc.
s.cyl('Entirely solid long cylindrical front','front',(-96,0,16),7.25,98,metal,'X',.5,64)
s.cyl('Sealed front flat disc','front',(-145,0,16),6.9,.4,s.dark,'X',.12)
for x in [-111,-88,-63]:
    s.cyl('Front sleeve broad external band','front',(x,0,16),7.7,4,metal,'X',.3)
    s.box('Front ornamental bottom collar bed','front',(x,0,8.8),(12,9,2.2),s.metal,.45)
    for i in range(4):s.box('Front collar tiny bottom ridge','front',(x-4.4+i*3,0,7.9),(1.7,10.5,1.2),metal,.25)
for sign in [-1,1]:
    for x in [-111,-88]:
        s.box('Front side collar bed','front',(x,sign*7.05,16),(14,1.7,5.8),s.metal,.5)
        for j in range(4):s.box('Front side collar shallow ridge','front',(x-5+j*3.1,sign*8.0,16),(1.7,1.2,6.8),metal,.25)
    s.box('Front long subtle cylinder seam','front',(-126,sign*7.05,16),(21,.5,.7),s.edge,.15)
# Short ribbed forebody has a rounded but flattened lower shell.
s.poly('Short solid handguard contour','handguard',[(-50,24),(-17,24),(-12,17),(-13,4),(-41,3),(-49,7)],20,poly,.9)
s.cyl('Forebody attached transition collar','handguard',(-49,0,16),8,5,metal,'X',.4)
for sign in [-1,1]:
    for j in range(6):
        z=6+j*2.6
        s.box('Handguard long shallow parallel rib','handguard',(-31,sign*9.94,z),(28,.7,1.25),metal,.4)
    s.box('Handguard rear short shoulder','handguard',(-15,sign*9.5,13),(3,2,15),metal,.6)
# Closed sheet-like receiver and ribbed arched top.
s.poly('Filled sloping receiver shell','receiver',[(-18,24),(43,24),(55,20),(58,1),(42,-3),(18,-1),(-13,4)],17,metal,.8)
s.poly('Rounded dust-cover sculpture','cover',[(-15,23),(-13,29),(44,29),(50,25),(51,18),(-14,18)],16.8,metal,1.2)
for x in [-4,10,25,40]:s.poly('Cover thin pressed transverse rib','cover',[(x-1,22),(x-1,29.4),(x+1,29.4),(x+1,22)],17.3,s.edge,.45)
for sign in [-1,1]:
    s.box('Receiver long lower flange','receiver',(16,sign*8.43,6),(59,.65,1.7),s.edge,.3)
    s.box('Cover shallow pressed seam','cover',(16,sign*8.38,23),(59,.5,1),s.dark,.2)
    for x,z in [(-8,13),(4,8),(27,8),(43,10),(52,9)]:s.screw('Receiver fixed rivet decoration','receiver',x,z,sign*8.45,.8)
    s.poly('Magazine root side plate','receiver',[(-12,12),(5,9),(5,-1),(-14,3)],.5,s.metal,.4,y=sign*8.4)
    s.box('Plain abstract side mark','receiver',(26,sign*8.52,15),(13,.3,3.4),metal,.25)
s.poly('Fixed low side selector','receiver',[(27,18),(42,18),(51,12),(50,10),(40,14),(28,14)],.9,s.metal,.35,y=8.62)
s.box('Fixed decorative short handle stem','receiver',(25,-10,20),(7,5,3),metal,.4)
s.cyl('Fixed handle broad knob','receiver',(25,-14,20),2.4,5,metal,'Y',.3)
for y in [-12.3,-13.8,-15.3]:s.cyl('Handle grip ring','receiver',(25,y,20),2.6,.6,s.edge,'Y',.1)
# The base game magazine is notably short and plum brown.
s.poly('Short solid magazine silhouette','magazine',[(-12,5),(10,1),(7,-14),(2,-31),(-18,-27),(-14,-11)],12.4,mag,.7)
side_plate(s,'Magazine broad flat inset','magazine',[(-10,0),(7,-3),(3,-25),(-14,-22)],6.15,poly,.42,.4)
for sign in [-1,1]:
    for j in range(5):s.line('Magazine shallow molded transverse ribs','magazine',(-12-j*.4,sign*6.38,-6-j*3.7),(5-j*.6,sign*6.38,-10-j*3.7),.38,mag)
s.poly('Magazine closed end plate','magazine',[(-18,-25),(3,-29),(3,-32),(-19,-28)],13.2,metal,.5)
# Static pistol grip and small open guard.
s.poly('Solid angled pistol grip','grip',[(36,2),(46,1),(48,-11),(56,-35),(45,-38),(37,-24),(29,-6)],14.5,poly,1)
side_plate(s,'Grip side rough inset','grip',[(36,-7),(44,-9),(51,-31),(45,-32),(38,-21)],7.15,s.rubber,.45,.6)
dot_texture(s,'grip',13,37,-11,7.36,.45,4,poly)
g=s.poly('Fixed small guard sculpture','grip',[(6,4),(35,4),(35,-9),(30,-13),(11,-12),(7,-8)],7,s.metal,.7)
s.cut(g,s.poly('Guard open visual window','grip',[(11,0),(30,0),(30,-6),(27,-9),(13,-8)],19,s.dark,.5))
s.poly('Fixed trigger shape','grip',[(23,3),(26,3),(27,-3),(24,-8),(21,-7),(24,-2)],2.5,s.metal,.3)
# Tubular fixed triangular skeleton. It is purely an exterior shape, no hinge motion.
s.poly('Static stock root block','stock',[(54,19),(67,19),(69,14),(66,3),(55,3)],17,metal,.6)
s.cyl('Blind stock root pivot ornament','stock',(60,0,10),2.6,20,metal,'Z',.3)
s.line('Stock upper solid brace','stock',(65,0,16),(141,0,16),2.6,metal)
s.line('Stock lower descending solid brace','stock',(65,0,10),(134,0,-14),2.6,metal)
s.line('Stock lower heel connection','stock',(134,0,-14),(142,0,-14),2.7,metal)
s.poly('Stock padded rear upright','stock',[(139,19),(145,19),(145,-18),(138,-18)],11.5,s.rubber,.9)
s.box('Stock central flat reinforcement band','stock',(106,0,5),(5.5,7.4,24),poly,.7)
for sign in [-1,1]:
    s.screw('Stock band fixed relief stud','stock',106,10,sign*3.7,.7)
    s.box('Stock upper shallow sheen','stock',(113,sign*2.45,16),(40,.3,.7),s.edge,.17)
for z in range(-15,18,3):s.box('Stock buttpad small tread','stock',(145,0,z),(.5,11.6,.8),poly,.18)
# Sight towers attach directly to the thick front and dust cover.
s.box('Front sight broad attached shoe','sights',(-137,0,23),(9,9,3.6),metal,.6)
s.poly('Front sight low tower','sights',[(-140,23),(-140,31),(-138,33),(-135,33),(-132,23)],5,metal,.5)
s.cyl('Front sight closed circular relief','sights',(-137,0,30),1.7,2.7,s.edge,'X',.15)
s.box('Rear sight attached base','sights',(-5,0,29),(12,8,3),metal,.4)
s.poly('Rear sight short inclined panel','sights',[(-11,30),(-5,35),(0,34),(2,30)],5,metal,.4)
# Optional scope has an art-only side plinth continuous with the upper cover.
s.box('Optional solid scope plinth','optic',(18,0,30),(30,8,3),metal,.4)
optic(s,18,32)
s.scene['print_segment_breaks_x_mm']='[-53]'
result=finish(s,'以实际游戏双侧截图的长粗圆柱前端、数道短装饰环轨、短带纹护木、紫褐短弹匣和细金属骨架托为辨识特征；默认不带瞄具配件。')
