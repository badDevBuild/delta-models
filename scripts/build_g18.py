"""G18 exterior sculpture. Fixed closed miniature, no mechanical interfaces."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_amg import Sculpture
s=Sculpture('g18',70)
for k,l,v in [('frame','握把与框架外观',True),('slide','封闭套筒外观',True),('muzzle','封闭短前端',True),('magazine','实心弹匣底部外观',True),('front_sight','前固定机械瞄具',True),('rear_sight','后固定机械瞄具',True),('light','可选灯具装饰',False)]:s.part(k,l,v)
slide=s.mat('Dark machined slide',(.075,.088,.096),.68,.4)
panel=s.mat('Fine polymer relief',(.065,.073,.077),.04,.72)

# Slide is a filled sculpture; all recesses are shallow and sealed.
upper=s.poly('Solid slide exterior','slide',[(-32,23.6),(-29.5,25),(28,25),(29.5,23.3),(29.5,16),(-32,16)],11.7,slide,.75)
s.poly('Slide upper chamfer','slide',[(-31,24.1),(-29.5,25),(28,25),(29,24.1)],10.5,s.edge,.15)
s.box('Solid slide top center','slide',(-1,0,24.98),(54,6.8,.25),slide,.08)
for sign in [-1,1]:
    # Game-visible serrations with genuine blind recess geometry.
    for x in [-23,-20.9,-18.8,-16.7,-14.6,17.2,19.3,21.4,23.5,25.6]:
        cutter=s.poly('Temporary blind serration','slide',[(x,23.4),(x+.85,23.4),(x+.55,17.4),(x-.3,17.4)],1.2,s.dark,.15,y=sign*5.75)
        s.cut(upper,cutter)
    s.poly('Slide lower relief contour','slide',[(-28,17),(-7,17),(-5,18),(-5,19),(-28,19)],.17,s.dark,.3,y=sign*5.88)
    s.box('Blank slide identification inset','slide',(5,sign*5.91,20.8),(10,.18,2.7),slide,.18)
    for i in range(4):s.box('Small non-letter maker mark','slide',(1.5+i*1.7,sign*6.03,20.8),(.8,.12,.35),s.edge,.04)
s.box('Sealed top recess border','slide',(3,0,25.08),(11,5.5,.25),s.dark,.35)
s.box('Sealed top recess metal face','slide',(3,0,25.24),(9.7,4.3,.25),s.steel,.25)
s.box('Slide rear cap','slide',(29.53,0,20.4),(.35,8.5,6.9),s.polymer,.4)
s.cyl('Fixed rear side selector dial','slide',(24,-6.3,20),1.8,1.1,s.metal,'Y',.15,32)
s.poly('Fixed selector lever decoration','slide',[(23,20.8),(26.5,22),(27.2,21),(24,19.2)],.7,s.polymer,.3,y=-7)

# Frame and angled grip, merged-looking but individually editable surface details.
s.poly('Upper polymer frame','frame',[(-31.7,16.1),(29.7,16.1),(30.8,13),(28,10),(19,9),(13,10),(7,11),(-12,10),(-15,12),(-31.7,12)],12,s.polymer,.65)
s.poly('Grip main silhouette','frame',[(10,12),(28,11),(27,6),(29,-5),(35,-19),(33,-22),(21,-22),(16,-17),(14,-7),(10,0),(8,7)],12.9,s.polymer,1.2)
for sign in [-1,1]:
    s.poly('Grip molded upper scallop','frame',[(14,7),(24,7),(26,4),(24,2),(16,3),(13,4)],.6,panel,.6,y=sign*6.45)
    s.poly('Grip checkered panel backing','frame',[(15,1),(25,0),(32,-18),(22,-19),(18,-13)],.5,panel,.65,y=sign*6.49)
    # Individual small pyramid-like cubes give visible relief at close inspection.
    for row in range(14):
        z=-.3-row*1.15;start=16.7+max(0,row-2)*.34
        for j in range(7):
            x=start+j*1.05
            o=s.box('Grip raised micro checkering','frame',(x,sign*6.88,z),(.61,.40,.61),s.polymer,.12)
            o.rotation_euler[1]=.22
    s.box('Fixed frame side lever','frame',(14.5,sign*6.38,12),(4.0,.9,1.25),s.metal,.28)
    for x in [13.1,14.2,15.3]:s.box('Side lever grip ridge','frame',(x,sign*6.92,12),(.33,.18,1.05),s.edge,.08)
    s.screw('Frame cosmetic pin','frame',-.5,13,sign*6.1,.64)
    s.screw('Rear frame cosmetic pin','frame',19,10,sign*6.1,.65)
    s.box('Fixed magazine catch ornament','frame',(11,sign*6.68,5.3),(2.0,.85,2.4),s.metal,.3)
for i in range(3):
    z=-3.5-i*5.2;x=14.2+i*1.35
    s.poly('Front grip finger ridge','frame',[(x-1,z+1.0),(x+.1,z+1.3),(x+1.7,z-.9),(x+1.9,z-2),(x+.7,z-2.4)],11.4,panel,.5)
for z,x in [(-4.5,28.2),(-8,29.6),(-11.5,31),(-15,32.6)]:s.box('Backstrap texture ridge','frame',(x,0,z),(1.05,10.8,.48),panel,.15)
s.box('Front lower accessory rail sculpture','frame',(-23,0,11.65),(17,9.5,1.4),s.polymer,.45)
for x in [-28,-23,-18]:s.box('Non-standard front rail ridge','frame',(x,0,10.85),(1.1,10.1,.75),s.metal,.16)
guard=s.poly('Fixed trigger guard outer','frame',[(-12,11),(10,11),(13,6),(12,-.5),(8,-3),(-11,-3),(-13,0)],7.8,s.polymer,.9)
s.cut(guard,s.poly('Open exterior trigger guard','frame',[(-9,8),(7,8),(9,5),(9,1),(6,-.7),(-9,-.7),(-10,1)],20,s.dark,.6))
s.poly('Fixed trigger silhouette','frame',[(2,10),(5,10),(6,5),(4,1),(1,-.4),(.3,1.1),(2.7,3.5),(3,6)],2.7,s.metal,.4)
s.poly('Fixed trigger central relief','frame',[(3.1,9),(4.2,9),(4.7,5),(3.3,2),(2.6,2.4),(3.7,5)],.5,s.dark,.1,y=-1.45)
for z in [-1,1,3,5,7]:s.box('Guard front texture relief','frame',(-12.7,0,z),(.5,7.2,.5),panel,.12)

# No bore: separate sealed nose and lower nose boss touch the slide/frame.
s.cyl('Short solid muzzle ornament','muzzle',(-33.3,0,20.8),2.15,3.4,s.metal,'X',.2)
for x in [-34.4,-33.7,-33]:s.cyl('Muzzle shallow circumferential relief','muzzle',(x,0,20.8),2.25,.23,s.edge,'X',.05)
s.cyl('Closed dark muzzle face','muzzle',(-35.05,0,20.8),1.45,.18,s.dark,'X',.03)
s.cyl('Lower solid front boss','muzzle',(-32.3,0,14.5),1.7,1.1,s.metal,'X',.15)
s.cyl('Lower closed front face','muzzle',(-32.9,0,14.5),1.25,.15,s.dark,'X',.03)
s.box('Buried miniature nose bridge','muzzle',(-32.0,0,17.4),(1.2,2.9,6.0),s.metal,.25)

# Magazine is solid with no feed geometry; only visible base is represented.
s.poly('Solid decorative magazine foot','magazine',[(20,-20.3),(33,-20.3),(34.6,-22.5),(33.8,-24),(20,-24),(19,-22)],13.6,s.metal,.55)
s.box('Magazine base lower pad','magazine',(26.9,0,-23.8),(14.7,13.8,1),s.polymer,.4)
for sign in [-1,1]:s.box('Magazine base side seam','magazine',(27,sign*6.91,-22.5),(11,.18,.35),s.edge,.1)

s.box('Front fixed sight base','front_sight',(-27,0,25.3),(3.3,3.4,.9),s.metal,.2)
s.box('Front fixed sight post','front_sight',(-27,0,26.2),(1.4,1.4,1.4),s.polymer,.23)
s.box('Front sight pale inlay','front_sight',(-26.24,0,26.25),(.12,.72,.65),s.edge,.08)
s.box('Rear fixed sight base','rear_sight',(25,0,25.5),(4,7,1.1),s.metal,.25)
for sign in [-1,1]:
    s.box('Rear sight ear','rear_sight',(25,sign*2.1,26.2),(2.3,1.7,2.1),s.polymer,.23)
    s.box('Rear sight pale inlay','rear_sight',(26.2,sign*2.1,26.2),(.12,.7,.75),s.edge,.08)

# Optional opaque flashlight accessory with deliberately arbitrary miniature foot.
s.box('Light accessory solid foot','light',(-22,0,9.5),(14,9,2.7),s.metal,.4)
s.box('Light accessory body','light',(-22,0,5.1),(13,10,7),s.polymer,.85)
s.cyl('Light front cap','light',(-29.5,0,5),4.8,3.6,s.metal,'X',.3)
s.cyl('Light opaque glass','light',(-31.35,0,5),3.6,.3,s.glass,'X',.1)
for sign in [-1,1]:s.box('Light cosmetic button','light',(-17,sign*5.15,5),(2.5,.7,3.3),panel,.3)
result=s.finish([
 'https://xtopup.com/news/delta-force-the-most-powerful-weapons-in-the-current-version',
 'https://global-res.xtopup.com/xw_20240604175855/sjzhd_20250212151137/delta_force_g18_202502121540.jpg',
 'https://df-build.com/builds/g18/'
],['以已查看的游戏基础黑色 G18 截图为主，保留前后套筒斜纹、倾斜握把、握把颗粒和固定瞄具。', '背面、顶部、底部及颗粒排布是艺术推断；未复制商标或提取游戏资源。', '约 70 mm 微缩实心装饰；套筒、弹匣和扳机均无实际运动或内部功能，灯具是可选不发光装饰。'])
