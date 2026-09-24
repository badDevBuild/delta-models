"""SVD game-reference miniature exterior; no functional geometry or interfaces."""
import sys, math, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('svd',380)
for k,l,v in [('receiver','封闭机匣外观',True),('top_cover','机匣上盖外观',True),('handguard','木色护木',True),('front','封闭前端和机械瞄具',True),('stock','木色开孔枪托',True),('magazine','实心短弹匣外观',True),('controls','固定操控件外观',True),('optic','可选望远瞄具装饰',False)]:s.part(k,l,v)
wood=s.mat('Warm reddish walnut',(.34,.135,.054),.0,.53)
wood_high=s.mat('Walnut grain light',(.43,.20,.089),.0,.56)
wood_dark=s.mat('Walnut grain shadow',(.16,.067,.033),.0,.67)
# Ratios traced visually from the game base screenshot: short exposed front,
# long wooden handguard, rectangular cover, large and small stock openings.
s.cyl('Solid short exposed front','front',(-151,0,24),2.6,76,s.metal,'X',.12,64)
s.cyl('Closed front cap','front',(-188,0,24),3.25,4,s.metal,'X',.16)
s.cyl('Filled front face','front',(-190,0,24),2.6,.15,s.dark,'X',.03)
for x in [-187,-185,-142,-133]:s.cyl('Front collar relief','front',(x,0,24),3.0,1.6,s.edge,'X',.1)
s.box('Front sight solid pedestal','front',(-180,0,28),(7,7,9),s.metal,.5)
for sy in [-1,1]:s.poly('Front sight hood wing','front',[(-183,30),(-182,41),(-178,42),(-177,31)],1.6,s.metal,.3,y=sy*2.7)
s.box('Front sight bridge','front',(-180,0,40.7),(5.6,6.8,1.5),s.metal,.2)
s.box('Front sight fixed central post','front',(-180,0,34.6),(2.6,2.2,7.5),s.steel,.2)
s.cyl('Sight external adjuster','front',(-180,-4,32),2,2,s.metal,'Y',.15)
s.poly('Front upper housing sculpture','front',[(-157,26),(-153,32),(-129,33),(-121,29),(-121,24)],8,s.metal,.6)
for sy in [-1,1]:s.box('Front upper shallow seam','front',(-138,sy*4.04,29),(19,.2,.55),s.dark,.08)

guard=s.poly('Wood handguard rounded body','handguard',[(-123,33),(-20,33),(-16,29),(-16,14),(-23,12),(-119,16),(-125,20)],15.5,wood,1.8)
s.box('Guard rear steel collar','handguard',(-18,0,23),(4.5,16.4,23),s.metal,.45)
s.box('Guard front steel collar','handguard',(-124,0,24),(3.6,14.8,16),s.metal,.4)
for sy in [-1,1]:
    # Blind visible recesses, leaving the central sculpture body filled.
    for i,(x,w,z) in enumerate([(-112,12,29),(-95,17,29),(-73,20,29),(-108,20,21),(-82,20,21),(-56,20,21)]):
        cutter=s.box('Blind vent carving','handguard',(x,sy*7.7,z),(w,4,2.7),s.dark,1.1)
        s.cut(guard,cutter)
        s.box('Blind vent dark floor','handguard',(x,sy*6.08,z),(w-1.1,.25,1.5),s.dark,.65)
    s.box('Wood center join line','handguard',(-72,sy*7.82,25),(95,.12,.25),wood_dark,.08)['print_skip']=True
    for row in range(13):
        z=17+row*1.05
        for j in range(3):
            a=-114+j*30; b=a+24+3*math.sin(row*.7+j)
            # Tiny grain accents are display-only; they are not isolated print pieces.
            obj=s.line('Handguard fine grain','handguard',(a,sy*7.84,z),(b,sy*7.84,z+.45*math.sin(row)),.055,wood_high if row%3 else wood_dark)
            obj['print_skip']=True

