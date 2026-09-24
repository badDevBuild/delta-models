"""MK4 short AR-like exterior sculpture with slender magazine."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_compact_helpers import *
s=begin('mk4',230,[('receiver','紧凑分层机匣'),('handguard','短镂槽外观护木'),('front','封闭短前端'),('stock','细管与三角骨架托'),('grip','紧凑斜握把'),('magazine','细长直身实心弹匣'),('controls','固定控制装饰与护圈'),('sights','短轨与折叠式外观瞄具')])
s.poly('Compact stepped upper shell','receiver',[(-28,18),(-31,33),(-25,39),(36,39),(42,34),(42,21),(27,16),(13,13),(-18,13)],18.5,s.metal,.75)
s.poly('Lower receiver with magazine shoulder','receiver',[(-25,23),(36,23),(39,15),(29,9),(15,9),(12,4),(-6,1),(-22,4),(-24,14)],17.2,s.metal,.7)
s.poly('Upper long cover facet','receiver',[(-23,39),(31,40),(38,36),(37,32),(-29,32)],15.5,s.edge,.55)
for side in [-1,1]:
 s.box('Closed lateral recess','receiver',(5,side*9.23,30),(35,.3,3.1),s.dark,.8)
 s.box('Shallow long side cover','receiver',(7,side*9.55,26),(26,.7,4),s.metal,.55)
 s.poly('Forward lower receiver panel','receiver',[(-21,20),(-5,20),(-4,7),(-20,9)],.45,s.polymer,.45,y=side*8.65)
 s.cyl('Fixed rear circular cover','receiver',(34,side*9.25,26),2.2,.6,s.steel,'Y',.25)
screws(s,'receiver',[(-21,24),(31,17)],9.27,.85)
h=s.poly('Short faceted handguard','handguard',[(-92,20),(-94,33),(-87,39),(-29,39),(-25,34),(-27,17),(-84,16)],20.3,s.metal,.7)
for x in [-83,-69,-55,-41]:slot(s,h,'handguard',x,26,10,4.1,1.3,10.05)
for side in [-1,1]:
 for i in range(8):
  x=-85+i*7.4
  o=s.box('Upper handguard diagonal relief','handguard',(x,side*10.1,34),(3,.6,4.6),s.polymer,.4);o.rotation_euler[1]=-.35
 for x in [-89,-29]:s.screw('Handguard fixed screw','handguard',x,21,side*10.15,.7)
s.box('Forearm lower ledge','handguard',(-58,0,16.5),(61,12.2,3),s.polymer,.5)
front(s,'front',-114,-91,27.4,3.2,4.3)
s.cyl('Short end shroud solid','front',(-108,0,27.4),4.6,13,s.metal,'X',.35)
for side in [-1,1]:s.box('Front shroud blind stripe','front',(-107,side*4.2,27.4),(6.5,.35,1.8),s.dark,.5)
s.poly('Thin straight magazine solid','magazine',[(-21,6),(-3,4),(-5,-54),(-8,-59),(-24,-58),(-26,-54)],11.5,s.polymer,.7)
for side in [-1,1]:
 for x in [-21,-8]:s.box('Magazine long edge rib','magazine',(x,side*5.73,-25),(1.1,.55,54),s.metal,.2)
 for z in [-5,-17,-29,-41,-51]:s.box('Magazine horizontal recessed band','magazine',(-15,side*5.92,z),(16,.24,.65),s.dark,.15)
s.box('Plain solid magazine foot','magazine',(-15,0,-58),(24,14,4.1),s.metal,.6)
grip(s,'grip',25,14,s.polymer,7.5,.92);guard(s,4,14,28,19)
s.cyl('Solid decorative stock tube','stock',(67,0,29),4.5,60,s.metal,'X',.35)
s.cyl('Stock tube collar','stock',(43,0,29),6,6,s.steel,'X',.3)
s.poly('Stock top cheek sleeve','stock',[(65,35),(113,35),(116,29),(110,24),(69,24),(64,27)],14,s.polymer,.85)
st=s.poly('Angular triangular stock shell','stock',[(70,27),(112,29),(114,1),(107,-6),(99,-6),(74,12)],12,s.polymer,.8)
s.cut(st,s.poly('Stock silhouette window','stock',[(79,22),(106,23),(105,2),(101,0),(81,13)],24,s.dark,.7))
s.box('Rubber stock end pad','stock',(114,0,14),(4.5,17,45),s.rubber,.8)
for side in [-1,1]:
 s.poly('Diagonal stock surface rib','stock',[(79,11),(102,-3),(104,-1),(81,13)],.6,s.metal,.3,y=side*6.0)
 s.cyl('Small fixed stock cover','stock',(104,side*7.1,27),1.8,.7,s.metal,'Y',.25)
 s.cyl('Fixed selector disk','controls',(28,side*9.6,18),2.0,.7,s.metal,'Y',.25)
 s.line('Selector static lever','controls',(28,side*10,18),(23,side*10,16),.75,s.steel)
 s.box('Fixed short bolt release','controls',(-2,side*9.8,23),(3.8,1.5,6),s.steel,.45)
sights(s,-91,38,39.2,6.8);optic(s,6,42.2,1)
result=finish(s,['https://ol.3dmgame.com/gl/323788.html','https://olimg.3dmgame.com/uploads/images/raiders/20251117/1763344376_550400_png_r.webp','https://g.aitags.cn/wp-content/uploads/2025/11/image-22.webp',REF],['按游戏展示截图的紧凑AR式机匣、短护木、细长直匣和三角骨架托绘制；不将资料图的鼓形前握把和长抑制筒作为基础配置。','未取得纯默认双侧正视图，短前端、握把侧纹和顶部为有说明的艺术推断；长短前端选型并非已验证官方默认。'],cut=-44)
