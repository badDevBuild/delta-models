"""FS-12 base-outline folding-style shotgun miniature; all components fixed art."""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_fs12_helpers import *
s=begin('fs12',280,[('receiver','银灰折线式长机匣'),('front','上下并列封闭前杆'),('forearm','黑色泵式护木外观'),('stock','后铰链外壳与三角尾托'),('grip','黑色弧线握把'),('controls','固定护圈与连接圆盖'),('details','机匣斜线与小五金'),('sights','低顶轨与机械瞄具')])
gray=s.mat('Satin dark silver shell',(.25,.27,.29),.71,.43)
s.poly('Distinct stepped solid receiver','receiver',[(-30,14),(-30,40),(25,40),(33,34),(50,31),(55,24),(52,10),(35,8),(-8,8),(-19,12)],22.3,gray,.85)
s.poly('Upper steep receiver shoulder','receiver',[(-31,34),(-29,42),(26,42),(32,36),(48,31),(48,27),(-18,27)],18.5,s.steel,.7)
for sign in [-1,1]:
 s.poly('Broad silver side cover','receiver',[(-29,29),(27,29),(32,26),(47,25),(46,14),(-8,13),(-22,18),(-29,17)],.65,gray,.55,y=sign*11.1)
 s.box('Closed longitudinal receiver seam','receiver',(-1,sign*11.48,31),(48,.23,.85),s.dark,.25)
 for j in range(6):
  x=-25+j*7.3
  o=s.box('Receiver slanted shallow relief','details',(x,sign*11.2,36.1),(1.1,.3,5.4),s.polymer,.16);o.rotation_euler[1]=-.27
 s.screw('Receiver side fixed fastener','details',43,17,sign*11.52,.8)
 s.screw('Receiver side fixed fastener','details',16,16,sign*11.52,.7)
 s.cyl('Large fixed forward pivot cover','controls',(-26,sign*11.4,17),3.3,.8,s.steel,'Y',.3)
 s.cyl('Pivot blind central disc','controls',(-26,sign*11.87,17),1.4,.17,s.dark,'Y',.1)
for z,r,end in [(31,4.2,-24),(21,4.0,-26)]:
 s.cyl('Long solid parallel front rod','front',((-140+end)/2,0,z),r,end+140,s.metal,'X',.3)
 s.cyl('Opaque sealed rod front','front',(-140.08,0,z),r*.63,.16,s.dark,'X',.1)
s.box('Parallel rod front join collar','front',(-135,0,26),(7.5,12,19),s.metal,.5)
s.box('Parallel rod receiver join','front',(-30,0,26),(8,13,20),s.metal,.5)
s.poly('Solid elongated pumping forearm','forearm',[(-114,20),(-113,29),(-104,33),(-57,32),(-50,26),(-53,16),(-63,13),(-106,14)],19.8,s.polymer,.95)
for sign in [-1,1]:
 s.poly('Forearm textured inset','forearm',[(-108,24),(-101,29),(-63,28),(-58,24),(-61,18),(-103,18)],.6,s.rubber,.6,y=sign*9.8)
 for j in range(13):
  x=-104+j*3.4
  s.line('Forearm short textured raised stroke','forearm',(x,sign*10.05,19),(x+1.5,sign*10.05,26),.25,s.metal)
s.poly('Rear fixed hinge neck','stock',[(49,28),(64,27),(76,22),(77,16),(61,14),(51,13)],18,s.metal,.75)
s.cyl('Fixed folded-style hinge pivot','stock',(68,0,21),5.5,22,s.metal,'Y',.45)
s.cyl('Solid slim rear stock tube','stock',(91,0,23),4.0,48,s.steel,'X',.3)
s.poly('Upper rear cheek shell','stock',[(92,28),(136,28),(140,24),(137,20),(96,18),(90,20)],13.7,s.polymer,.7)
st=s.poly('Triangular stock tail silhouette','stock',[(98,23),(137,24),(140,-7),(132,-11),(128,-10),(101,7)],11.5,s.polymer,.8)
s.cut(st,s.poly('Rear stock decorative opening','stock',[(107,18),(132,19),(133,-2),(128,-3),(109,8)],25,s.dark,.65))
s.box('Thick rubber stock terminal','stock',(140,0,9),(4.8,16,42),s.rubber,.7)
grip(s,'grip',36,13,s.polymer,7.5,.90);guard(s,13,13,29,20)
for sign in [-1,1]:
 s.cyl('Rear hinge round surface disc','details',(68,sign*11.15,21),2.5,.4,s.steel,'Y',.2)
 s.cyl('Fixed safety small button','controls',(43,sign*11.3,14),1.7,.6,s.metal,'Y',.2)
s.rail('sights',-29,27,42.2,6.8,4)
s.box('Fixed front sight pedestal','sights',(-136,0,38),(6.5,8.5,8),s.metal,.45)
s.box('Front low sight marker','sights',(-136,0,43),(2,3,3.5),s.polymer,.3)
s.box('Receiver rear low blade','sights',(23,0,45),(4.2,7,4.5),s.polymer,.4)
optic(s,1,45.0,.94)
result=finish(s,['https://www.shacknews.com/article/147698/how-to-get-the-fs-12-shotgun-in-delta-force','https://d1lss44hh2trtw.cloudfront.net/assets/editorial/2026/02/delta-force-unlock-fs-12-shotgun-operations-craft.jpg','https://gamewith.jp/deltaforce/542358','https://img.gamewith.jp/article_tools/deltaforce/gacha/w_62.png'],['主体参考新武器解锁画面与基础图标：银灰斜肩机匣、黑色泵式护木、上下长杆、独立握把与骨架尾托。','基础形态不装资料站改装图的下置大鼓匣；尾托小图分辨率低，托架细节为艺术推断，铰链仅静态表面造型。'],cut=-38)
