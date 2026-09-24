"""Audit current artifact identities and stage evidence, without inflating scope."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import struct
import zipfile
from slicing_evidence import check_slicing
from model_catalog import MODEL_IDS,CONFIG

ROOT=Path(__file__).resolve().parents[1]
IDS=MODEL_IDS
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def audit():
    rows=[]
    for id in IDS:
        asset=ROOT/'assets'/id
        paths={'blend':asset/'source'/(id+'.blend'),'glb':asset/'web'/(id+'.glb'),
               'studio':asset/'renders/studio.png','side':asset/'renders/side.png',
               'manifest':asset/'manifest.json','print_zip':asset/'print'/(id+'-print.zip')}
        evidence={name:{'exists':path.is_file(),'bytes':path.stat().st_size if path.is_file() else None,
                        'sha256':sha(path) if path.is_file() else None}
                  for name,path in paths.items()}
        glb_valid=False;groups=[]
        if paths['glb'].exists():
            raw=paths['glb'].read_bytes()
            magic,version,length=struct.unpack_from('<4sII',raw,0)
            js_len,js_type=struct.unpack_from('<I4s',raw,12)
            data=json.loads(raw[20:20+js_len])
            groups=[n['name'] for n in data.get('nodes',[]) if n.get('name','').startswith('part_') and 'mesh' not in n]
            # Blender exporter may make primitive groups; verify logical IDs
            # with the separately executed Three.js manifest-aware tests too.
            glb_valid=magic==b'glTF' and version==2 and length==len(raw) and js_type==b'JSON' and bool(groups)
        geometry=False;pieces=None;plates=None
        pm=asset/'print/manifest.json';pv=asset/'print/validation.json';pp=asset/'print/plates.json'
        if pm.exists() and pv.exists() and paths['blend'].exists():
            manifest=json.loads(pm.read_text());validation=json.loads(pv.read_text())
            geometry=bool(validation.get('passed') and manifest.get('source_sha256')==sha(paths['blend']))
            pieces=validation.get('part_count')
            if pp.exists():plates=len(json.loads(pp.read_text())['plates'])
        archive_valid=False
        if paths['print_zip'].exists():
            with zipfile.ZipFile(paths['print_zip']) as archive:
                archive_valid=archive.testzip() is None
                zipped_manifest=json.loads(archive.read('manifest.json'))
                archive_valid=archive_valid and zipped_manifest.get('source_sha256')==sha(paths['blend'])
        slice_evidence=check_slicing(asset);sliced=slice_evidence['passed']
        rows.append({'id':id,'files':evidence,'glb_container_valid':glb_valid,'glb_group_nodes':groups,
                     'print_geometry_current':geometry,'print_piece_count':pieces,'plate_count':plates,
                     'archive_integrity_current':archive_valid,'slicing_verified':sliced,'slicing_errors':slice_evidence['errors'],
                     'physical_print_verified':False,'public_release_authorized':False})
    report={'schema':'delta-model-delivery-audit/v2','date':datetime.now().astimezone().date().isoformat(),'checked_at':datetime.now(timezone.utc).isoformat(),'assets':rows,'expected_model_count':len(IDS),
            'all_digital_artifacts_present':all(all(r['files'][k]['exists'] for k in ['blend','glb','studio','side','manifest']) and r['glb_container_valid'] for r in rows),
            'all_print_geometry_current':all(r['print_geometry_current'] and r['archive_integrity_current'] for r in rows),
            'all_sliced':all(r['slicing_verified'] for r in rows),'all_physical_prints_verified':False,
            'physical_print_required_now':not CONFIG.get('physicalPrintDeferred',False),
            'scope_limit':'File identity and individual stage evidence, not an overall completion verdict. Visual review and browser tests are recorded separately; physical printing is deferred by the user and public licensing remains separate.'}
    (ROOT/'reports/delivery-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['assets','scope_limit']}))
    return report

if __name__=='__main__':audit()
