"""RM277 tan bullpup game-outline sculpture."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_compact_helpers import *
s=begin('rm277',290,[('receiver','沙色分层无托机身'),('handguard','长方护木与黑色侧片'),('front','封闭长前杆与端帽'),('stock','高贴腮板与后托轮廓'),('grip','黑色下斜握把'),('magazine','后置长方实心弹匣'),('controls','固定护圈及控制装饰'),('sights','低轨与固定瞄具')])
tan=s.mat('Earth tan alloy',(.30,.23,.145),.4,.55);sand=s.mat('Light tan polymer',(.37,.32,.22),.08,.66)
s.poly('Upper angular solid body','receiver',[(-20,23),(-24,38),(-16,43),(128,43),(139,37),(140,16),(99,15),(83,7),(51,8),(34,13),(4,14)],23.5,tan,.8)
s.poly('Lower angled chassis','receiver',[(-11,23),(137,23),(138,14),(125,4),(108,5),(98,11),(80,5),(47,8),(36,16),(-6,15)],22,sand,.85)
for side in [-1,1]:
 s.poly('Closed side faceted shoulder','receiver',[(-8,34),(79,34),(82,25),(73,22),(-3,22)],.5,tan,.4,y=side*11.74)
 s.box('Long shallow seam','receiver',(33,side*11.98,37),(77,.23,1.1),s.dark,.23)
 for x in [4,9,14]:
  obj=s.box('Angled receiver shallow strokes','receiver',(x,side*12.07,29),(1.2,.25,5.3),sand,.2);obj.rotation_euler[1]=-.22
 s.box('Silver rear cover inset','receiver',(107,side*11.9,30),(43,.5,6.2),s.steel,.5)
 s.box('Rear cover dark stripe','receiver',(112,side*12.22,29),(26,.22,1.5),s.dark,.25)
screws(s,'receiver',[(1,19),(57,20),(78,25),(132,34)],11.85,.82)
h=s.poly('Long square forearm','handguard',[(-88,20),(-91,30),(-89,41),(-17,41),(-13,34),(-13,17),(-79,15)],24,tan,.75)
for x in [-78,-62,-46,-30]:slot(s,h,'handguard',x,33,11,3.1,1.2,11.92)
for side in [-1,1]:
 for x,w in [(-72,21),(-38,31)]:
  s.box('Black textured forearm panel','handguard',(x,side*12,24),(w,.9,8.0),s.polymer,.5)
  for i in range(int(w/2.5)):s.line('Fine grip panel diagonal','handguard',(x-w/2+1+i*2.5,side*12.56,21),(x-w/2+3+i*2.5,side*12.56,27),.21,s.metal)
 s.screw('Forearm fore fastener','handguard',-84,21,side*12,.95)
 s.box('Forearm lower linear ledge','handguard',(-49,side*8,16),(68,2,2.3),sand,.35)
front(s,'front',-145,-86,28,3.1,4.2)
s.cyl('Long solid front end shroud','front',(-130,0,28),5.1,30,s.metal,'X',.45)
for side in [-1,1]:s.box('Front shroud blind long stripe','front',(-131,side*4.7,28),(19,.5,2),s.dark,.7)
s.box('Opaque sealed shroud front','front',(-145.1,0,28),(.25,6.1,5.4),s.dark,1.3)
s.poly('Rear shoulder lower outline','stock',[(101,20),(138,19),(141,12),(139,-9),(125,-8),(119,1),(105,4)],23,sand,.85)
for side in [-1,1]:s.poly('Solid blind triangular rear inlay','stock',[(117,10),(135,13),(134,-2),(127,-1)],.45,s.dark,.55,y=side*11.5)
s.box('Thick vertical rubber end pad','stock',(142,0,17),(5.6,26,56),s.rubber,.8)
s.poly('High cheekpad','stock',[(81,43),(87,48),(134,48),(140,44),(139,39),(84,39)],22,s.polymer,.7)
s.poly('Long solid rear magazine','magazine',[(56,9),(83,8),(86,-41),(81,-48),(52,-48),(52,-26)],17.5,s.polymer,.85)
for side in [-1,1]:
 for z in [-7,-15,-23,-31]:s.line('Magazine diagonal shallow rib','magazine',(54,side*8.8,z),(82,side*8.8,z-5),.45,s.metal)
 s.poly('Tan magazine bottom wrap','magazine',[(51,-37),(86,-38),(85,-48),(52,-48)],.7,sand,.5,y=side*8.7)
s.box('Broad magazine foot','magazine',(68,0,-49),(36,20,4.2),tan,.55)
grip(s,'grip',20,17,s.polymer,8,.95);guard(s,-1,18,32,21,mat=sand)
for side in [-1,1]:
 s.box('Fixed small release switch','controls',(-4,side*12,20),(4,1.3,4.0),s.metal,.4)
 s.cyl('Fixed selector dial','controls',(25,side*12,23),1.9,.8,s.metal,'Y',.18)
 s.box('Shallow receiver forward stop','controls',(-19,side*12,29),(3,1.7,8),s.metal,.5)
s.box('Continuous forearm rail riser','handguard',(-50,0,42),(76,7.4,3.3),tan,.25)
sights(s,-87,132,43.5,7.4);optic(s,21,46.5,1)
result=finish(s,['https://gamewith.jp/deltaforce/565803','https://img.gamewith.jp/img/original_9d898b0abe0387b9e98c2d34732dbeba.jpg','https://game.xiaomi.com/viewpoint/1543075652_1781229900126_16'],['以游戏展示图的沙色长机身、长前杆、后置弹匣、黑色贴腮板与后托凹面为主要外形；图中光学镜作为可切换装饰，图中改装握把未当成默认。','未获得无附件正投影视图，基础比例、背面与前端细节为图像重建推断，非逐件官方精确复刻。'],cut=-34)
