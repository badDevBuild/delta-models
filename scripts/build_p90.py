"""P90 miniature exterior: side silhouette reviewed against the game reference.

Coordinates follow the viewed reference image for visual proportions only.
All solids are filled; this contains no real internal/interface geometry.
"""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_helpers_ap import Model
m=Model('p90','P90 · 深色基础外观',170)
S=170/552
X=lambda px:(px-657)*S
Z=lambda py:(350-py)*S
P=lambda px,y,py:(X(px),y,Z(py))
polymer=m.mat('P90 charcoal polymer',(.053,.064,.068),.04,.68)
panel=m.mat('P90 inset graphite polymer',(.040,.048,.053),.02,.72)
edge=m.mat('P90 molded shoulder',(.088,.104,.108),.05,.61)
metal=m.mat('P90 anodized upper housing',(.073,.085,.091),.72,.36)
steel=m.mat('P90 dark steel furniture',(.11,.127,.131),.76,.34)
highlight=m.mat('P90 softened edge',(.17,.19,.19),.73,.35)
dark=m.mat('P90 blind recess shadow',(.012,.019,.022),.1,.75)
rubber=m.mat('P90 rubber butt plate',(.022,.029,.032),0,.86)
magmat=m.mat('P90 opaque smoke magazine',(.072,.073,.056),.15,.43)
magband=m.mat('P90 molded magazine edge',(.11,.12,.104),.17,.4)
glass=m.mat('P90 filled optical face',(.013,.092,.115),.4,.17)
for k,label in [('body','聚合物一体主体'),('magazine','上置实心弹匣外观'),('upper','高架外观框架'),('sight','固定一体瞄具'),('barrel','封口短前端'),('butt','后端胶垫')]:m.part(k,label)
def prof(name,key,points,depth,mat=polymer,b=.6,y=0):return m.poly(name,key,[(X(x),Z(z)) for x,z in points],depth,mat,b,y)
def box(name,key,px,y,py,w,d,h,mat=polymer,b=.4):return m.box(name,key,P(px,y,py),(w*S,d,h*S),mat,b)
def line(name,key,points,r,mat=steel):return m.path(name,key,[(X(px),y,Z(py)) for px,y,py in points],r,mat)
def screw(name,key,px,py,y,r=1):return m.screw(name,key,X(px),Z(py),y,r,steel,dark)

outline=[(455,343),(751,339),(756,308),(780,305),(912,307),(927,315),(928,419),(921,427),(775,426),(714,439),(692,452),(666,455),(638,452),(616,446),(598,430),(585,416),(550,416),(554,451),(542,455),(506,454),(491,449),(482,438),(477,421),(474,403),(464,393)]
body=prof('P90 continuous exterior shell','body',outline,16.6,polymer,1.8)
trigger=[(508,378),(523,370),(549,370),(566,375),(574,386),(571,399),(559,407),(542,411),(526,409),(512,402),(505,391)]
thumb=[(633,372),(682,372),(696,378),(702,389),(699,399),(689,409),(675,415),(658,416),(641,410),(630,402),(623,392),(624,382)]
for label,pts in [('trigger opening',trigger),('thumb opening',thumb)]:m.cut(body,prof('Temporary '+label,'body',pts,30,dark,1.5))
# Foremost flange is a fixed sculpture, joined to the shell rather than a real rail.
prof('Front lower integrated flange','body',[(383,371),(454,371),(466,363),(478,361),(476,382),(460,387),(439,382),(383,382)],12.7,metal,.55)
for i in range(10):box('Flange shallow serration','body',391+i*7.3,0,371,4.4,14,2.8,steel,.18)
for side in [-1,1]:
    y=side*8.33
    prof('Front shallow cheek facet','body',[(467,349),(574,349),(579,367),(556,370),(522,369),(493,382),(484,396),(470,389)],.42,edge,.7,y)
    prof('Rear lower stock contour panel','body',[(777,371),(913,371),(913,415),(783,416),(772,406)],.35,panel,.7,y)
    prof('Rear upper cheek contour','body',[(765,312),(788,309),(909,312),(914,323),(914,344),(768,343)],.4,edge,.8,y)
    line('Rear lower panel seam','body',[(780,side*8.5,374),(908,side*8.5,374),(908,side*8.5,410),(784,side*8.5,410)],.17,polymer)
    line('Long body parting seam','body',[(467,side*8.5,364),(574,side*8.5,364),(619,side*8.5,365),(769,side*8.5,365),(914,side*8.5,365)],.18,dark)
    line('Thumb heel shallow molding','body',[(602,side*8.35,427),(619,side*8.35,442),(644,side*8.35,448),(675,side*8.35,450),(693,side*8.35,445)],.21,edge)
    line('Front heel shallow molding','body',[(486,side*8.35,425),(492,side*8.35,440),(509,side*8.35,448),(544,side*8.35,448)],.21,edge)
    for px,py,r in [(476,355,.95),(530,435,.85),(631,431,.85),(718,437,.85),(782,413,.8),(897,414,.8),(784,328,1.0),(831,337,.8),(897,340,.8)]:screw('Shell external fastener','body',px,py,side*8.7,r)
    box('Fixed external charging tab pad','body',522,side*8.7,356,96,.9,12,metal,.55)
    box('Fixed external charging tab','body',551,side*9.55,357,17,2.2,10,steel,.5)
    for i in range(4):box('Tab shallow grip rib','body',546+i*3.2,side*10.65,357,1.2,.25,7,dark,.06)
    # Small, shallow molded ribs sit on the outer front grip wall.
    for i in range(8):line('Front grip molded rib','body',[(482,side*8.2,401+i*3.0),(489,side*8.35,400+i*3.0)],.17,panel)
    for i in range(6):box('Rear lower molded rib','body',810+i*12,side*8.57,412,2.5,.22,7.0,polymer,.14)
