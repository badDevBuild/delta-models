#!/usr/bin/env python3
"""Independently read exported STL/3MF geometry and verify print-mesh invariants.

No Blender or third-party packages are required. This is a geometry check, not
a slicer simulation, minimum-wall analysis, or a physical print test.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile


CORE_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
ROUND_DIGITS = 5


def read_stl(path: Path):
    """Read actual binary STL bytes; weld repeated triangle vertices by position."""
    payload = path.read_bytes()
    if len(payload) < 84:
        raise ValueError(f"Truncated STL: {path}")
    count = struct.unpack_from("<I", payload, 80)[0]
    if len(payload) != 84 + count * 50:
        raise ValueError(f"Not a well-formed binary STL: {path}")
    vertex_index = {}
    vertices, triangles = [], []
    for values in struct.iter_unpack("<12fH", payload[84:]):
        face = []
        for offset in (3, 6, 9):
            coordinate = tuple(round(values[offset + i], ROUND_DIGITS) for i in range(3))
            index = vertex_index.get(coordinate)
            if index is None:
                index = len(vertices)
                vertex_index[coordinate] = index
                vertices.append(coordinate)
            face.append(index)
        triangles.append(tuple(face))
    return vertices, triangles


def read_3mf(path: Path):
    """Read the standard model part and reject non-mm/ambiguous builds."""
    with zipfile.ZipFile(path) as archive:
        required = {"[Content_Types].xml", "_rels/.rels", "3D/3dmodel.model"}
        if not required.issubset(archive.namelist()):
            raise ValueError(f"Missing 3MF package entries: {path}")
        model = ET.fromstring(archive.read("3D/3dmodel.model"))
    if model.get("unit") != "millimeter":
        raise ValueError("3MF unit must explicitly be millimeter")
    ns = {"m": CORE_NS}
    objects = {obj.get("id"): obj for obj in model.findall("m:resources/m:object", ns)}
    items = model.findall("m:build/m:item", ns)
    if len(items) != 1:
        raise ValueError("Expected exactly one object per individual-part 3MF")
    item = items[0]
    if item.get("transform") not in (None, "1 0 0 0 1 0 0 0 1 0 0 0"):
        raise ValueError("Unexpected transform in individual-part 3MF")
    obj = objects[item.get("objectid")]
    vertices = [tuple(float(v.get(axis)) for axis in "xyz")
                for v in obj.findall("m:mesh/m:vertices/m:vertex", ns)]
    triangles = [tuple(int(t.get(f"v{i}")) for i in (1, 2, 3))
                 for t in obj.findall("m:mesh/m:triangles/m:triangle", ns)]
    return vertices, triangles


def inspect_mesh(vertices, triangles, build_volume=(256.0, 256.0, 256.0)):
    if not vertices or not triangles:
        return {"passed": False, "failures": ["empty_mesh"]}
    edges = defaultdict(lambda: [0, 0])
    vertex_links = [[] for _ in vertices]
    parent = list(range(len(vertices)))

    def find(value):
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    signed_volume = 0.0
    degenerate = 0
    used = set()
    for triangle in triangles:
        a, b, c = triangle
        if min(triangle) < 0 or max(triangle) >= len(vertices):
            raise ValueError("Triangle references missing vertex")
        used.update(triangle)
        vertex_links[a].append((b, c))
        vertex_links[b].append((c, a))
        vertex_links[c].append((a, b))
        av, bv, cv = (vertices[i] for i in triangle)
        ab = [bv[i] - av[i] for i in range(3)]
        ac = [cv[i] - av[i] for i in range(3)]
        cross = (ab[1] * ac[2] - ab[2] * ac[1],
                 ab[2] * ac[0] - ab[0] * ac[2],
                 ab[0] * ac[1] - ab[1] * ac[0])
        if len(set(triangle)) < 3 or sum(x * x for x in cross) < 1e-16:
            degenerate += 1
        signed_volume += (av[0] * (bv[1] * cv[2] - bv[2] * cv[1])
                          + av[1] * (bv[2] * cv[0] - bv[0] * cv[2])
                          + av[2] * (bv[0] * cv[1] - bv[1] * cv[0])) / 6.0
        for start, end in ((a, b), (b, c), (c, a)):
            union(start, end)
            edge = edges[tuple(sorted((start, end)))]
            edge[0] += 1
            edge[1] += 1 if start < end else -1
    components = len({find(v) for v in used})
    boundary = sum(count == 1 for count, _ in edges.values())
    non_manifold = sum(count != 2 for count, _ in edges.values())
    inconsistent = sum(count == 2 and orientation != 0 for count, orientation in edges.values())
    non_manifold_vertices = 0
    for links in vertex_links:
        if not links:
            continue
        neighborhood = defaultdict(list)
        for a, b in links:
            neighborhood[a].append(b)
            neighborhood[b].append(a)
        visited = set()
        stack = [next(iter(neighborhood))]
        while stack:
            value = stack.pop()
            if value in visited:
                continue
            visited.add(value)
            stack.extend(n for n in neighborhood[value] if n not in visited)
        if len(visited) != len(neighborhood) or any(len(v) != 2 for v in neighborhood.values()):
            non_manifold_vertices += 1
    minimum = [min(v[axis] for v in vertices) for axis in range(3)]
    maximum = [max(v[axis] for v in vertices) for axis in range(3)]
    size = [maximum[i] - minimum[i] for i in range(3)]
    fits = all(size[i] <= build_volume[i] + 0.001 for i in range(3))
    conservative = all(size[i] <= (230.0, 230.0, 250.0)[i] for i in range(3))
    failures = []
    if non_manifold:
        failures.append("non_manifold_edges")
    if inconsistent:
        failures.append("inconsistent_winding")
    if non_manifold_vertices:
        failures.append("non_manifold_vertices")
    if degenerate:
        failures.append("degenerate_triangles")
    if signed_volume <= 0:
        failures.append("non_positive_volume")
    if components != 1:
        failures.append("not_single_connected_component")
    if not fits:
        failures.append("exceeds_P1S_build_volume")
    if minimum[2] < -0.001 or abs(minimum[2]) > 0.001:
        failures.append("not_resting_on_Z_zero")
    return {
        "passed": not failures,
        "failures": failures,
        "vertices": len(vertices),
        "triangles": len(triangles),
        "connected_components": components,
        "boundary_edges": boundary,
        "non_manifold_edges": non_manifold,
        "non_manifold_vertices": non_manifold_vertices,
        "inconsistent_winding_edges": inconsistent,
        "degenerate_triangles": degenerate,
        "signed_volume_mm3": round(signed_volume, 5),
        "bounds_mm": {"min": [round(v, 5) for v in minimum],
                      "max": [round(v, 5) for v in maximum]},
        "dimensions_mm": [round(v, 5) for v in size],
        "fits_P1S_256mm": fits,
        "fits_conservative_230x230x250mm": conservative,
        "checks_not_performed": ["physical_print", "slicer_toolpath", "minimum_wall_thickness", "self_intersection"],
    }


def validate_directory(directory: Path):
    manifest = json.loads((directory / "manifest.json").read_text())
    parts = []
    for part in manifest["parts"]:
        record = {"name": part["name"]}
        try:
            record["stl"] = inspect_mesh(*read_stl(directory / part["stl"]))
            record["3mf"] = inspect_mesh(*read_3mf(directory / part["3mf"]))
            dims_a = record["stl"]["dimensions_mm"]
            dims_b = record["3mf"]["dimensions_mm"]
            volume_a = record["stl"]["signed_volume_mm3"]
            volume_b = record["3mf"]["signed_volume_mm3"]
            record["formats_agree"] = (
                record["stl"]["triangles"] == record["3mf"]["triangles"]
                and all(abs(a - b) < 0.001 for a, b in zip(dims_a, dims_b))
                and abs(volume_a - volume_b) < max(0.005, abs(volume_a) * 1e-5)
            )
            record["passed"] = record["stl"]["passed"] and record["3mf"]["passed"] and record["formats_agree"]
        except Exception as error:
            record.update(passed=False, error=str(error))
        parts.append(record)
    return {
        "schema": "delta-six-print-validation/v1",
        "purpose": "nonfunctional miniature decorative game-model parts",
        "evidence": "Actual exported STL bytes and 3MF XML were read independently",
        "passed": bool(parts) and all(part["passed"] for part in parts),
        "part_count": len(parts),
        "nominal_printer_build_volume_mm": [256, 256, 256],
        "printer_source": "https://store.bblcdn.com/7032c40b1ca64c70bcb3239d46cc72aa.pdf",
        "scope_limit": "Geometry validation only. This report does not test slicer paths or physical prints; current slicing status is recorded separately in slice-validation.json.",
        "parts": parts,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?",
                        default=Path(__file__).resolve().parents[1] / "output" / "print")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate_directory(args.directory)
    output = args.output or args.directory / "validation.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"passed": report["passed"], "part_count": report["part_count"],
                      "report": str(output)}, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
