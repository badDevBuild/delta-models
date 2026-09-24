#!/usr/bin/env python3
"""Make nonfunctional decorative print parts from a read-only Blender source.

Run with a separate background Blender process, never against the live MCP scene:
  Blender --background --python scripts/prepare_print.py -- --source output/m7_display.blend

Coordinates in the source use numeric millimeters (scene scale_length=0.001).
Each part_* empty owns mesh descendants. Optional source-empty properties:
  print_skip: bool; print_split: bool; print_bounds_mm: [xmin,ymin,zmin,xmax,ymax,zmax]
  print_reinforcements: JSON string containing simple ornamental box supports
    [{"center":[x,y,z], "size":[x,y,z]}]. No mechanisms or real interfaces.

The source file is opened but is never saved or overwritten. Evaluated meshes
are copied into a new scene and the original source objects are not edited.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

import bmesh
import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
PARTS = (
    "part_receiver", "part_handguard", "part_stock", "part_grip",
    "part_magazine", "part_barrel_short", "part_sights",
    "part_barrel_long", "part_optic", "part_foregrip",
)
ACCESSORIES = {"part_barrel_long", "part_optic", "part_foregrip"}
CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
REFERENCE_SCALE = 300.0 / 1173.0
DISPLAY_ONLY_PREFIXES = ("Optic rear red dot", "Stock cheek grooves")


def reference_x(px):
    return (px - 602.5) * REFERENCE_SCALE


def reference_z(py):
    return (300.0 - py) * REFERENCE_SCALE


def reference_plane(a, b):
    """Upward-facing normal for a slanted x/z ornamental mating surface."""
    point = Vector((reference_x(a[0]), 0.0, reference_z(a[1])))
    delta = Vector((reference_x(b[0]) - point.x, 0.0, reference_z(b[1]) - point.z))
    return Vector((-delta.z, 0.0, delta.x)).normalized(), point


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "assets/m7/source/m7.blend")
    parser.add_argument("--output", type=Path, default=ROOT / "assets/m7/print")
    parser.add_argument("--voxel", type=float, default=0.25)
    parser.add_argument("--no-split", action="store_true")
    parser.add_argument("--keep-tiny", action="store_true",
                        help="Keep detached fragments below 0.05 mm³ instead of recording and discarding them")
    parser.add_argument("--only", nargs="*", choices=PARTS)
    parser.add_argument("--skip-preview", action="store_true")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])


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


def append_reference_prism(obj, points, depth):
    """Add a small solid decorative support specified by the image-side profile."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    vertices = [bm.verts.new((reference_x(x), y, reference_z(z)))
                for y in (-depth / 2, depth / 2) for x, z in points]
    count = len(points)
    bm.faces.new(list(reversed(vertices[:count])))
    bm.faces.new(vertices[count:])
    for i in range(count):
        j = (i + 1) % count
        bm.faces.new([vertices[i], vertices[j], vertices[j + count], vertices[i + count]])
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    bm.free()


def add_print_strengthening(obj, part_name):
    """Strengthen only external ornaments; these are custom-scale solid glue seams."""
    boxes = []
    notes = []
    if part_name == "part_receiver":
        boxes.append({"center": [reference_x(742.5), 0, reference_z(178)],
                      "size": [369 * REFERENCE_SCALE, 8.0, 5.0]})
        boxes.append({"center": [reference_x(964.5), 0, reference_z(242)],
                      "size": [11 * REFERENCE_SCALE, 14.8, 10.0]})
        for sign in (-1, 1):
            boxes.extend([
                {"center": [reference_x(696), sign * 9.0, reference_z(299)], "size": [6.0, 3.0, 3.0]},
                {"center": [reference_x(790), sign * 8.6, reference_z(301)], "size": [2.0, 2.0, 2.0]},
                {"center": [reference_x(830), sign * 9.3, reference_z(294)], "size": [9.0, 3.2, 3.2]},
            ])
        append_reference_prism(obj, [(598, 328), (716, 353), (716, 371), (598, 343)], 15.4)
        append_reference_prism(obj, [(811, 321), (854, 307), (867, 337), (814, 344)], 15.2)
        notes.extend(["solid ornamental rail plinth", "short external-control back supports",
                      "solid stock seam bridge", "slanted magazine and grip glue surfaces"])
    if part_name == "part_handguard":
        boxes.append({"center": [reference_x(552), 0, reference_z(232)],
                      "size": [10 * REFERENCE_SCALE, 16.0, 23.0]})
        notes.append("short solid rear bridge up to planar receiver glue face")
    if part_name == "part_stock":
        for sign in (-1, 1):
            boxes.extend([
                {"center": [reference_x(1045), sign * 6.0, reference_z(281)], "size": [8.0, 5.0, 2.4]},
                {"center": [reference_x(1118), sign * 4.4, reference_z(303)], "size": [3.4, 3.4, 3.4]},
            ])
        notes.append("short back supports for thin floating stock ornaments")
    if part_name == "part_optic":
        boxes.append({"center": [reference_x(722), 0, 35.80], "size": [21.0, 13.0, 1.4]})
        notes.append("flat decorative mounting foot down to rail-top glue plane")
    append_support_boxes(obj, boxes)
    return notes


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