# Decorative trigger is permanently joined to the upper inside edge.
prof('Fixed trigger silhouette','body',[(554,366),(561,369),(563,385),(558,397),(550,402),(546,401),(553,390),(555,378)],3.3,metal,.35)
box('Fixed selector ornament','body',549,0,410,21,5.7,5,steel,.45)
box('Sealed underside sculptural panel','body',843,0,424,65,10.4,3.0,panel,.4)

# Magazine stops at the raised rear polymer cheek, as in the viewed game image.
prof('Filled horizontal top magazine','magazine',[(465,308),(477,303),(731,303),(750,307),(750,332),(738,336),(474,335),(465,330)],17.8,magmat,.8)
box('Magazine bottom molding','magazine',607,0,335,273,18.6,4,panel,.5)
box('Magazine long top shoulder','magazine',607,0,304,246,16.2,3,magband,.5)
for side in [-1,1]:
    line('Magazine upper molded rim','magazine',[(478,side*8.9,309),(729,side*8.9,309),(743,side*8.9,314)],.25,magband)
    line('Magazine lower molded rim','magazine',[(478,side*8.9,330),(734,side*8.9,330)],.22,magband)
    # Subtle mold divisions, not visible ammunition or working internal detail.
    for px in [486,529,575,621,665,711]:box('Magazine faint transverse mold seam','magazine',px,side*8.94,320,1.6,.28,17,magband,.12)
    box('Magazine rear latch silhouette','magazine',743,side*9.1,319,10,1.0,26,metal,.45)
box('Magazine front closed shoe','magazine',472,0,320,17,18.5,28,panel,.75)
box('Magazine rear closed shoe','magazine',746,0,320,12,18.5,28,panel,.65)

# Open-sided structural optic frame. Its lower bridge meets both pedestals.
prof('Upper front frame pedestal','upper',[(421,296),(446,296),(454,311),(454,338),(471,344),(474,358),(431,359),(421,346)],13.3,metal,.7)
prof('Upper rear frame pedestal','upper',[(558,286),(588,283),(599,301),(605,321),(616,339),(611,346),(577,346),(572,329),(568,309)],13.3,metal,.7)
box('Upper frame joined lower bridge','upper',518,0,346,191,13.3,12,metal,.65)
for side in [-1,1]:
    prof('Front frame blind relief','upper',[(427,310),(440,310),(444,318),(444,334),(427,334)],.25,dark,.35,side*6.72)
    prof('Rear frame broad exterior facet','upper',[(574,293),(590,290),(595,304),(603,322),(609,334),(584,336)],.4,steel,.5,side*6.72)
    screw('Upper front frame screw','upper',438,346,side*7.0,.95)
    screw('Upper rear frame screw','upper',593,339,side*7.0,.95)
    box('Upper side edge detail','upper',517,side*7.0,349,135,.8,3.5,highlight,.14)
