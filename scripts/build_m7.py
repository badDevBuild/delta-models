"""Reference-derived, inert 300 mm display sculpture. Run using Blender MCP.

Only exterior art: filled body, blind decorative recesses, capped muzzle,
solid magazine, fixed trigger ornament, custom scale, no working internals.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector

# This generator only runs in a separate background process. Start a new file;
# the seed .blend on disk is never overwritten.
bpy.ops.wm.read_factory_settings(use_empty=True)
ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'assets/m7'
OUT = ASSET / 'source'
for folder in ['source','web','renders']:
    (ASSET/folder).mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
S = 300 / 1173
def X(px): return (px - 602.5) * S
def Z(py): return (300 - py) * S
def P(px, y, py): return (X(px), y, Z(py))

# Keep the opened source scene untouched; author in a separate scene.
scene = bpy.data.scenes.new('M7_DISPLAY_STUDIO')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = .001
scene.unit_settings.length_unit = 'MILLIMETERS'
scene['asset_purpose'] = 'INERT GAME DISPLAY SCULPTURE / NOT A WEAPON COMPONENT'
scene['reference_scope'] = 'User screenshots. Hidden surfaces are artist interpretations.'
scene['length_mm'] = 300
scene['version'] = '1.0.0'
col = bpy.data.collections.new('M7_EXTERIOR_COMPONENTS')
scene.collection.children.link(col)
parts = {}
def material(name, rgb, metallic, roughness):
    m=bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*rgb,1)
    p.inputs['Metallic'].default_value=metallic; p.inputs['Roughness'].default_value=roughness
    m.diffuse_color=(*rgb,1)
    return m
metal=material('Graphite anodized alloy',(.115,.123,.128),.72,.37)
edge=material('Machined bevels',(.20,.215,.22),.78,.32)
dark=material('Recess shadow',(.014,.019,.021),.26,.53)
polymer=material('Charcoal polymer',(.053,.061,.065),.08,.73)
rubber=material('Matte rubber',(.021,.026,.029),0,.86)
steel=material('Dark steel hardware',(.083,.098,.107),.82,.30)
glass=material('Optic blue glass',(.025,.25,.29),.35,.14)
red=material('Reticle red',(.65,.018,.006),.1,.28)
red.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(1,.025,.002,1)
red.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=2
orange=material('Inert prop muzzle marker',(.9,.22,.015),.08,.52)

def part(key,label):
    o=bpy.data.objects.new('part_'+key,None); col.objects.link(o)
    o['label']=label; o['inert_prop']=True; parts[key]=o; return o
for key,label in [('receiver','机匣外观'),('handguard','护木外壳'),('stock','镂空枪托'),('grip','后握把'),('magazine','实心弹匣外观'),('barrel_short','短款装饰前端'),('barrel_long','长款装饰前端'),('sights','机械瞄具'),('optic','红点瞄具外观'),('foregrip','前握把')]: part(key,label)

def attach(o,name,key,mat=metal):
    o.name=name
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o); o.parent=parts[key]
    o.data.materials.append(mat)
    return o
def active(o):
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
def bevel(o,width=.4,segments=3):
    if width>0:
        m=o.modifiers.new('Soft machined edges','BEVEL'); m.width=width; m.segments=segments
    m=o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL'); m.keep_sharp=True; m.weight=40
    return o
def box(name,key,loc,dim,mat=metal,b=.35):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=attach(bpy.context.object,name,key,mat); o.dimensions=dim
    active(o); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return bevel(o,b)
def poly(name,key,points,depth,mat=metal,b=.4,y=0):
    # Reference image side profile extruded across thickness.
    n=len(points); verts=[P(px,yy,py) for yy in [y-depth/2,y+depth/2] for px,py in points]
    faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new(name+'_mesh'); mesh.from_pydata(verts,[],faces); mesh.update()
    o=bpy.data.objects.new(name,mesh); col.objects.link(o); o.parent=parts[key]; o.data.materials.append(mat)
    # Ensure outward winding regardless of reference polygon orientation.
    import bmesh
    bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(mesh); bm.free()
    return bevel(o,b)
def cyl(name,key,loc,radius,depth,mat=steel,axis='X',b=.18,vertices=48):
    rot={'X':(0,math.pi/2,0),'Y':(math.pi/2,0,0),'Z':(0,0,0)}[axis]
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc,rotation=rot)
    o=attach(bpy.context.object,name,key,mat)
    active(o); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for f in o.data.polygons: f.use_smooth=len(f.vertices)==4
    return bevel(o,b)
def line(name,key,a,b,r,mat=metal):
    d=Vector(b)-Vector(a)
    o=cyl(name,key,(Vector(a)+Vector(b))/2,r,d.length,mat,'Z',r*.2,24)
    o.rotation_mode='QUATERNION';o.rotation_quaternion=d.to_track_quat('Z','Y');return o
def cut(obj,cutter):
    active(cutter)
    for m in list(cutter.modifiers):
        if m.type=='BEVEL': bpy.ops.object.modifier_apply(modifier=m.name)
        else: cutter.modifiers.remove(m)
    active(obj); m=obj.modifiers.new('Blind exterior pocket','BOOLEAN');m.object=cutter;m.operation='DIFFERENCE';m.solver='EXACT'
    # Evaluate pocket before final edge treatment.
    bpy.ops.object.modifier_move_up(modifier=m.name)
    bpy.ops.object.modifier_move_up(modifier=m.name)
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter,do_unlink=True)
def screw(name,key,px,py,y,r=1.45):
    sign=1 if y>0 else -1
    cyl(name+' seat',key,P(px,y,py),r+.4,.35,dark,'Y',.08)
    cyl(name+' head',key,P(px,y+sign*.22,py),r,.65,steel,'Y',.08,24)
    cyl(name+' hex recess',key,P(px,y+sign*.6,py),r*.40,.12,dark,'Y',.03,6)

# Main long faceted guard. Blind openings never create a bore or usable part.
guard=poly('Faceted handguard body','handguard',[(105,187),(112,172),(354,171),(360,182),(554,182),(560,194),(550,239),(552,278),(483,278),(459,267),(111,267),(106,253)],16.8,metal,.65)
for sign in [-1,1]:
    # Tapered large pockets and rows of rounded decorative vents.
    pockets=[[(120,190),(160,190),(157,211),(126,211)],[(174,189),(207,190),(220,208),(165,208)]]
    for i,points in enumerate(pockets):
        cutter=poly('temporary pocket','handguard',points,3.4,dark,.45,y=sign*8.9);cut(guard,cutter)
    for i,(a,b) in enumerate([(162,233),(283,387),(409,483)]):
        c=box('temporary slot','handguard',P((a+b)/2,sign*8.9,230),((b-a)*S,3.4,12*S),dark,.8);cut(guard,c)
    for i in range(3):
        a=225+i*29
        c=poly('temporary slant slot','handguard',[(a,199),(a+18,199),(a+24,209),(a+6,209)],3.3,dark,.35,y=sign*8.9);cut(guard,c)
    for i in range(4):
        a=158+i*39
        c=poly('temporary lower vent','handguard',[(a,254),(a+23,254),(a+14,263),(a-8,263)],3.1,dark,.28,y=sign*8.8);cut(guard,c)
    for i in range(3):
        a=478+i*20
        c=poly('temporary rear vent','handguard',[(a,250),(a+8,249),(a+26,273),(a+18,273)],3.1,dark,.25,y=sign*8.8);cut(guard,c)
    for px,py,r in [(131,230,1.25),(256,229,1.35),(502,231,2.05)]: screw('Guard screw', 'handguard',px,py,sign*8.5,r)
    poly('Guard shoulder chamfer','handguard',[(111,174),(354,174),(360,182),(551,183),(550,191),(112,189)],.32,edge,.1,y=sign*8.4)
    for a in [362,389,417,444]:
        poly('Upper shoulder slot','handguard',[(a,183),(a+18,183),(a+22,188),(a+4,188)],.30,dark,.16,y=sign*8.62)
    for a in [480,515]: box('Rear shoulder slot','handguard',P(a,sign*8.6,205),(7.8,.3,1.65),dark,.5)

receiver=poly('Upper receiver sculpted shell','receiver',[(555,183),(897,177),(923,184),(937,207),(960,220),(961,266),(938,286),(900,304),(865,308),(809,291),(595,285),(554,274)],17.4,metal,.75)
lower=poly('Lower receiver solid sculpture','receiver',[(593,267),(728,275),(786,289),(847,288),(854,306),(817,323),(727,315),(727,359),(590,330)],16.4,metal,.55)
for sign in [-1,1]:
    poly('Long receiver bevel','receiver',[(573,182),(893,182),(914,202),(563,202)],.45,edge,.28,y=sign*8.64)
    poly('Receiver lower contour','receiver',[(569,242),(925,242),(919,257),(874,280),(603,277),(569,267)],.65,steel,.5,y=sign*8.8)
    box('Horizontal receiver recess','receiver',P(762,sign*8.9,225),(86,.35,2.5),dark,.65)
    box('Upper trim strip','receiver',P(762,sign*9.1,219),(84,.55,.8),edge,.18)
    # Closed shallow side panel, never an open ejection/internal chamber.
    box('Sealed receiver side panel','receiver',P(658,sign*9.1,209),(29,1.3,5.3),steel,1.2)
    box('Side panel inset','receiver',P(658,sign*9.85,209),(22,.2,2.6),dark,.5)
    for a in [611,709]: screw('Side panel fastener','receiver',a,209,sign*10,1.2)
    for px,py,r in [(559,256,1.4),(579,276,1.4),(861,276,1.7),(929,272,2.9),(790,301,.75)]: screw('Receiver hardware','receiver',px,py,sign*9,r)
    poly('Magazine well seam','receiver',[(591,323),(722,356),(722,364),(590,332)],.45,edge,.2,y=sign*8.1)
    # Fixed cosmetic controls; no moving action or working mechanism.
    box('Fixed decorative paddle','receiver',P(730,sign*10.5,292),(3.5,2.2,9),steel,.55)
    cyl('Paddle cap','receiver',P(730,sign*11,255),1.9,1.1,polymer,'Y',.15)
    box('Paddle stem','receiver',P(730,sign*10.5,274),(1.2,1.2,6.4),steel,.2)
    screw('Decorative selector center','receiver',830,294,sign*10,1.85)
    box('Fixed selector ornament','receiver',P(815,sign*11.1,296),(5.8,1.6,1.85),polymer,.35)
    box('Receiver catch detail','receiver',P(696,sign*10,299),(6.6,1.8,3.3),steel,.6)
    for k in range(3): box('Catch grip rib','receiver',P(688+k*5,sign*11,299),(.5,.35,2.2),edge,.1)
guard2=poly('Trigger guard outer sculpture','receiver',[(724,316),(805,319),(818,341),(805,367),(768,380),(725,365)],9.2,metal,.8)
c=poly('Temporary guard opening','receiver',[(737,325),(796,327),(805,342),(796,359),(769,370),(737,360)],22,dark,.8);cut(guard2,c)
poly('Fixed trigger silhouette','receiver',[(769,319),(779,320),(786,336),(784,351),(773,358),(777,347),(777,337)],3.2,steel,.35)

# Solid magazine silhouette, curved lower edge and shallow panel reliefs.
mag=poly('Solid display magazine','magazine',[(598,336),(716,364),(719,477),(723,490),(712,495),(597,495),(594,486),(598,437)],15.5,polymer,.8)
poly('Magazine base shoe','magazine',[(595,477),(722,477),(724,491),(718,497),(595,497)],17.2,rubber,.65)
for sign in [-1,1]:
    poly('Magazine inset panel','magazine',[(607,375),(705,391),(707,476),(604,476)],.4,metal,.3,y=sign*7.8)
    for py in [381,418,459]:
        poly('Magazine horizontal reinforcement','magazine',[(601,py),(715,py+13),(715,py+18),(601,py+5)],.9,polymer,.2,y=sign*8.0)
    for a in [634,674]:
        poly('Magazine long emboss','magazine',[(a,384),(a+3,384),(a+3,472),(a,472)],.8,polymer,.2,y=sign*8.1)
    box('Magazine base seam','magazine',P(657,sign*8.7,485),(29,.4,.65),edge,.1)

# Rear angled ergonomic grip, two broad slightly raised rubber panels.
poly('Ergonomic grip solid','grip',[(812,324),(844,316),(867,334),(878,365),(891,392),(927,451),(926,470),(853,470),(847,451),(844,431),(816,366)],15.6,polymer,1.3)
for sign in [-1,1]:
    poly('Grip palm inlay','grip',[(820,354),(850,350),(864,370),(871,397),(904,452),(884,460),(859,451),(850,419),(829,383)],.65,rubber,.6,y=sign*7.8)
    poly('Grip upper highlight','grip',[(817,342),(848,337),(866,359),(858,365),(832,354),(820,358)],.6,metal,.4,y=sign*7.9)
    for i in range(17):
        py=380+i*4;px=843+(py-380)*.42
        line('Grip stipple groove','grip',P(px,sign*8.28,py),P(px+22,sign*8.28,py+1),.16,polymer)
poly('Grip heel','grip',[(851,462),(926,462),(926,472),(853,472)],16.2,rubber,.45)

# Stock: central hinge sculpture, cheek rest, triangular open frame, ribbed pad.
poly('Stock hinge block','stock',[(963,203),(986,198),(1011,208),(1012,294),(972,300),(964,287)],16.7,steel,.65)
cyl('Stock hinge external pin','stock',P(998,0,243),4.4,24,steel,'Z',.45)
for py in [206,287]: cyl('Hinge collar','stock',P(998,0,py),5.0,2.0,polymer,'Z',.35)
cheek=cyl('Stock cheek tube sculpture','stock',P(1090,0,220),8.25,47,polymer,'X',1.4)
poly('Stock upper cheek contour','stock',[(1012,192),(1166,192),(1181,202),(1174,252),(1048,247),(1011,236)],15.8,polymer,1.5)
poly('Stock open frame lower bar','stock',[(977,282),(1068,282),(1135,365),(1126,380),(1060,304),(977,304)],8.5,polymer,.7)
poly('Stock rear sloped butt','stock',[(1165,188),(1188,195),(1174,306),(1138,379),(1124,378),(1144,302)],15.5,rubber,1.1)
poly('Stock inner spine','stock',[(1160,246),(1169,252),(1151,312),(1131,351),(1121,340),(1141,299)],9.0,metal,.7)
for py,a,b in [(276,1040,1158),(305,1075,1147),(333,1100,1133)]:
    box('Stock bridge rib','stock',P((a+b)/2,0,py),((b-a)*S,7.5,1.3),metal,.3)
for sign in [-1,1]:
    poly('Stock diagonal molded panel','stock',[(1022,253),(1050,256),(1070,281),(1034,280)],.5,rubber,.4,y=sign*7.4)
    screw('Stock sling recess ornament','stock',1118,303,sign*5.0,2.5)
    for k in range(7):
        a=1030+k*5
        line('Stock cheek grooves','stock',P(a,sign*7.9,254),P(a+10,sign*7.9,278),.17,metal)
for k in range(12):
    py=209+k*12; px=1181-(py-209)*.23
    box('Buttpad transverse rib','stock',P(px,0,py),(1.0,16,1.0),polymer,.2)

# Top rail is decorative, deliberately scaled and non-standard.
for key,a,b in [('handguard',113,550),('receiver',558,927)]:
    box('Decorative rail base',key,P((a+b)/2,0,170),((b-a)*S,8.3,1.8),steel,.28)
    for i,px in enumerate(range(a+5,b,18)):
        box('Decorative transverse rail tooth',key,P(px,0,165),(2.8,10.2,1.35),metal,.24)
        box('Rail tooth top wear',key,P(px,0,162.7),(2.2,8.5,.17),edge,.08)

# Capped short / long display cylinders; orange end explicitly marks an inert prop.
for key,start in [('barrel_short',16),('barrel_long',-84)]:
    end=106
    cyl('Solid capped display rod',key,P((start+end)/2,0,231),3.1,(end-start)*S,steel,'X',.25)
    cyl('Front cap collar',key,P(start+5,0,231),3.7,10*S,metal,'X',.25)
    cyl('Closed muzzle face',key,P(start+.6,0,231),3.35,.50,dark,'X',.1)
    cyl('Orange inert marker',key,P(start+1.5,0,231),3.78,1.0,orange,'X',.12)
    # Concentric face disc is closed; there is no hole through this asset.
    cyl('Blind end disc',key,P(start-.1,0,231),1.45,.15,steel,'X',.06)
    for k in range(4): cyl('Front ring detail',key,P(start+9+k*2.6,0,231),3.3,.35,edge,'X',.05)

# Fixed iron sights. Sight aperture is a nonfunctional sculptural opening.
for px in [130,842]:
    box('Sight foot','sights',P(px,0,163),(10,13,2.4),steel,.5)
    screw('Sight base screw','sights',px,161,-7,1.4)
    poly('Sight pedestal','sights',[(px-9,157),(px-7,138),(px-3,128),(px+4,128),(px+9,155)],5.5,steel,.45)
    # Ring in the side view makes the raised sight recognisable.
    ring=cyl('Sight aperture rim','sights',P(px,0,124),3.5,3.1,steel,'Y',.28) if px==130 else box('Rear sight rounded rectangular hood','sights',P(px,0,129),(4.8,4.2,8.2),steel,.85)
    hole=cyl('temporary aperture','sights',P(px,0,124 if px==130 else 125),1.65 if px==130 else 1.15,7,dark,'Y',.15);cut(ring,hole)
    box('Sight fixed center post','sights',P(px,0,137),(1.0,2.6,4.0),steel,.2)

# Alternate accessory package from reference 02.
box('Optic base clamp','optic',P(722,0,155),(22,14,3),steel,.55)
box('Optic riser','optic',P(722,0,147),(13,10,2.4),metal,.45)
for sign in [-1,1]:
    poly('Optic hood side','optic',[(682,144),(685,102),(695,92),(730,91),(746,100),(751,142)],2.2,metal,.65,y=sign*6.1)
    screw('Optic side fastener','optic',718,136,sign*7.5,1.4)
box('Optic hood bridge','optic',P(715,0,95),(13.3,13.2,2.4),metal,.6)
box('Optic closed glass','optic',P(690,0,120),(1.0,10.4,9.3),glass,.55)
cyl('Optic adjustment turret','optic',P(735,0,137),3.1,4.0,steel,'Z',.25)
cyl('Optic adjustment knob','optic',P(735,0,127),3.5,1.4,polymer,'Z',.2)
box('Optic rear red dot','optic',P(737,0,118),(.7,.65,.65),red,.2)
box('Foregrip mounting ornament','foregrip',P(311,0,273),(14,12,3),steel,.55)
poly('Foregrip angled neck','foregrip',[(296,277),(322,277),(329,300),(321,312),(296,307),(287,292)],11.5,polymer,.9)
cyl('Foregrip body','foregrip',P(309,0,336),6.0,21.8,polymer,'Z',1.0)
for py in [308,321,336,351,364]: cyl('Foregrip palm ring','foregrip',P(309,0,py),6.35,1.25,rubber,'Z',.35)
cyl('Foregrip heel','foregrip',P(309,0,379),5.8,2,steel,'Z',.4)

# Explicit custom print trim bounds. Adjacent exterior pieces meet on flat glue faces.
parts['handguard']['print_bounds_mm']=[X(105),-30,-60,X(555),30,60]
parts['receiver']['print_bounds_mm']=[X(555),-30,Z(382),X(968),30,60]
parts['stock']['print_bounds_mm']=[X(968),-30,-60,X(1189),30,60]
parts['magazine']['print_bounds_mm']=[-180,-30,-60,180,30,Z(350)]
parts['grip']['print_bounds_mm']=[-180,-30,-60,180,30,Z(332)]
for k in ['barrel_short','barrel_long']:
    parts[k]['print_split']=False
    parts[k]['print_bounds_mm']=[-180,-30,-60,X(105),30,60]
parts['optic']['print_split']=False
parts['foregrip']['print_split']=False

# Save all variants; userData identifies default visibility in the viewer.
for k,o in parts.items():
    o['default_visible']=k not in ['barrel_long','optic','foregrip']
    o['variant']='accessory' if k in ['barrel_long','optic','foregrip'] else 'base'

bpy.context.view_layer.update()
manifest={'id':'m7','name':'M7','display_length_mm':300,'source_urls':[], 'approximation':'User reference 01 base / reference 02 optional accessories. Unseen surfaces interpreted. Inert exterior only.', 'version':'1.1.0','kind':'nonfunctional_reference_sculpture','base_length_mm':300,'units':'mm','parts':[]}
for k,o in parts.items():
    children=[c for c in o.children_recursive if c.type=='MESH']
    coords=[c.matrix_world@Vector(v) for c in children for v in c.bound_box]
    lo=[min(v[i] for v in coords) for i in range(3)]; hi=[max(v[i] for v in coords) for i in range(3)]
    manifest['parts'].append({'id':o.name,'label':o['label'],'meshes':len(children),'bounds_mm':[lo,hi],'default_visible':o['default_visible']})
(ASSET/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

# Studio, separate from the export selection.
world=bpy.data.worlds.new('Cool charcoal studio');world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.075,.085,.10,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.45;scene.world=world
def area(name,loc,power,size,color):
    dat=bpy.data.lights.new(name,'AREA');dat.energy=power;dat.shape='DISK';dat.size=size;dat.color=color
    o=bpy.data.objects.new(name,dat);scene.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector((0,0,5))-o.location).to_track_quat('-Z','Y').to_euler()
area('Softbox key',(-60,-170,230),1250000,250,(.80,.90,1))
area('Warm fill',(120,-60,80),580000,140,(1,.78,.55))
area('Long rim',(-50,160,100),1650000,180,(.60,.77,1))
camdat=bpy.data.cameras.new('Studio camera');cam=bpy.data.objects.new('Studio camera',camdat);scene.collection.objects.link(cam)
cam.location=(-145,-480,170);target=Vector((0,0,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camdat.type='ORTHO';camdat.ortho_scale=365;camdat.clip_end=5000;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.render.resolution_x=1800;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.render.filepath=str(ASSET/'renders/studio.png')

bpy.ops.object.select_all(action='DESELECT')
for o in list(col.all_objects):o.select_set(True)
bpy.context.view_layer.update()
bpy.ops.export_scene.gltf(filepath=str(ASSET/'web/m7.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_extras=True,export_yup=True,export_animations=False)
for k in ['barrel_long','optic','foregrip']:
    for o in parts[k].children_recursive:o.hide_render=True;o.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'m7.blend'))
bpy.ops.render.render(write_still=True)
cam.location=(0,-520,0)
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath=str(ASSET/'renders/side.png')
bpy.ops.render.render(write_still=True)
result={'blend':str(OUT/'m7.blend'),'glb':str(ASSET/'web/m7.glb'),'preview':str(ASSET/'renders/studio.png'),'parts':len(parts),'mesh_count':sum(1 for o in col.objects if o.type=='MESH')}
