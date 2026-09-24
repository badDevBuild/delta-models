#!/usr/bin/env python3
"""Read actual geometry-only 3MF plates and conservatively certify placement.

Never edits print files. Clearance is a proven lower bound between actual mesh
XY projections, using their enclosing boxes or convex hulls. It is not an exact
concave-surface distance, and does not include slicer supports, brims or toolpaths.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
from model_catalog import MODEL_IDS

ROOT=Path(__file__).resolve().parents[1]
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
TOL=.001
IDENTITY=(1.,0.,0.,0.,1.,0.,0.,0.,1.,0.,0.,0.)

def transform_vertex(v,t):
    """3MF stores the affine matrix as four rows of three values."""
    return tuple(sum(v[j]*t[j*3+i] for j in range(3))+t[9+i] for i in range(3))

def parse_transform(text):
    t=tuple(map(float,text.split())) if text else IDENTITY
    if len(t)!=12 or not all(math.isfinite(x) for x in t):
        raise ValueError('Invalid 3MF affine transform')
    determinant=t[0]*(t[4]*t[8]-t[5]*t[7])-t[1]*(t[3]*t[8]-t[5]*t[6])+t[2]*(t[3]*t[7]-t[4]*t[6])
    if abs(determinant)<1e-12:
        raise ValueError('Singular 3MF affine transform')
    return t

def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def hull(points):
    pts=sorted(set(points))
    if len(pts)<=1:return pts
    lower=[]
    for p in pts:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    upper=[]
    for p in reversed(pts):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]

def point_segment_distance(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1];length=dx*dx+dy*dy
    if not length:return math.dist(p,a)
    f=max(0.,min(1.,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/length))
    return math.hypot(p[0]-a[0]-f*dx,p[1]-a[1]-f*dy)

def edges(poly):
    return list(zip(poly,poly[1:]+poly[:1]))

def on_segment(p,a,b):
    return abs(cross(a,b,p))<1e-9 and min(a[0],b[0])-1e-9<=p[0]<=max(a[0],b[0])+1e-9 and min(a[1],b[1])-1e-9<=p[1]<=max(a[1],b[1])+1e-9

def intersect(a,b,c,d):
    q=(cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b))
    if q[0]*q[1]<0 and q[2]*q[3]<0:return True
    return on_segment(c,a,b) or on_segment(d,a,b) or on_segment(a,c,d) or on_segment(b,c,d)

def inside(p,poly):
    if len(poly)<3:return any(on_segment(p,a,b) for a,b in edges(poly))
    signs=[cross(a,b,p) for a,b in edges(poly)]
    return all(q>=-1e-9 for q in signs) or all(q<=1e-9 for q in signs)

def convex_distance(a,b):
    if inside(a[0],b) or inside(b[0],a):return 0.
    ae,be=edges(a),edges(b)
    if any(intersect(u,v,w,x) for u,v in ae for w,x in be):return 0.
    return min([point_segment_distance(p,u,v) for p in a for u,v in be]+
               [point_segment_distance(p,u,v) for p in b for u,v in ae])

def read_plate(path):
    """Read mesh vertices/faces, apply build transforms, reject unsupported models."""
    with zipfile.ZipFile(path) as archive:
        root=ET.fromstring(archive.read('3D/3dmodel.model'))
    if root.get('unit')!='millimeter':raise ValueError('Expected millimeter units')
    objects={o.get('id'):o for o in root.findall('m:resources/m:object',NS)}
    records=[]
    for item in root.findall('m:build/m:item',NS):
        if item.get('printable','1') not in ('1','true'):raise ValueError('Non-printable build item requires explicit review')
        obj=objects[item.get('objectid')]
        if obj.find('m:components',NS) is not None:raise ValueError('Component graph 3MF not supported; use geometry-only plate')
        t=parse_transform(item.get('transform'))
        vertices=[transform_vertex(tuple(float(q.get(k)) for k in 'xyz'),t)
                  for q in obj.findall('m:mesh/m:vertices/m:vertex',NS)]
        if not vertices or not all(math.isfinite(q) for v in vertices for q in v):raise ValueError('Empty or non-finite vertices')
        triangles=obj.findall('m:mesh/m:triangles/m:triangle',NS)
        if not triangles:raise ValueError('Mesh has no faces')
        for tri in triangles:
            indices=[int(tri.get('v'+str(i))) for i in (1,2,3)]
            if min(indices)<0 or max(indices)>=len(vertices):raise ValueError('Triangle references missing vertex')
        lo=[min(v[i] for v in vertices) for i in range(3)];hi=[max(v[i] for v in vertices) for i in range(3)]
        records.append({'name':obj.get('name',item.get('objectid')),'vertices':len(vertices),'triangles':len(triangles),
                        'build_transform':t,'bounds_mm':{'min':lo,'max':hi},'_hull':hull([(v[0],v[1]) for v in vertices])})
    if not records:raise ValueError('Plate has no build items')
    return records

def validate_asset(asset_id,clearance=5.):
    directory=ROOT/'assets'/asset_id/'print'
    manifest=json.loads((directory/'plates.json').read_text())
    expected_origin=manifest.get('reserved_origin_mm')
    if expected_origin!=[23,35]:raise ValueError('Unexpected reserved plate origin; review explicit bounds')
    results=[]
    for spec in manifest['plates']:
        path=(directory/spec['file']).resolve()
        if directory.resolve() not in path.parents:raise ValueError('Plate path escapes asset directory')
        rows=read_plate(path);failures=[]
        expected=sorted(p['name'] for p in spec['parts'])
        if sorted(r['name'] for r in rows)!=expected:failures.append('build_items_do_not_match_plate_manifest')
        for r in rows:
            lo,hi=r['bounds_mm']['min'],r['bounds_mm']['max']
            r['rests_on_z_zero']=abs(lo[2])<=TOL
            r['inside_reserved_plate_area']=(lo[0]>=23-TOL and lo[1]>=35-TOL and hi[0]<=243+TOL and hi[1]<=245+TOL)
            r['inside_p1s_volume']=(min(lo)>=-TOL and max(hi)<=256+TOL)
            if not all(r[k] for k in ['rests_on_z_zero','inside_reserved_plate_area','inside_p1s_volume']):failures.append(r['name']+':placement')
        pairs=[]
        for a,b in itertools.combinations(rows,2):
            alo,ahi=a['bounds_mm']['min'],a['bounds_mm']['max'];blo,bhi=b['bounds_mm']['min'],b['bounds_mm']['max']
            gaps=[max(0.,alo[i]-bhi[i],blo[i]-ahi[i]) for i in range(2)]
            lower_bound=math.hypot(*gaps);method='actual_transformed_mesh_xy_bounding_boxes'
            if lower_bound<clearance-TOL:
                lower_bound=convex_distance(a['_hull'],b['_hull']);method='actual_transformed_mesh_xy_convex_hulls'
            proven=lower_bound>=clearance-TOL
            pairs.append({'objects':[a['name'],b['name']],'clearance_lower_bound_mm':lower_bound,'method':method,'required_clearance_proven':proven})
            if not proven:failures.append(a['name']+' / '+b['name']+':clearance_not_proven')
        for r in rows:r.pop('_hull')
        results.append({'file':spec['file'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'passed':not failures,
                        'failures':failures,'objects':rows,'object_pairs':pairs})
    return {'asset':asset_id,'passed':bool(results) and all(p['passed'] for p in results),'plates':results}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('assets',nargs='*',default=MODEL_IDS,choices=MODEL_IDS)
    parser.add_argument('--output',type=Path,default=ROOT/'reports/plate-layout-validation.json')
    args=parser.parse_args();results=[]
    for asset in args.assets:
        try:results.append(validate_asset(asset))
        except Exception as exc:results.append({'asset':asset,'passed':False,'error':str(exc)})
    report={'schema':'delta-six-plate-layout-validation/v1','checked_at':datetime.now().astimezone().isoformat(),
            'passed':bool(results) and all(r['passed'] for r in results),'required_clearance_mm':5.,'numeric_tolerance_mm':TOL,
            'reserved_xy_mm':{'min':[23,35],'max':[243,245]},'nominal_build_volume_mm':[256,256,256],
            'scope':'Actual geometry-only 3MF mesh vertices/faces and build transforms. XY clearance is a conservative certified lower bound, not an exact concave-mesh distance.',
            'not_checked':['supports','brims','rafts','slicer_toolpaths','nozzle_travel','physical_print','mesh_manifoldness'],
            'assets':results}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'assets':[{k:r[k] for k in ['asset','passed']} for r in results],'report':str(args.output)}))
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
