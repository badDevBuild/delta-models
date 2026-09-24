"""M249 game-reference solid miniature artwork, independent exterior groups."""
import sys, math, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('m249',320)
for k,l,v in [('receiver','封闭机匣外壳',True),('top_cover','上盖与顶部外观',True),('handguard','护木外观',True),('front','封闭前端和机械瞄具',True),('stock','黑色固定托外观',True),('grip','握把和固定护圈',True),('box','实心长盒外壳',True),('trim','金色压纹及固定细节',True),('bipod','可选装饰支架',False)]:s.part(k,l,v)
graphite=s.mat('Dark gunmetal stamped shell',(.11,.119,.12),.67,.45)
edgegrey=s.mat('Worn grey edges',(.18,.19,.185),.65,.43)
brass=s.mat('Muted brass surface relief',(.36,.255,.08),.65,.43)

# Closed silhouette front: cap and all end faces are filled.
s.cyl('Solid forward barrel sculpture','front',(-117,0,21),2.5,85,s.metal,'X',.12,64)
s.cyl('Solid muzzle collar','front',(-157,0,21),3.0,6,s.metal,'X',.15)
s.cyl('Closed muzzle end face','front',(-160,0,21),2.45,.16,s.dark,'X',.03)
for x in [-157.5,-155,-118,-109]:s.cyl('Front collar ring relief','front',(x,0,21),2.85,1.4,s.edge,'X',.15)
s.box('Sight fixed base','front',(-113,0,24),(10,8,8),s.metal,.6)
s.poly('Sight front silhouette','front',[(-116,25),(-116,37),(-114,40),(-111,39),(-109,26)],4.5,s.metal,.5)
s.box('Sight horizontal ledge','front',(-112,0,31),(9,9,2.3),s.metal,.3)
s.box('Sight fixed post','front',(-113,0,36),(1.8,2,5),s.steel,.2)
for sy in [-1,1]:s.screw('Sight adjustment cap','front',-113,28,sy*4.2,1.3)
s.cyl('Lower solid fore tube','front',(-109,0,12),3.2,30,s.metal,'X',.3)
s.cyl('Lower tube decorative collar','front',(-121,0,12),4.0,5,s.metal,'X',.3)
s.box('Front lower anchor block','front',(-99,0,14),(9,10,8),s.metal,.5)

# Game base handguard has a large pressed grey upper side and a dark angled lower strip.
hand=s.poly('Stamped fore-end exterior','handguard',[(-102,24),(-29,24),(-21,32),(-13,31),(-14,3),(-24,-1),(-64,0),(-69,6),(-108,6)],19.4,graphite,.85)
s.poly('Dark lower fore-end contour','handguard',[(-106,8),(-71,8),(-63,0),(-21,-1),(-19,-5),(-69,-5),(-74,0),(-108,0)],16.8,s.polymer,.75)
for sy in [-1,1]:
    # Non-through pressed channels, not a functional heat shield specification.
    s.poly('Raised fore-end side flange','handguard',[(-101,21),(-32,21),(-21,28),(-19,22),(-25,17),(-100,17)],.5,edgegrey,.5,y=sy*9.74)
    s.poly('Fore-end mid relief','handguard',[(-83,14),(-66,14),(-63,8),(-32,8),(-31,13),(-21,13),(-21,5),(-66,5),(-72,10),(-83,10)],.45,s.metal,.5,y=sy*9.8)
    for i in range(5):
        x=-102+i*7
        s.poly('Diagonal lower fore-end recess','handguard',[(x,3),(x+3,6),(x+6,6),(x+2,1)],.3,s.dark,.3,y=sy*8.58)
    for x,z in [(-99,17),(-77,12),(-24,3),(-20,24)]:s.screw('Fore-end fixed fastener','handguard',x,z,sy*9.84,.95)
    s.box('Fore-end closed panel seam','handguard',(-48,sy*9.99,4),(30,.2,.45),s.dark,.12)
s.cyl('Fore-end visible round boss','handguard',(-97,0,21),2.7,21,s.metal,'Y',.2)

s.poly('Solid machine-gun receiver exterior','receiver',[(-17,31),(66,31),(77,26),(76,1),(61,-2),(-15,1),(-19,12)],23.6,graphite,.8)
s.box('Receiver closed lower spine','receiver',(27,0,2),(94,21,5),s.metal,.55)
s.poly('Receiver upper rounded shoulder','receiver',[(-13,33),(64,33),(72,29),(71,26),(-15,26)],22,s.metal,.8)
for sy in [-1,1]:
    s.box('Upper closed side panel','receiver',(39,sy*11.9,23),(55,.45,9),s.metal,.6)
    s.box('Receiver lower pressed channel','receiver',(32,sy*12.01,8),(76,.5,5.8),s.metal,.6)
    s.box('Receiver channel shadow','receiver',(37,sy*12.31,8),(53,.15,2.1),s.dark,.35)
    s.box('Lower receiver seam highlight','receiver',(33,sy*12.31,3),(72,.2,.55),edgegrey,.12)
    for x,z in [(-12,28),(9,22),(44,10),(68,22),(70,7),(19,1)]:s.screw('Receiver fixed exterior rivet','receiver',x,z,sy*12,.9)
    s.cyl('Receiver rear pivot appearance','receiver',(70,sy*12.1,18),3.3,1.0,s.metal,'Y',.25)
    s.cyl('Receiver rear pivot inset','receiver',(70,sy*12.67,18),1.7,.1,s.dark,'Y',.05)
    # Unbranded identification relief avoids copying game logos or serials.
    s.box('Blank rectangular ID plaque','receiver',(48,sy*12.2,24),(14,.3,2.8),s.dark,.3)
    for i in range(6):s.box('Fine plaque stroke','receiver',(43+i*1.5,sy*12.38,24),(.4,.15,1.3),s.edge,.06)['print_skip']=True