def trim_receiver_joint(bm, a, b, low_x, high_x):
    """Remove material below a glue plane within one ornament's footprint."""
    cutter_bm = bmesh.new()
    vertices = bmesh.ops.create_cube(cutter_bm, size=1.0)["verts"]
    xmin, xmax = reference_x(low_x), reference_x(high_x)
    for vert in vertices:
        vert.co = ((xmin + xmax) / 2 + vert.co.x * (xmax - xmin),
                   vert.co.y * 100, vert.co.z * 200)
    normal, point = reference_plane(a, b)
    cut_keep(cutter_bm, normal, point)
    mesh = bpy.data.meshes.new("temporary_joint_wedge")
    cutter_bm.to_mesh(mesh)
    cutter_bm.free()
    cutter = bpy.data.objects.new("temporary_joint_wedge", mesh)
    bpy.context.scene.collection.objects.link(cutter)
    boolean_with_mesh(bm, cutter, "DIFFERENCE")
    bpy.data.objects.remove(cutter, do_unlink=True)


def trim_custom_glue_faces(bm, part_name):
    magazine_seam = ((598, 339), (716, 367))
    grip_seam = ((811, 335), (858, 328))
    if part_name == "part_receiver":
        # Move the local cutter's side walls beyond the support profile to
        # avoid coplanar touching edges at the ornamental seam endpoints.
        trim_receiver_joint(bm, *magazine_seam, 594, 721)
        trim_receiver_joint(bm, *grip_seam, 808, 970)
    elif part_name == "part_magazine":
        cut_keep(bm, *reference_plane(*magazine_seam))
    elif part_name == "part_grip":
        cut_keep(bm, *reference_plane(*grip_seam))
    elif part_name in {"part_sights", "part_optic"}:
        # External scenic accessories rest on a flat face at the decorative
        # teeth's top, with no clips, slots, or standard interface dimensions.
        cut_keep(bm, (0, 0, -1), (0, 0, 35.21))


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


def printable_halves(bm, enabled, part_name=""):
    bounds = mesh_bounds(bm)
    if enabled and bounds["min"][1] < -0.5 and bounds["max"][1] > 0.5:
        result = []
        for side, sign in (("left", 1.0), ("right", -1.0)):
            half = bm.copy()
            cut_keep(half, (0.0, sign, 0.0), (0.0, 0.0, 0.0))
            if not half.faces:
                half.free()
                continue
            # Original x remains print x. Original z becomes ±print y;
            # the y=0 glue plane lies at print z=0. Determinant stays +1.
            for v in half.verts:
                x, y, z = v.co
                v.co = (x, sign * z, -sign * y)
            result.append((side, half, "split_y0_flat_face_down"))
        return result
    output = bm.copy()
    if part_name in {"part_barrel_short", "part_barrel_long"}:
        for v in output.verts:
            x, y, z = v.co
            v.co = (y, -z, -x)
        return [("whole", output, "rear_flat_glue_face_down_use_brim")]
    if part_name in {"part_optic", "part_foregrip"}:
        return [("whole", output, "original_z_down_check_support_in_slicer")]
    # Side-down orientation for off-centre small ornaments; bottom is normalized later.
    for v in output.verts:
        x, y, z = v.co
        v.co = (x, z, -y)
    return [("whole", output, "side_down_check_support_in_slicer")]


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
    header = b"M7 NONFUNCTIONAL DECORATIVE MODEL. Numeric coordinates are millimeters."
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