s.poly('Main sealed receiver','receiver',[(-18,31),(95,31),(98,20),(88,7),(21,7),(-18,14)],16.6,s.metal,.8)
s.box('Receiver upper shoulder','receiver',(39,0,32),(114,17.4,3.8),s.metal,.45)
for sy in [-1,1]:
    s.poly('Lower receiver side stamped face','receiver',[(-14,18),(79,18),(83,11),(27,9),(-13,14)],.45,s.edge,.5,y=sy*8.32)
    s.box('Receiver closed side port','receiver',(42,sy*8.61,25),(45,.3,6),s.dark,.6)
    s.box('Sealed interior face relief','receiver',(42,sy*8.84,25),(37,.18,3.5),s.metal,.3)
    for x,z in [(-9,20),(29,13),(61,12),(84,20)]:s.screw('Receiver exterior rivet','receiver',x,z,sy*8.55,.95)
    s.box('Receiver lower seam','receiver',(39,sy*8.74,17),(91,.2,.4),s.dark,.08)
s.poly('Rounded top cover silhouette','top_cover',[(-17,33),(-12,37),(83,37),(92,34),(96,30),(-17,30)],15.4,s.metal,.65)
for x in range(-4,85,15):
    s.box('Top cover shallow transverse crease','top_cover',(x,0,37),(1.2,14.5,.52),s.edge,.2)
    for sy in [-1,1]:s.box('Cover crease folded edge','top_cover',(x,sy*7.45,34),(1.0,.6,5),s.metal,.2)
s.box('Rear cover catch fixed ornament','top_cover',(88,0,35),(5,8,3.4),s.metal,.4)
s.poly('Rear mechanical sight seat','top_cover',[(-31,32),(-16,32),(-14,37),(-25,38)],8,s.metal,.3)
s.box('Rear fixed sight block','top_cover',(-17,0,39),(4,8,2.7),s.metal,.3)
for sy in [-1,1]:s.box('Rear notch wing','top_cover',(-17,sy*2.6,41),(3,1.8,2.2),s.metal,.2)

stock=s.poly('Walnut double-opening stock','stock',[(88,22),(187,22),(189,17),(186,-21),(92,-17),(82,9)],15.7,wood,1.15)
s.cut(stock,s.poly('Large thumb opening cutter','stock',[(108,15),(143,15),(143,-10),(111,-7),(104,5)],24,s.dark,2.7))
s.cut(stock,s.poly('Rear sling-shaped opening cutter','stock',[(166,13),(178,13),(178,-2),(166,-2)],24,s.dark,2.2))
s.poly('Grip raised palm shape','stock',[(90,12),(104,10),(108,-8),(113,-15),(94,-16),(88,-1)],16.05,wood_high,.7)
s.poly('Rear black rubber pad','stock',[(186,23),(190,22),(189,-22),(185,-22)],16.8,s.rubber,.6)
for z in range(-19,22,3):s.box('Butt pad relief rib','stock',(189.1,0,z),(.6,17.1,1.0),s.polymer,.18)
for sy in [-1,1]:
    for x,z in [(97,16),(153,16),(179,-13)]:s.screw('Stock exterior screw','stock',x,z,sy*7.9,.8)
    # Grain lines stay inside three solid regions and do not bridge stock openings.
    for row in range(10):
        z=-18+row*.68
        s.line('Stock lower walnut grain','stock',(116,sy*7.97,z),(179,sy*7.97,z+1.4*math.sin(row)),.065,wood_high if row%2 else wood_dark)['print_skip']=True
    for row in range(6):
        s.line('Stock upper walnut grain','stock',(112,sy*7.95,17+row*.63),(180,sy*7.95,17+row*.63),.06,wood_high)['print_skip']=True
    for row in range(12):
        z=-6+row*1.4
        s.line('Stock rear walnut grain','stock',(148,sy*7.96,z),(160,sy*7.96,z+1),.06,wood_dark if row%3==0 else wood_high)['print_skip']=True

s.poly('Solid short magazine','magazine',[(0,13),(29,12),(31,-24),(5,-20),(2,-15)],13,s.metal,.7)
s.poly('Magazine bottom rim','magazine',[(3,-18),(31,-22),(31,-26),(3,-22)],14.3,s.polymer,.4)
for sy in [-1,1]:
    s.poly('Stamped magazine side panel','magazine',[(5,5),(25,5),(26,-17),(8,-15)],.32,s.dark,.5,y=sy*6.52)
    for x in [8,14,20,26]:s.box('Magazine vertical stamped rib','magazine',(x,sy*6.74,-6),(1.1,.6,22),s.metal,.3)
    for z in [0,-11]:s.box('Magazine transverse rib','magazine',(17,sy*6.9,z),(20,.6,1.4),s.metal,.3)