s.box('Closed cover main slab','top_cover',(28,0,34),(81,21,5.0),s.metal,.7)
s.rail('top_cover',-8,60,37,8.5,3.1)
s.cyl('Cover front fixed hinge appearance','top_cover',(-15,0,32),3.2,25,s.metal,'Y',.3)
for sy in [-1,1]:
    s.box('Cover outside rim','top_cover',(25,sy*10.6,34),(75,.7,2.5),s.edge,.2)
    s.screw('Cover hinge side cap','top_cover',-15,32,sy*13,1.5)
s.box('Rear sight sculpted foundation','top_cover',(55,0,39),(17,12,3.5),s.metal,.5)
s.cyl('Rear sight transverse body','top_cover',(54,0,41),3.2,11,s.metal,'Y',.3)
for sy in [-1,1]:s.box('Rear sight protective cheek','top_cover',(59,sy*4.5,41),(5,2.2,6),s.metal,.5)
s.box('Rear sight central fixed notch','top_cover',(60,0,40),(3,5,2.5),s.steel,.25)
# The folded carry handle is solidly joined at one end, with an enlarged art connection.
s.box('Buried carry-handle sculpture bridge','top_cover',(-28,0,26.5),(5,6,8),s.metal,.5)
s.cyl('Fixed carry handle pivot','top_cover',(-28,0,30),2.4,10,s.metal,'Y',.3)
s.line('Fixed carry handle rising stem','top_cover',(-28,0,30),(-29,0,41),1.75,s.metal)
s.line('Fixed carry handle angled segment','top_cover',(-29,0,41),(-49,0,39),1.55,s.metal)
s.box('Folded carry handle grip','top_cover',(-45,0,40),(19,5,4),s.polymer,.7)
for x in range(-53,-36,2):s.box('Carry handle grip shallow rib','top_cover',(x,0,41.9),(.65,5.1,.55),s.metal,.18)

stock=s.poly('Fixed black stock body','stock',[(72,27),(94,14),(117,12),(127,19),(155,22),(158,18),(156,-18),(116,-18),(112,-13),(112,-4),(90,0),(71,2)],20.0,s.polymer,1.9)
for sy in [-1,1]:
    s.poly('Stock molded shoulder panel','stock',[(88,17),(112,9),(124,12),(119,6),(114,3),(89,6),(77,9)],.55,s.rubber,.85,y=sy*10)
    s.poly('Stock rear subtle molding','stock',[(130,17),(152,18),(151,-13),(122,-13),(120,-9),(132,-7)],.3,s.polymer,.9,y=sy*10.13)
    s.screw('Stock collar fixed fastener','stock',80,8,sy*10.08,1)
    s.screw('Butt upper fastener','stock',155,18,sy*10.12,1.2)
s.poly('Black butt pad','stock',[(155,23),(160,22),(158,-19),(154,-19)],21.8,s.rubber,.6)
for z in range(-16,21,2):s.box('Butt pad fine transverse ridge','stock',(158.7,0,z),(.7,22,0.7),s.polymer,.16)

s.poly('Molded pistol grip silhouette','grip',[(35,3),(47,4),(62,-25),(48,-31),(34,-7)],13.4,s.polymer,.9)
for sy in [-1,1]:
    s.poly('Pistol grip inset panel','grip',[(39,-3),(45,-1),(56,-23),(48,-27),(38,-6)],.35,s.rubber,.55,y=sy*6.76)
    for i in range(12):
        z=-5-i*1.55;x=39+i*.6
        o=s.box('Grip diagonal molded rib','grip',(x+5,sy*7,z),(9,.55,.6),s.metal,.16)
        o.rotation_euler.y=-.3
guard=s.poly('Fixed trigger guard silhouette','grip',[(13,5),(36,5),(39,-9),(34,-15),(18,-15),(12,-9)],6,s.metal,.65)
s.cut(guard,s.poly('Trigger guard outer opening','grip',[(17,1),(31,1),(35,-8),(31,-11),(18,-11),(16,-7)],14,s.dark,.7))
s.poly('Fixed trigger exterior','grip',[(26,3),(30,3),(31,-5),(28,-9),(26,-8),(28,-4)],2.6,s.steel,.4)