def keep_assembly_preview_mesh(bm, part_name):
    mesh = bpy.data.meshes.new(part_name + "_print_assembly")
    bm.to_mesh(mesh)
    obj = bpy.data.objects.new(part_name + "_assembly_preview", mesh)
    bpy.context.scene.collection.objects.link(obj)
    palette = {
        "part_receiver": (0.30, 0.34, 0.39, 1),
        "part_handguard": (0.47, 0.52, 0.40, 1),
        "part_stock": (0.32, 0.43, 0.52, 1),
        "part_grip": (0.46, 0.48, 0.50, 1),
        "part_magazine": (0.60, 0.46, 0.29, 1),
        "part_barrel_short": (0.74, 0.35, 0.12, 1),
        "part_sights": (0.60, 0.66, 0.72, 1),
    }
    mat = bpy.data.materials.new(part_name + "_assembly_color")
    mat.diffuse_color = palette.get(part_name, (0.4, 0.4, 0.4, 1))
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = mat.diffuse_color
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.65
    obj.data.materials.append(mat)
    obj.hide_render = part_name in ACCESSORIES
    return obj


def render_assembly(path):
    scene = bpy.context.scene
    camera_data = bpy.data.cameras.new("Print assembly orthographic camera")
    camera = bpy.data.objects.new("Print assembly orthographic camera", camera_data)
    scene.collection.objects.link(camera)
    camera.location = (0, -520, 1)
    camera.rotation_euler = (Vector((0, 0, 1)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 329
    camera_data.clip_end = 2000
    scene.camera = camera
    world = bpy.data.worlds.new("Print assembly studio world")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.19, 0.21, 0.25, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.45
    scene.world = world
    for name, location, energy, size in [
        ("Key", (-100, -190, 180), 850000, 260),
        ("Fill", (100, -120, 30), 450000, 180),
        ("Rim", (0, 60, 170), 500000, 150),
    ]:
        data = bpy.data.lights.new(name, "AREA")
        data.energy, data.shape, data.size = energy, "DISK", size
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = location
        light.rotation_euler = (-light.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 12
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1536
    scene.render.resolution_y = 600
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(path)
    scene.view_settings.view_transform = "AgX"
    bpy.ops.render.render(write_still=True)


def package_outputs(output, manifest, include_preview):
    filename = output / "m7-print.zip"
    paths = [Path("manifest.json"), Path("validation.json")]
    paths += [Path(part[key]) for part in manifest["parts"] for key in ("stl", "3mf")]
    if include_preview:
        paths.append(Path("assembly-guide.png"))
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in paths:
            archive.write(output / path, path.as_posix())
        archive.write(ROOT / "assets/m7/print/PRINTING.md", "PRINTING.md")
    return filename


def main():
    args = arguments()
    if not 0.22 <= args.voxel <= 0.30:
        raise ValueError("Use 0.22–0.30 mm voxel size for this decorative print conversion")
    source = args.source.resolve()
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(source))
    source_scene = bpy.context.scene
    depsgraph = bpy.context.evaluated_depsgraph_get()
    missing = [part for part in (args.only or PARTS) if part not in source_scene.objects]
    if missing:
        raise ValueError("Missing required part roots: " + ", ".join(missing))
    scene = bpy.data.scenes.new("PRINT_WORK_COPY_DO_NOT_SAVE_SOURCE")
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    copied = []
    for part_name in args.only or PARTS:
        root = source_scene.objects[part_name]
        if root.get("print_skip", False):
            continue
        obj = copy_evaluated_meshes(descendant_meshes(root), depsgraph, scene, part_name)
        copied.append((part_name, obj, {
            "split": bool(root.get("print_split", True)),
            "bounds": list(root["print_bounds_mm"]) if "print_bounds_mm" in root else None,
            "reinforcements": root.get("print_reinforcements"),
        }))
    bpy.context.window.scene = scene
    (args.output / "stl").mkdir(parents=True, exist_ok=True)
    (args.output / "3mf").mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "m7-display-print-manifest/v1",
        "purpose": "300 mm nonfunctional decorative game-model parts; no real firearm interfaces or mechanisms",
        "source_blend": "../source/m7.blend", "source_sha256": source_hash,
        "coordinate_unit": "millimeter", "voxel_size_mm": args.voxel,
        "geometry_3mf_only": True, "physical_print_tested": False,
        "slicing_status_scope": "This manifest describes geometry-only exports. Current slicing evidence is recorded separately in slice-validation.json.",
        "display_only_excluded_prefixes": list(DISPLAY_ONLY_PREFIXES),
        "custom_print_strengthening": {},
        "glue_planes_reference_pixels": {
            "magazine_to_receiver": [[598, 339], [716, 367]],
            "grip_to_receiver": [[811, 335], [858, 328]],
            "stock_to_receiver_x": 968,
        },
        "parts": [], "discarded_tiny_fragments": [],
    }
    for part_name, obj, config in copied:
        print("PREPARING " + part_name, flush=True)
        append_support_boxes(obj, config["reinforcements"])
        manifest["custom_print_strengthening"][part_name] = add_print_strengthening(obj, part_name)
        bm = voxel_union(obj, args.voxel)
        if part_name in {"part_magazine", "part_grip"} and config["bounds"]:
            config["bounds"][5] = 60.0
        crop_bounds(bm, config["bounds"])
        trim_custom_glue_faces(bm, part_name)
        if not args.skip_preview:
            keep_assembly_preview_mesh(bm, part_name)
        islands = connected_meshes(bm)
        for island_index, island in enumerate(islands, 1):
            volume = abs(island.calc_volume(signed=True))
            if volume < 0.05 and not args.keep_tiny:
                manifest["discarded_tiny_fragments"].append({"part": part_name, "island": island_index,
                                                             "volume_mm3": volume})
                island.free()
                continue
            source_bounds = mesh_bounds(island)
            suffix = f"_{island_index:02}" if len(islands) > 1 else ""
            for side, half, orientation in printable_halves(island, config["split"] and not args.no_split, part_name):
                # Cutting can disconnect an ornamental loop; each output stays one solid.
                half_islands = connected_meshes(half)
                for split_index, solid in enumerate(half_islands, 1):
                    split_suffix = f"_{split_index:02}" if len(half_islands) > 1 else ""
                    name = part_name.removeprefix("part_") + suffix + "_" + side + split_suffix
                    vertices, faces = normalized_triangles(solid)
                    stl_path = Path("stl") / (name + ".stl")
                    mf_path = Path("3mf") / (name + ".3mf")
                    write_stl(args.output / stl_path, vertices, faces)
                    write_3mf(args.output / mf_path, name, vertices, faces)
                    manifest["parts"].append({
                        "name": name, "source_group": part_name,
                        "accessory": part_name in ACCESSORIES,
                        "stl": str(stl_path), "3mf": str(mf_path),
                        "assembly_side": side, "orientation": orientation,
                        "source_bounds_mm": source_bounds,
                        "planar_trim_bounds_mm": config["bounds"],
                        "reinforcement_specification": config["reinforcements"],
                        "triangles": len(faces),
                    })
                    solid.free()
                half.free()
            island.free()
        bm.free()
        bpy.data.objects.remove(obj, do_unlink=True)
    if hashlib.sha256(source.read_bytes()).hexdigest() != source_hash:
        raise RuntimeError("Source .blend changed while preparation ran; do not trust this output")
    manifest_path = args.output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validate_print import validate_directory
    report = validate_directory(args.output)
    (args.output / "validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print("PRINT_RESULT=" + json.dumps({"passed": report["passed"], "part_count": report["part_count"],
                                      "manifest": str(manifest_path)}, ensure_ascii=False), flush=True)
    if not report["passed"]:
        raise RuntimeError("Exported mesh validation failed; inspect output/print/validation.json")
    if not args.skip_preview:
        render_assembly(args.output / "assembly-guide.png")
    package = package_outputs(args.output, manifest, not args.skip_preview)
    print("PRINT_PACKAGE=" + str(package), flush=True)


if __name__ == "__main__":
    main()
