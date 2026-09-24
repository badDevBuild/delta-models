"""Shared authoring helpers for AKM/P90 miniature exterior sculptures.

All coordinates are arbitrary millimetres at display scale. No functional
internals, real interfaces or original game assets are included.
"""
import bpy, bmesh, math, json, hashlib
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]

class Model:
    def __init__(self, asset_id, title, length):
        self.asset_id, self.title, self.length = asset_id, title, length
        self.root = ROOT/'assets'/asset_id
        for d in ['source','web','renders']: (self.root/d).mkdir(parents=True,exist_ok=True)
        self.scene=bpy.data.scenes.new(asset_id.upper()+'_DISPLAY_STUDIO')
        bpy.context.window.scene=self.scene
        # This background process is writing a new asset, never its input file.
        for s in list(bpy.data.scenes):
            if s != self.scene: bpy.data.scenes.remove(s)
        for obj in list(bpy.data.objects): bpy.data.objects.remove(obj,do_unlink=True)
        for col in list(bpy.data.collections):
            if col.users==0: bpy.data.collections.remove(col)
        self.scene.unit_settings.system='METRIC'
        self.scene.unit_settings.scale_length=.001
        self.scene.unit_settings.length_unit='MILLIMETERS'
        self.scene['asset_purpose']='INERT MINIATURE EXTERIOR SCULPTURE'
        self.scene['no_functional_geometry']=True
        self.col=bpy.data.collections.new(asset_id.upper()+'_EXTERIOR_COMPONENTS')
        self.scene.collection.children.link(self.col)
        self.parts={}
    def mat(self,name,color,metal=0,rough=.5):
        m=bpy.data.materials.new(name); m.use_nodes=True
        p=m.node_tree.nodes.get('Principled BSDF')
        p.inputs['Base Color'].default_value=(*color,1)
        p.inputs['Metallic'].default_value=metal
        p.inputs['Roughness'].default_value=rough
        m.diffuse_color=(*color,1)
        return m
    def part(self,key,label,default=True,variant='base'):
        o=bpy.data.objects.new('part_'+key,None);self.col.objects.link(o)
        o['label']=label;o['default_visible']=default;o['variant']=variant
        o['inert_prop']=True;o['print_split']=True
        self.parts[key]=o;return o
    def attach(self,o,name,key,mat):
        o.name=name
        for col in list(o.users_collection): col.objects.unlink(o)
        self.col.objects.link(o);o.parent=self.parts[key]
        o.data.materials.clear();o.data.materials.append(mat)
        return o
    @staticmethod
    def active(o):
        bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
        bpy.context.view_layer.objects.active=o
    def bevel(self,o,b=.4,segments=3):
        if b:
            m=o.modifiers.new('Rounded miniature edges','BEVEL');m.width=b;m.segments=segments
        m=o.modifiers.new('Area weighted normals','WEIGHTED_NORMAL');m.keep_sharp=True
        return o
    def box(self,name,key,loc,dim,mat,b=.4):
        bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
        o=self.attach(bpy.context.object,name,key,mat);o.dimensions=dim
        self.active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        return self.bevel(o,b)
    def poly(self,name,key,points,depth,mat,b=.4,y=0):
        n=len(points);verts=[(x,yy,z) for yy in [y-depth/2,y+depth/2] for x,z in points]
        faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
        faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        mesh=bpy.data.meshes.new(name+'_mesh');mesh.from_pydata(verts,[],faces);mesh.update()
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(mesh);bm.free()
        o=bpy.data.objects.new(name,mesh);self.col.objects.link(o);o.parent=self.parts[key]
        o.data.materials.append(mat);return self.bevel(o,b)
    def cyl(self,name,key,loc,r,depth,mat,axis='X',b=.15,vertices=48):
        rot={'X':(0,math.pi/2,0),'Y':(math.pi/2,0,0),'Z':(0,0,0)}[axis]
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc,rotation=rot)
        o=self.attach(bpy.context.object,name,key,mat)
        self.active(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        for f in o.data.polygons: f.use_smooth=len(f.vertices)==4
        return self.bevel(o,b)
    def rod(self,name,key,a,b,r,mat):
        d=Vector(b)-Vector(a)
        o=self.cyl(name,key,(Vector(a)+Vector(b))/2,r,d.length,mat,'Z',r*.15,24)
        o.rotation_mode='QUATERNION';o.rotation_quaternion=d.to_track_quat('Z','Y');return o
    def path(self,name,key,points,r,mat):
        cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1
        cu.bevel_depth=r;cu.bevel_resolution=2;cu.resolution_u=12;cu.use_fill_caps=True
        spline=cu.splines.new('POLY');spline.points.add(len(points)-1)
        for p,co in zip(spline.points,points):p.co=(*co,1)
        o=bpy.data.objects.new(name,cu);self.col.objects.link(o);o.parent=self.parts[key];cu.materials.append(mat)
        self.active(o);bpy.ops.object.convert(target='MESH')
        return bpy.context.object
    def cut(self,o,c):
        self.active(c)
        for mod in list(c.modifiers):
            if mod.type=='BEVEL':bpy.ops.object.modifier_apply(modifier=mod.name)
            else:c.modifiers.remove(mod)
        self.active(o)
        mod=o.modifiers.new('Sculpted surface opening','BOOLEAN');mod.object=c;mod.operation='DIFFERENCE';mod.solver='EXACT'
        while list(o.modifiers).index(mod)>0:bpy.ops.object.modifier_move_up(modifier=mod.name)
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(c,do_unlink=True)
    def screw(self,name,key,x,z,y,r,mat,dark):
        sign=1 if y>0 else -1
        self.cyl(name+' rim',key,(x,y,z),r,.6,mat,'Y',.08,32)
        self.cyl(name+' blind center',key,(x,y+sign*.32,z),r*.35,.08,dark,'Y',.02,6)
    def finish(self,sources,approximation,view=(.34,-1,.28),license_status='publisher_declared_cc_by_nc_4_0'):
        bpy.context.view_layer.update()
        manifest={'schema':'delta-six-asset/v1','id':self.asset_id,'name':self.title,'version':'1.0.0',
            'kind':'nonfunctional_reference_sculpture','units':'mm','display_length_mm':self.length,
            'source_urls':sources,'approximation':approximation,'license_status':license_status,
            'physical_print_tested':False,'parts':[]}
        allcoords=[]
        for key,p in self.parts.items():
            children=[c for c in p.children_recursive if c.type=='MESH']
            coords=[c.matrix_world@Vector(v) for c in children for v in c.bound_box]
            lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
            if p['default_visible']:allcoords+=coords
            manifest['parts'].append({'id':p.name,'key':key,'label':p['label'],'meshes':len(children),
                'bounds_mm':[lo,hi],'default_visible':p['default_visible'],'variant':p['variant']})
        lo=[min(v[i] for v in allcoords) for i in range(3)];hi=[max(v[i] for v in allcoords) for i in range(3)]
        manifest['bounds_mm']=[lo,hi];manifest['measured_length_mm']=hi[0]-lo[0]
        manifest['mesh_count']=sum(p['meshes'] for p in manifest['parts'])
        self.active(next(o for o in self.col.objects if o.type=='MESH'))
        bpy.ops.object.select_all(action='DESELECT')
        for o in self.col.objects:o.select_set(True)
        glb=self.root/'web'/f'{self.asset_id}.glb'
        bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,use_active_scene=True,
            export_apply=True,export_extras=True,export_yup=True,export_animations=False)
        manifest['glb_bytes']=glb.stat().st_size
        manifest['glb_sha256']=hashlib.sha256(glb.read_bytes()).hexdigest()
        # Lighting lives outside the model collection and is not exported.
        world=bpy.data.worlds.new(self.asset_id+' studio');world.use_nodes=True
        world.node_tree.nodes['Background'].inputs[0].default_value=(.045,.057,.073,1)
        world.node_tree.nodes['Background'].inputs[1].default_value=.55;self.scene.world=world
        center=Vector(((lo[0]+hi[0])/2,0,(lo[2]+hi[2])/2))
        def area(name,loc,power,size,color):
            d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color
            o=bpy.data.objects.new(name,d);self.scene.collection.objects.link(o);o.location=loc
            o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
        area('Large cool key',(-70,-150,230),1200000,200,(.77,.87,1))
        area('Warm edge fill',(140,-50,70),650000,150,(1,.77,.5))
        area('Long blue rim',(-50,180,150),1800000,230,(.64,.80,1))
        d=bpy.data.cameras.new('Display camera');cam=bpy.data.objects.new('Display camera',d);self.scene.collection.objects.link(cam)
        d.type='ORTHO';d.ortho_scale=self.length*1.18;d.clip_end=5000;self.scene.camera=cam
        self.scene.render.engine='CYCLES';self.scene.cycles.samples=40;self.scene.cycles.use_denoising=True
        self.scene.render.resolution_x=2000;self.scene.render.resolution_y=1000;self.scene.render.resolution_percentage=100
        self.scene.render.image_settings.file_format='PNG';self.scene.view_settings.view_transform='AgX'
        for p in self.parts.values():
            for o in p.children_recursive:o.hide_render=not p['default_visible']
        for name,vec in [('studio',view),('side',(0,-1,0))]:
            cam.location=center+Vector(vec)*480
            cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
            self.scene.render.filepath=str(self.root/'renders'/f'{name}.png')
            bpy.ops.render.render(write_still=True)
        cam.location=center+Vector(view)*480;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
        bpy.ops.wm.save_as_mainfile(filepath=str(self.root/'source'/f'{self.asset_id}.blend'))
        manifest['artifacts']={'blend':f'source/{self.asset_id}.blend','glb':f'web/{self.asset_id}.glb','studio':'renders/studio.png','side':'renders/side.png'}
        (self.root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
        return manifest
