"""Populate the local viewer only from existing, hashed build artifacts."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import shutil
from slicing_evidence import check_slicing
from model_catalog import MODELS,CONFIG

ROOT=Path(__file__).resolve().parents[1]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def sync():
    public=ROOT/'web/public'
    for folder in ['models','previews','downloads']:(public/folder).mkdir(parents=True,exist_ok=True)
    catalog={'schemaVersion':1,'updatedAt':datetime.now().astimezone().date().isoformat(),'models':[]}
    evidence=[]
    for spec in MODELS:
        id,name,category,length,description=(spec[k] for k in ['id','name','category','lengthMm','description'])
        asset=ROOT/'assets'/id
        glb=asset/'web'/(id+'.glb');blend=asset/'source'/(id+'.blend')
        preview=asset/'renders/catalog.png'
        if not preview.exists():preview=asset/'renders/studio.png'
        package=asset/'print'/(id+'-print.zip')
        required=[glb,blend,preview]
        if not all(p.exists() for p in required):
            continue
        for src,dest in [(glb,public/'models'/(id+'.glb')),(preview,public/'previews'/(id+'.png')),(blend,public/'downloads'/(id+'.blend'))]:
            shutil.copy2(src,dest)
        manifest_path=asset/'manifest.json'
        manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        length=manifest.get('display_length_mm',manifest.get('base_length_mm',length))
        geometry=False
        validation=asset/'print/validation.json';print_manifest=asset/'print/manifest.json'
        if validation.exists() and print_manifest.exists():
            vm=json.loads(validation.read_text());pm=json.loads(print_manifest.read_text())
            geometry=bool(vm.get('passed') and pm.get('source_sha256')==digest(blend))
        downloads={'blend':f'/downloads/{id}.blend'}
        if package.exists() and geometry:
            shutil.copy2(package,public/'downloads'/package.name)
            downloads['print']=f'/downloads/{id}-print.zip'
        status={
            'geometry':{'state':'passed' if geometry else 'pending','label':'打印网格已验证' if geometry else '打印网格待验收',
                        'detail':'实际 STL/3MF 读回，封闭性、连通性、正体积与尺寸检查。' if geometry else '母版与网页可查看，打印导出仍在处理。'},
            'slicing':{'state':'pending','label':'切片待验收','detail':'几何 3MF 不含已验证的机器路径。'},
            'physical':{'state':'pending','label':'未实机打印','detail':'按当前安排先制作数字模型，实机验证留待后续。' if CONFIG.get('physicalPrintDeferred') else '需要基础配置全套试打与装配反馈。'},
            'rights':{'state':'passed','label':'发布者声明已取得非商业分享授权','detail':'发布者声明已取得非商业下载、修改和再分发授权；模型资产按 CC BY-NC 4.0 分享。'}}
        slicing=check_slicing(asset)
        if slicing['passed']:
            status['slicing']={'state':'passed','label':'切片已验证','detail':slicing['report'].get('summary','')}
            sliced_package=asset/'print'/(id+'-sliced.zip')
            package_record=asset/'print/sliced-package-validation.json'
            record=json.loads(package_record.read_text()) if package_record.is_file() else {}
            if sliced_package.is_file() and record.get('sha256')==digest(sliced_package) and record.get('report_sha256')==digest(asset/'print/slice-validation.json'):
                shutil.copy2(sliced_package,public/'downloads'/sliced_package.name)
                downloads['sliced']=f'/downloads/{id}-sliced.zip'
        catalog['models'].append({'id':id,'name':name,'category':category,'description':description,
            'lengthMm':length,'batch':spec['batch'],'model':f'/models/{id}.glb','preview':f'/previews/{id}.png',
            'downloads':downloads,'status':status})
        evidence.append({'id':id,'blend_sha256':digest(blend),'glb_sha256':digest(glb),
                         'glb_bytes':glb.stat().st_size,'print_geometry_verified':geometry})
    (public/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'reports/assets-synced.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'models_synced':len(evidence),'ids':[r['id'] for r in evidence]}))

if __name__=='__main__':sync()
