"""Shared exterior-sculpture mesh preparation. Never modifies the source scene."""
import json, struct, zipfile
import xml.etree.ElementTree as ET
import bpy, bmesh
from mathutils import Vector
CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
DISPLAY_ONLY_PREFIXES = ()

def mesh_bounds(bm):
    return {"min": [min(v.co[i] for v in bm.verts) for i in range(3)],
            "max": [max(v.co[i] for v in bm.verts) for i in range(3)]}

def descendant_meshes(root):
    result = []
    for child in root.children_recursive:
        if (child.type == "MESH" and not child.get("print_skip", False)
                and not child.name.startswith(DISPLAY_ONLY_PREFIXES)):
            result.append(child)
    return result

def copy_evaluated_meshes(sources, depsgraph, scene, name):
    vertices, faces = [], []
    for source in sources:
        evaluated = source.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        offset = len(vertices)
        vertices.extend(tuple(source.matrix_world @ vertex.co) for vertex in mesh.vertices)
        faces.extend(tuple(offset + v for v in poly.vertices) for poly in mesh.polygons)
        evaluated.to_mesh_clear()
    mesh = bpy.data.meshes.new(name + "_print_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name + "_print_work", mesh)
    scene.collection.objects.link(obj)
    return obj

def append_support_boxes(obj, specification):
    if not specification:
        return
    boxes = json.loads(specification) if isinstance(specification, str) else specification
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    for box in boxes:
        size = box["size"]
        if min(size) < 0.8:
            raise ValueError("Decorative reinforcement box must be at least 0.8 mm in every dimension")
        created = bmesh.ops.create_cube(bm, size=1.0)["verts"]
        for vert in created:
            vert.co = Vector([vert.co[i] * size[i] + box["center"][i] for i in range(3)])
    bm.to_mesh(obj.data)
    bm.free()

def voxel_union(obj, voxel):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    modifier = obj.modifiers.new(name="Decorative solid voxel union", type="REMESH")
    modifier.mode = "VOXEL"
    modifier.voxel_size = voxel
    modifier.adaptivity = 0.0
    modifier.use_smooth_shade = False
    modifier.use_remove_disconnected = False
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    return bm

def boolean_with_mesh(bm, cutter, operation):
    mesh = bpy.data.meshes.new("temporary_boolean_source")
    bm.to_mesh(mesh)
    obj = bpy.data.objects.new("temporary_boolean_source", mesh)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.update()
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    modifier = obj.modifiers.new("Planar ornamental glue face", "BOOLEAN")
    modifier.operation = operation
    modifier.solver = "EXACT"
    modifier.object = cutter
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bm.clear()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bpy.data.objects.remove(obj, do_unlink=True)

def cut_keep(bm, normal, point):
    """Keep the non-positive side and close the newly exposed flat cut."""
    normal = Vector(normal).normalized()
    point = Vector(point)
    distances = [(vert.co - point).dot(normal) for vert in bm.verts]
    if not distances or max(distances) <= 1e-6:
        return
    if min(distances) > 1e-6:
        bm.clear()
        return
    # A Boolean cube closes nested contours correctly. Filling each bisected
    # boundary loop separately would overlap faces across ornamental openings.
    diameter = max(1000.0, max((vert.co - point).length for vert in bm.verts) * 4.0)
    bpy.ops.mesh.primitive_cube_add(size=diameter, location=point - normal * diameter / 2.0)
    cutter = bpy.context.object
    cutter.name = "temporary_closed_halfspace"
    cutter.rotation_mode = "QUATERNION"
    cutter.rotation_quaternion = normal.to_track_quat("Z", "Y")
    boolean_with_mesh(bm, cutter, "INTERSECT")
    bpy.data.objects.remove(cutter, do_unlink=True)

def crop_bounds(bm, limits):
    if not limits:
        return
    if len(limits) != 6:
        raise ValueError("print_bounds_mm requires six [min x,y,z,max x,y,z] values")
    for axis in range(3):
        for side in (0, 1):
            normal = [0.0, 0.0, 0.0]
            point = [0.0, 0.0, 0.0]
            normal[axis] = -1.0 if side == 0 else 1.0
            point[axis] = limits[axis + side * 3]
            cut_keep(bm, normal, point)

def connected_meshes(bm):
    bm.verts.ensure_lookup_table()
    remaining = set(bm.verts)
    islands = []
    while remaining:
        first = remaining.pop()
        connected, stack = {first}, [first]
        while stack:
            vert = stack.pop()
            for edge in vert.link_edges:
                other = edge.other_vert(vert)
                if other in remaining:
                    remaining.remove(other)
                    connected.add(other)
                    stack.append(other)
        islands.append(connected)
    islands.sort(key=lambda island: min(v.co.x for v in island))
    result = []
    for island in islands:
        output = bmesh.new()
        mapping = {v: output.verts.new(v.co) for v in island}
        faces = {face for vert in island for face in vert.link_faces}
        for face in faces:
            output.faces.new([mapping[v] for v in face.verts])
        bmesh.ops.recalc_face_normals(output, faces=list(output.faces))
        result.append(output)
    return result

def normalized_triangles(bm):
    # Boolean/voxel evaluation can leave sub-micron slivers, far below the
    # 0.25 mm source resolution. Weld these before writing float32 STL.
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=0.001)
    bmesh.ops.dissolve_degenerate(bm, dist=0.001, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    if bm.calc_volume(signed=True) < 0:
        bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    bmesh.ops.triangulate(bm, faces=list(bm.faces), quad_method="BEAUTY", ngon_method="BEAUTY")
    bmesh.ops.dissolve_degenerate(bm, dist=0.001, edges=list(bm.edges))
    # dissolve_degenerate can create polygons, so triangulate once more.
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    boundary = [edge for edge in bm.edges if edge.is_boundary]
    if boundary and len(boundary) <= 20:
        # Collapse cleanup can leave a tiny triangular gap at a clipped bevel.
        # Only repair small boundary sets; a larger failure must reach validation.
        bmesh.ops.holes_fill(bm, edges=boundary, sides=0)
        bmesh.ops.triangulate(bm, faces=list(bm.faces))
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.verts.ensure_lookup_table()
    bm.verts.index_update()
    bounds = mesh_bounds(bm)
    minimum = bounds["min"]
    for vertex in bm.verts:
        vertex.co -= Vector(minimum)
    bm.normal_update()
    vertices = [tuple(v.co) for v in bm.verts]
    faces = [tuple(v.index for v in f.verts) for f in bm.faces]
    if any(len(face) != 3 for face in faces):
        raise ValueError("Failed to triangulate print mesh")
    return vertices, faces

def write_stl(path, vertices, faces):
    header = b"INERT MINIATURE DECORATIVE MODEL. Numeric coordinates are millimeters."
    with path.open("wb") as handle:
        handle.write(header.ljust(80, b" ")[:80])
        handle.write(struct.pack("<I", len(faces)))
        for a, b, c in faces:
            av, bv, cv = (Vector(vertices[i]) for i in (a, b, c))
            normal = (bv - av).cross(cv - av).normalized()
            handle.write(struct.pack("<12fH", *normal, *av, *bv, *cv, 0))

def write_3mf(path, name, vertices, faces):
    ET.register_namespace("", CORE_NS)
    tag = lambda local: "{" + CORE_NS + "}" + local
    model = ET.Element(tag("model"), unit="millimeter", attrib={"xml:lang": "en-US"})
    ET.SubElement(model, tag("metadata"), name="Title").text = name
    ET.SubElement(model, tag("metadata"), name="Description").text = (
        "Nonfunctional decorative game-model part. Geometry only; no slicing settings or G-code."
    )
    resources = ET.SubElement(model, tag("resources"))
    obj = ET.SubElement(resources, tag("object"), id="1", type="model", name=name)
    mesh = ET.SubElement(obj, tag("mesh"))
    verts = ET.SubElement(mesh, tag("vertices"))
    for vertex in vertices:
        ET.SubElement(verts, tag("vertex"), **{axis: f"{value:.8f}" for axis, value in zip("xyz", vertex)})
    tris = ET.SubElement(mesh, tag("triangles"))
    for a, b, c in faces:
        ET.SubElement(tris, tag("triangle"), v1=str(a), v2=str(b), v3=str(c))
    build = ET.SubElement(model, tag("build"))
    ET.SubElement(build, tag("item"), objectid="1")
    content_types = ('<?xml version="1.0" encoding="UTF-8"?>'
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                     '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
                     '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
            '</Relationships>')
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("3D/3dmodel.model", ET.tostring(model, encoding="utf-8", xml_declaration=True))