# Long low base sight integrated into the high frame, with solid lens discs.
prof('Integrated optic upper silhouette','sight',[(425,268),(447,263),(575,262),(591,266),(595,287),(572,295),(451,295),(425,290)],13.6,metal,.7)
box('Optic long shallow top rail','sight',514,0,262,147,11.5,4,steel,.35)
for i in range(18):box('Optic top rail decorative tooth','sight',447+i*7.8,0,259.3,4.3,12.8,3.5,steel,.14)
prof('Front optic sight post','sight',[(449,262),(451,250),(460,250),(463,262)],5.3,steel,.35)
prof('Rear optic sight post','sight',[(558,262),(560,251),(578,249),(585,254),(586,264)],5.3,steel,.35)
for side in [-1,1]:
    prof('Optic shallow long side inset','sight',[(445,273),(579,270),(584,283),(564,290),(447,290)],.3,panel,.45,side*6.85)
    line('Optic side molded edge','sight',[(449,side*7.02,277),(576,side*7.02,274)],.18,steel)
    screw('Optic front housing screw','sight',440,278,side*7.03,.82)
    screw('Optic rear housing screw','sight',579,280,side*7.03,.82)
for px in [425,594]:
    m.cyl('Optic closed end bezel','sight',P(px,0,282),2.9,.6,steel,'X',.18)
    m.cyl('Optic filled end face','sight',P(px+(-1 if px==425 else 1),0,282),2.15,.25,glass,'X',.08)

# Closed solid front and decorative shallow rings. There is no firing channel.
m.cyl('Short closed barrel-shaped ornament','barrel',P(417,0,348),2.3,40*S,steel,b=.22)
m.cyl('Front muzzle-shaped collar','barrel',P(404,0,348),2.8,16*S,metal,b=.3)
m.cyl('Solid front cap','barrel',P(395.5,0,348),2.45,.45,dark,b=.08)
m.cyl('Blind muzzle face disk','barrel',P(394.7,0,348),1.2,.10,steel,b=.03)
m.cyl('Front rear collar','barrel',P(429,0,348),2.9,6*S,steel,b=.2)

prof('Rear vertical rubber pad','butt',[(917,307),(931,310),(936,320),(935,418),(928,429),(914,429),(919,414),(922,325)],18.2,rubber,.9)
for i in range(16):box('Butt vertical grip rib','butt',933.4,0,325+i*5.8,3.0,16.1,2.1,panel,.15)
for side in [-1,1]:
    line('Rear rubber molded edge','butt',[(924,side*9.1,323),(925,side*9.1,414),(920,side*9.1,423)],.20,edge)
# Normalize the overall miniature length after the visual reference traced outline.
from mathutils import Vector
import bpy
bpy.context.view_layer.update()
pts=[o.matrix_world@Vector(v) for o in m.col.objects if o.type=='MESH' for v in o.bound_box]
span=max(v.x for v in pts)-min(v.x for v in pts)
for part in m.parts.values():part.scale.x=170/span
result=m.finish([
 'https://zilliongamer.com/delta-force/c/weapons/best-p90-build-delta-force',
 'https://zilliongamer.com/uploads/delta-force/weapons-builds/submachine-gun/p90/p90-delta-force-build.jpg',
 'https://deltaforcedb.com/weapon/p90'
],['The base-appearance game image was visually inspected in the browser, and the side silhouette was hand traced as an exterior sculpture.',
 'The dark shell, two ergonomic openings, top magazine ending at the raised rear cheek, high optic frame and short front follow that reference.',
 'The far side, underside, depth, material roughness and small hardware are artist interpretations; no claim of exact game-mesh fidelity.',
 'The magazine, receiver and front are filled; there are no working internal parts, firing passages or real component interfaces.',
 'No source game mesh, game textures or original logos are embedded. Model assets are shared noncommercially under CC BY-NC 4.0, as declared by the publisher.'],view=(-.25,-1,.27))