# The base screenshot's prominent vertical box is solid and closed throughout.
s.box('Solid long box exterior','box',(-4,0,-29),(26.4,23,58),s.polymer,1.5)
s.box('Box thick closed upper lid','box',(-4,0,-.6),(28,24.8,5),s.metal,.7)
s.box('Box solid base flange','box',(-4,0,-56),(27,23.8,3.4),s.metal,.5)
for sy in [-1,1]:
    s.box('Box outer raised frame','box',(-4,sy*11.65,-29),(22,.5,48),s.metal,.85)
    s.box('Box panel inset','box',(-4,sy*11.98,-29),(18,.28,43),s.polymer,.7)
    for x in [-14,6]:s.box('Box long edge rib','box',(x,sy*12,-29),(.8,.55,48),edgegrey,.23)
    for z in [-6,-52]:s.box('Box transverse flange rib','box',(-4,sy*12,z),(19,.5,1.1),s.metal,.3)
    s.box('Box blank information plate','box',(-4,sy*12.16,-30),(6,.22,15),s.dark,.2)
    for i in range(9):
        o=s.box('Box decorative label short line','box',(-4,sy*12.31,-24-i*1.35),(3.5 if i%3 else 4.5,.12,.35),s.edge,.05);o['print_skip']=True
    for x,z in [(-12,-7),(4,-7),(-12,-51),(4,-51)]:s.screw('Box exterior rivet','box',x,z,sy*12.1,.6)

# A fixed shallow brass relief reproduces the screenshot's color pattern only.
# These flattened bars share a closed solid backing; no separate rounds or belt mechanism.
s.box('Solid brass-relief backing panel','trim',(-4,-12.3,17),(24,3.1,30),s.dark,.6)
for i in range(8):
    z=4+i*3.5
    s.box('Brass colored fixed horizontal relief','trim',(-4,-14.05,z),(18,.9,1.65),brass,.65)
    s.box('Relief left dark edge','trim',(-14,-13.9,z),(3,1.2,2.1),s.metal,.35)
    s.box('Relief right dark edge','trim',(6,-13.9,z),(3,1.2,2.1),s.metal,.35)
s.box('Relief upper lip','trim',(-4,-14.1,32),(24,2.4,2),s.metal,.4)
s.cyl('Side fixed control pivot','trim',(24,-12.8,15),1.7,2.2,s.metal,'Y',.2)
s.line('Side fixed control relief stem','trim',(24,-13.4,15),(27,-14.6,8),1,s.metal)
s.box('Side fixed control paddle','trim',(27,-14.4,7),(3.5,2,5),s.polymer,.4)
for x in [17,35,60]:s.box('Fine receiver side score','trim',(x,-12.47,14),(3,.15,.4),edgegrey,.05)['print_skip']=True

# Optional fixed decorative stand, intentionally not a real articulated bipod.
s.box('Decorative stand closed attachment','bipod',(-97,0,4),(10,15,5),s.metal,.6)
for sy in [-1,1]:
    s.cyl('Stand ornamental side pivot','bipod',(-97,sy*7,1),3.3,3,s.metal,'Y',.3)
    s.line('Decorative stand upper leg','bipod',(-97,sy*8,1),(-109,sy*19,-30),1.8,s.metal)
    s.line('Decorative stand lower leg','bipod',(-109,sy*19,-30),(-114,sy*23,-43),1.45,s.steel)
    s.box('Decorative stand foot','bipod',(-114,sy*23,-44),(9,5,2.8),s.rubber,.5)
    for i in range(6):
        q=i/6;s.line('Stand leg cross hatch','bipod',(-101-q*7,sy*(11+q*7)-1,-10-q*17),(-101-q*7,sy*(11+q*7)+1,-10-q*17),1.85,s.polymer)
s.scene['print_segment_breaks_x_mm']=json.dumps([30])
sources=['https://zilliongamer.com/delta-force/c/weapons/best-m249-build-delta-force','https://zilliongamer.com/uploads/delta-force/weapons-builds/light-machine-gun/m249/m249-delta-force-build.jpg']
approx=['已实际查看游戏基础截图：长直前端、灰黑压制护木、固定黑色宽托、垂直长盒外壳、侧面金色横条以及折叠提把。','总长320mm为微缩艺术设计值；右侧、顶部隐蔽细节与小型五金为外观推断；未照抄游戏标识或文字。','侧面金色列仅用连续实心底板和扁平金色横条浮雕表现，无弹药、供弹或其他内部机构；盒体实心封闭。','可选支架是固定装饰，网页可切换；实体基础配置整体融合后平面胶合，不含支架。']
result=s.finish(sources,approx)
(s.out/'SOURCE_NOTES.md').write_text('# M249 参考与重建说明\n\n'+'\n'.join('- '+u for u in sources)+'\n\n'+'\n'.join('- '+p for p in approx)+'\n',encoding='utf-8')
