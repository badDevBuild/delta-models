"""Exterior sculpture helpers. Dimensions are arbitrary miniature millimetres.

No internal mechanisms, mounting specifications, chambers or through bores.
The authored meshes are independent visual reconstructions from game pictures.
"""
import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]

class Sculpture:
    def __init__(self, asset, length):
        # CLI invocation opens a seed only to initialize Blender. Reset the in-memory
        # copy so other scenes cannot cause part IDs to acquire numeric suffixes.
        # The seed file is never overwritten.
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.asset=asset; self.length=length; self.parts={}
        self.out=ROOT/'assets'/asset
        for p in ['source','web','renders']: (self.out/p).mkdir(parents=True,exist_ok=True)
        self.scene=bpy.data.scenes.new(asset.upper()+'_EXTERIOR_STUDIO')
        bpy.context.window.scene=self.scene
        self.scene.unit_settings.system='METRIC'
        self.scene.unit_settings.scale_length=.001
        self.scene.unit_settings.length_unit='MILLIMETERS'
        self.scene['asset_purpose']='Solid miniature exterior sculpture; no functional internals or usable interfaces'
        self.col=bpy.data.collections.new(asset.upper()+'_EXTERIOR');self.scene.collection.children.link(self.col)
        self.metal=self.mat('Graphite alloy',(.085,.099,.108),.72,.36)
        self.edge=self.mat('Soft metallic edges',(.19,.215,.225),.73,.34)
        self.dark=self.mat('Blind recess shadow',(.014,.020,.022),.25,.65)
        self.polymer=self.mat('Charcoal polymer',(.04,.047,.05),.05,.64)
        self.rubber=self.mat('Matte rubber',(.015,.020,.022),0,.88)
        self.steel=self.mat('Satin steel',(.23,.26,.27),.8,.4)
        self.glass=self.mat('Opaque blue-green optic',(.018,.105,.12),.62,.16)
    def mat(self,name,rgb,metal=0,rough=.5):
        m=bpy.data.materials.new(self.asset+' / '+name);m.use_nodes=True
        p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb,1)
        p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
        m.diffuse_color=(*rgb,1);return m
    def part(self,key,label,visible=True):
        o=bpy.data.objects.new('part_'+key,None);self.col.objects.link(o)
        o['label']=label;o['default_visible']=visible;o['variant']='base' if visible else 'accessory'
        o['inert_prop']=True;self.parts[key]=o;return o
    def active(self,o):
        bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    def attach(self,o,name,key,mat):
        o.name=name
        for c in list(o.users_collection):c.objects.unlink(o)
        self.col.objects.link(o);o.parent=self.parts[key];o.data.materials.append(mat or self.metal)
        return o
    def bevel(self,o,b=.4,n=3):
        if b:
            m=o.modifiers.new('Rounded sculpture edges','BEVEL');m.width=b;m.segments=n
        m=o.modifiers.new('Weighted exterior normals','WEIGHTED_NORMAL');m.keep_sharp=True
        return o
    def box(self,name,key,loc,dim,mat=None,b=.4):
        bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=self.attach(bpy.context.object,name,key,mat)
        o.dimensions=dim;self.active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        return self.bevel(o,b)
    def poly(self,name,key,pts,depth,mat=None,b=.4,y=0):
        n=len(pts);verts=[(x,yy,z) for yy in [y-depth/2,y+depth/2] for x,z in pts]
        faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(mesh);bm.free()
        o=bpy.data.objects.new(name,mesh);self.col.objects.link(o);o.parent=self.parts[key];o.data.materials.append(mat or self.metal)
        return self.bevel(o,b)
    def cyl(self,name,key,loc,r,depth,mat=None,axis='X',b=.12,vertices=48):
        rot={'X':(0,math.pi/2,0),'Y':(math.pi/2,0,0),'Z':(0,0,0)}[axis]
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc,rotation=rot)
        o=self.attach(bpy.context.object,name,key,mat);self.active(o)
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
        return self.bevel(o,b)
    def cone(self,name,key,loc,r1,r2,depth,mat=None,axis='X',b=.15):
        rot={'X':(0,math.pi/2,0),'Y':(math.pi/2,0,0),'Z':(0,0,0)}[axis]
        bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=r1,radius2=r2,depth=depth,location=loc,rotation=rot)
        o=self.attach(bpy.context.object,name,key,mat)
        for f in o.data.polygons:f.use_smooth=len(f.vertices)==4
        return self.bevel(o,b)
    def line(self,name,key,a,b,r,mat=None):
        d=Vector(b)-Vector(a);o=self.cyl(name,key,(Vector(a)+Vector(b))/2,r,d.length,mat,'Z',r*.22,16)
        o.rotation_mode='QUATERNION';o.rotation_quaternion=d.to_track_quat('Z','Y');return o
    def cut(self,obj,cutter):
        self.active(cutter)
        for m in list(cutter.modifiers):
            if m.type=='BEVEL':bpy.ops.object.modifier_apply(modifier=m.name)
            else:cutter.modifiers.remove(m)
        self.active(obj);m=obj.modifiers.new('Exterior silhouette recess','BOOLEAN');m.object=cutter;m.operation='DIFFERENCE';m.solver='EXACT'
        while list(obj.modifiers).index(m)>0:bpy.ops.object.modifier_move_up(modifier=m.name)
        bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(cutter,do_unlink=True)
    def screw(self,name,key,x,z,y,r=1):
        s=1 if y>0 else -1
        self.cyl(name+' seat',key,(x,y,z),r+.24,.28,self.dark,'Y',.05,32)
        self.cyl(name+' head',key,(x,y+s*.23,z),r,.42,self.steel,'Y',.07,32)
        self.cyl(name+' blind hex',key,(x,y+s*.46,z),r*.4,.1,self.dark,'Y',.01,6)
    def rail(self,key,a,b,z,width=5,pitch=4):
        self.box('Non-standard display rail base',key,((a+b)/2,0,z),(b-a,width,1.35),self.metal,.2)
        for i in range(int((b-a)/pitch)):
            self.box('Display rail transverse ridge',key,(a+pitch/2+i*pitch,0,z+1),(pitch*.61,width+1.4,1.5),self.metal,.2)
    def finish(self,sources,approximation):
        scene=self.scene;bpy.context.view_layer.update()
        manifest={'id':self.asset,'version':'1.0.0','kind':'nonfunctional_reference_sculpture','units':'mm','display_length_mm':self.length,'source_urls':sources,'approximation':approximation,'rights_status':'publisher_declared_cc_by_nc_4_0','parts':[]}
        base_coords=[]
        for key,p in self.parts.items():
            kids=[c for c in p.children_recursive if c.type=='MESH'];coords=[c.matrix_world@Vector(v) for c in kids for v in c.bound_box]
            lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
            manifest['parts'].append({'id':p.name,'label':p['label'],'variant':p['variant'],'default_visible':p['default_visible'],'meshes':len(kids),'bounds_mm':[lo,hi]})
            if p['default_visible']:base_coords+=coords
        lo=[min(v[i] for v in base_coords) for i in range(3)];hi=[max(v[i] for v in base_coords) for i in range(3)]
        manifest['bounds_mm']=[lo,hi];manifest['display_length_mm']=round(hi[0]-lo[0],3)
        manifest['mesh_count']=sum(p['meshes'] for p in manifest['parts'])
        (self.out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
        world=bpy.data.worlds.new(self.asset+' dark studio');world.use_nodes=True
        world.node_tree.nodes['Background'].inputs[0].default_value=(.055,.071,.081,1)
        world.node_tree.nodes['Background'].inputs[1].default_value=.48;scene.world=world
        focus=Vector(((lo[0]+hi[0])/2,0,(lo[2]+hi[2])/2))
        L=self.length
        def area(name,pos,power,size,color):
            d=bpy.data.lights.new(name,'AREA');d.energy=power*(L/300)**2;d.shape='DISK';d.size=size*L/300;d.color=color
            o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=Vector(pos)*L/300+focus
            o.rotation_euler=(focus-o.location).to_track_quat('-Z','Y').to_euler()
        area('Large cool softbox',(-70,-180,210),1400000,230,(.8,.9,1))
        area('Warm near fill',(90,-50,75),480000,150,(1,.86,.69))
        area('Long blue rim',(-40,145,90),1750000,220,(.64,.8,1))
        dat=bpy.data.cameras.new('Studio camera');cam=bpy.data.objects.new('Studio camera',dat);scene.collection.objects.link(cam);scene.camera=cam
        dat.type='ORTHO';dat.ortho_scale=max(L*1.16,(hi[2]-lo[2])*2.6);dat.clip_end=5000
        cam.location=focus+Vector((-L*.18,-L*1.8,L*.47));cam.rotation_euler=(focus-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True
        scene.render.resolution_x=1800;scene.render.resolution_y=900;scene.render.resolution_percentage=100
        scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='AgX'
        for p in self.parts.values():
            if not p['default_visible']:
                for c in p.children_recursive:c.hide_render=True
        bpy.ops.wm.save_as_mainfile(filepath=str(self.out/'source'/f'{self.asset}.blend'))
        scene.render.filepath=str(self.out/'renders'/'studio.png');bpy.ops.render.render(write_still=True)
        cam.location=focus+Vector((0,-L*2,0));cam.rotation_euler=(focus-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(self.out/'renders'/'side.png');bpy.ops.render.render(write_still=True)
        # Merge evaluated visual surfaces per exterior part only for the web export.
        # The saved Blender master retains individually editable detail objects.
        for p in self.parts.values():
            kids=[c for c in p.children_recursive if c.type=='MESH']
            for c in kids:
                c.hide_set(False);c.hide_render=False;self.active(c)
                bpy.ops.object.convert(target='MESH')
            bpy.ops.object.select_all(action='DESELECT')
            for c in kids:c.select_set(True)
            bpy.context.view_layer.objects.active=kids[0];bpy.ops.object.join();kids[0].name=p.name+'_surfaces'
        bpy.ops.object.select_all(action='DESELECT')
        for o in self.col.all_objects:o.select_set(True)
        bpy.ops.export_scene.gltf(filepath=str(self.out/'web'/f'{self.asset}.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_extras=True,export_yup=True,export_animations=False)
        return {'id':self.asset,'blend':str(self.out/'source'/f'{self.asset}.blend'),'glb':str(self.out/'web'/f'{self.asset}.glb'),'manifest':str(self.out/'manifest.json'),'parts':len(self.parts),'meshes':manifest['mesh_count'],'bounds_mm':manifest['bounds_mm']}