guard=s.poly('Fixed trigger guard silhouette','controls',[(47,10),(80,9),(83,-8),(76,-12),(55,-12),(49,-7)],6,s.metal,.75)
s.cut(guard,s.poly('Trigger guard opening','controls',[(53,5),(76,5),(77,-5),(73,-8),(56,-8)],12,s.dark,.7))
s.poly('Fixed trigger appearance','controls',[(66,9),(70,9),(71,-2),(67,-7),(64,-7),(67,-1)],2.5,s.steel,.3)
s.cyl('Fixed side lever root','controls',(75,-9,22),2.1,2.6,s.metal,'Y',.2)
s.line('Fixed ornamental charging stem','controls',(75,-8.8,22),(80,-14,24),1.25,s.metal)
s.box('Fixed charging tab','controls',(81,-14,24),(7,3.5,2.8),s.metal,.6)
s.poly('Selector surface ornament','controls',[(60,14),(66,15),(70,20),(74,20),(70,12),(63,10)],.9,s.metal,.3,y=9)
s.box('Magazine catch fixed ornament','controls',(34,0,5),(4.5,6,8),s.metal,.4)

# Optional optic is a closed decorative approximation, not present on the base screenshot.
s.box('Optic closed side foot','optic',(48,-10.4,24),(30,5,8),s.metal,.5)
s.poly('Optic raised support silhouette','optic',[(36,23),(55,23),(58,43),(52,46),(40,43)],6,s.metal,.6,y=-8)
s.box('Optic cross bridge','optic',(48,-3,45),(50,17,6),s.metal,.5)
s.cyl('Opaque optic main tube','optic',(47,0,53),4.1,61,s.metal,'X',.25)
s.cone('Opaque optic forward bell','optic',(9,0,53),6.8,4.1,19,s.metal)
s.cyl('Optic front protective sleeve','optic',(-3,0,53),6.8,7,s.polymer,'X',.3)
s.cyl('Solid tinted front optic face','optic',(-6.65,0,53),5.8,.3,s.glass,'X',.05)
s.cyl('Optic rear eyecup solid','optic',(85,0,53),5.7,16,s.rubber,'X',.4)
s.cyl('Opaque rear optic face','optic',(93.1,0,53),4.6,.25,s.glass,'X',.05)
for x in [29,67]:
    s.cyl('Optic raised ring','optic',(x,0,53),5.3,5,s.metal,'X',.3)
    s.box('Optic ring foot','optic',(x,0,46.5),(5,8,8),s.metal,.4)
for x in [78,81,84,87,90]:s.cyl('Optic eyecup rib','optic',(x,0,53),5.9,.8,s.metal,'X',.12)
s.cyl('Optic elevation dial','optic',(48,0,60),4.1,5,s.metal,'Z',.3)
s.cyl('Optic side dial','optic',(48,-6,53),3.8,5,s.metal,'Y',.3)
for i in range(24):
    a=i*math.tau/24
    s.box('Optic knob knurl','optic',(48+4*math.cos(a),4*math.sin(a),60),(.5,.5,3.8),s.polymer,.12)

# A lengthwise glue plane crosses the solid fore-end just before the receiver.
s.scene['print_segment_breaks_x_mm']=json.dumps([0])
sources=['https://zilliongamer.com/delta-force/c/weapons/best-svd-build-delta-force','https://zilliongamer.com/uploads/delta-force/weapons-builds/marksman-rifle/svd/svd-delta-force-build.jpg']
approx=['已实际查看游戏基础截图：木色双开孔枪托、木护木、短外露前端和短弹匣；默认不含光学瞄具。','尺寸为380mm桌面微缩雕塑设计值，不来源于真实武器尺寸；隐藏侧、顶部、细小五金及木纹位置为艺术推断。','可选瞄具是独立外观装饰，其封闭镜片和实心支座没有功能性内部结构或真实接口。','木纹细线为网页显示保留，打印时跳过；实体基础款整体融合后平面胶合。']
result=s.finish(sources,approx)
(s.out/'SOURCE_NOTES.md').write_text('# SVD 参考与重建说明\n\n'+ '\n'.join('- '+u for u in sources)+'\n\n'+ '\n'.join('- '+p for p in approx)+'\n',encoding='utf-8')
