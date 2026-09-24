"""Pack already validated inert miniature pieces into geometry-only P1S plates."""
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import shutil
import xml.etree.ElementTree as ET
import zipfile
from assembly_docs import write_assembly_docs

ROOT=Path(__file__).resolve().parents[1]
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',NS)
tag=lambda n:'{'+NS+'}'+n
PAD=5.0

def arrange(parts):
    """Deterministic shelf packing, leaving P1S front-left exclusion area empty."""
    plates=[]
    for part in sorted(parts,key=lambda p:(-p['dimensions'][1],-p['dimensions'][0],p['name'])):
        w,h=part['dimensions'][:2]
        if w>220 or h>210:
            raise ValueError(f'Piece too large for reserved plate area: {part["name"]}')
        placed=False
        for plate in plates:
            for row in plate['rows']:
                if h<=row['height'] and row['x']+w<=243:
                    plate['items'].append(dict(part,x=row['x'],y=row['y']))
                    row['x']+=w+PAD
                    placed=True
                    break
            if placed:break
            y=plate['next_y']
            if y+h<=245:
                plate['rows'].append({'x':23+w+PAD,'y':y,'height':h})
                plate['items'].append(dict(part,x=23,y=y))
                plate['next_y']=y+h+PAD
                placed=True
                break
        if not placed:
            plates.append({'rows':[{'x':23+w+PAD,'y':35,'height':h}],
                           'next_y':35+h+PAD,'items':[dict(part,x=23,y=35)]})
    return plates

def write_plate(path,items,directory):
    model=ET.Element(tag('model'),unit='millimeter',attrib={'xml:lang':'en-US'})
    ET.SubElement(model,tag('metadata'),name='Title').text=path.stem
    ET.SubElement(model,tag('metadata'),name='Description').text='Geometry only. Inert miniature sculpture. P1S plate arrangement; inspect and slice before printing.'
    resources=ET.SubElement(model,tag('resources'))
    build=ET.SubElement(model,tag('build'))
    for index,part in enumerate(items,1):
        with zipfile.ZipFile(directory/part['3mf']) as archive:
            src=ET.fromstring(archive.read('3D/3dmodel.model'))
        obj=src.find(tag('resources')+'/'+tag('object'))
        obj.set('id',str(index));obj.set('name',part['name'])
        resources.append(obj)
        transform=f'1 0 0 0 1 0 0 0 1 {part["x"]:.6f} {part["y"]:.6f} 0'
        ET.SubElement(build,tag('item'),objectid=str(index),transform=transform)
    with zipfile.ZipFile(directory/items[0]['3mf']) as sample,zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as archive:
        for name in ['[Content_Types].xml','_rels/.rels']:
            archive.writestr(name,sample.read(name))
        archive.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))

def package(asset_id,reuse_plates=False):
    directory=ROOT/'assets'/asset_id/'print'
    manifest=json.loads((directory/'manifest.json').read_text())
    validation=json.loads((directory/'validation.json').read_text())
    if not validation['passed']:
        raise ValueError('Refusing to package failed geometry')
    source=ROOT/'assets'/asset_id/'source'/(asset_id+'.blend')
    if manifest['source_sha256']!=hashlib.sha256(source.read_bytes()).hexdigest():
        raise ValueError('Print source hash is stale')
    byname={p['name']:p['stl'] for p in validation['parts']}
    parts=[dict(p,dimensions=byname[p['name']]['dimensions_mm']) for p in manifest['parts']]
    plates_dir=directory/'plates';plates_dir.mkdir(exist_ok=True)
    plate_records=json.loads((directory/'plates.json').read_text())['plates'] if reuse_plates else []
    if reuse_plates:
        expected=sorted(p['name'] for p in parts)
        actual=sorted(p['name'] for plate in plate_records for p in plate['parts'])
        if actual!=expected:raise ValueError('Saved plates do not cover current parts')
    for variant,optional in ([] if reuse_plates else [('base',False),('accessories',True)]):
        for index,plate in enumerate(arrange([p for p in parts if bool(p['accessory'])==optional]),1):
            filename=f'{asset_id}-{variant}-{index:02}.3mf'
            write_plate(plates_dir/filename,plate['items'],directory)
            plate_records.append({'file':'plates/'+filename,'variant':variant,
                                  'parts':[{'name':p['name'],'position_mm':[p['x'],p['y'],0],
                                            'dimensions_mm':p['dimensions']} for p in plate['items']]})
    if not reuse_plates:
        (directory/'plates.json').write_text(json.dumps({'schema':'delta-six-plates/v1',
            'geometry_only':True,'sliced':False,'physical_print_tested':False,
            'printer':'P1S','bed_mm':[256,256], 'reserved_origin_mm':[23,35],
            'packing_clearance_mm':PAD,'plates':plate_records},ensure_ascii=False,indent=2)+'\n')
    write_assembly_docs(directory.parent,manifest)
    table=io.StringIO();writer=csv.writer(table,delimiter='\t')
    writer.writerow(['piece','group','side','optional','dimensions_mm','original_assembly_bounds'])
    for p in parts:
        writer.writerow([p['name'],p['source_group'],p['assembly_side'],p['accessory'],p['dimensions'],p['source_bounds_mm']])
    (directory/'assembly-table.tsv').write_text(table.getvalue())
    guide=f'''# {asset_id.upper()} 装饰模型打印与装配

本包为实心微缩外观收藏件，不包含真实内部机构。基础款 {sum(not p['accessory'] for p in parts)} 件，配件 {sum(p['accessory'] for p in parts)} 件。

## 导入与切片

1. 在 Bambu Studio 中选择 P1S、实际喷嘴与实际 PLA 配置。当前规划使用 0.4 mm 喷嘴。
2. 逐个打开 plates 中的 3MF。它们是毫米单位的几何排版；如果提示非 Bambu 工程，选择作为几何导入。不要自动缩放。
3. 核对每个对象均落在板上，按实际热床检查摆放。建议从 0.16 mm 层高、3 层墙和约 15% 填充开始切片评估。小而高的件要检查裙边及支撑。
4. 查看层预览，重点检查薄凸纹、瞄具、悬垂、独立小件和初始层。三维网格检查没有证明这些细节一定能打印。
5. 切片工程、路径与实物结果的真实状态见项目报告；本几何包本身没有宣称已实机打印。

## 组装

请先打开本包的 [ASSEMBLY.md 装配图解](ASSEMBLY.md)。其中附完整侧视图、文件名配对表与前后段连接顺序，无需读取坐标。左右剖面是平整胶合面，先干拼对齐外轮廓，再胶合。whole 为未剖分的小件。若名称是 display_body，代表所有基础外观已经融合再平面分段，不能按网页的组件线拆开。

按侧视渲染与 assembly-table.tsv 的原始坐标对位，不要把 STL 在板上的排版位置当作装配位置。M7 配件文件单独列出，长短前端只选择一种配置；其他款式的打印包包含基础配置，可选配件当前用于网页展示。可用适合 PLA 的模型胶，胶合后不应反复拆卸。

数字模型的外观组件拆装与实体胶合结构分别设计。外观存在参考不可见区域的推断，具体见资产 manifest。实际试打前先选择一对较小半件验证细节和接缝。

## 验证证据

validation.json 为独立读取 STL 与 3MF 后的封闭性、流形、连通性、体积及热床范围检查。plates.json 记录排版。它们不替代实机试打、全面壁厚分析或权利授权。
'''
    (directory/'PRINTING.md').write_text(guide)
    archive_path=directory/(asset_id+'-print.zip')
    include=[directory/'manifest.json',directory/'validation.json',directory/'plates.json',directory/'PRINTING.md',directory/'assembly-table.tsv']
    include += [directory/p[k] for p in manifest['parts'] for k in ['stl','3mf']]
    include += [directory/p['file'] for p in plate_records]
    if (directory/'assembly-guide.png').exists():include.append(directory/'assembly-guide.png')
    include += [directory/'ASSEMBLY.md',directory/'assembly-reference.png']
    if (directory/'assembly-map.svg').exists():include.append(directory/'assembly-map.svg')
    with zipfile.ZipFile(archive_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for path in include:archive.write(path,path.relative_to(directory).as_posix())
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:raise ValueError('ZIP CRC check failed')
    result={'asset':asset_id,'pieces':len(parts),'plates':len(plate_records),
            'zip_bytes':archive_path.stat().st_size,'zip_sha256':hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            'archive_files':len(include),'archive_crc_passed':True}
    (directory/'archive-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    for older_name in ['plate-verification.json','package-validation.json']:
        older_path=directory/older_name
        if older_path.is_file():
            older=json.loads(older_path.read_text())
            older['archive_evidence_superseded_by']='archive-validation.json'
            older_path.write_text(json.dumps(older,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('assets',nargs='+')
    parser.add_argument('--reuse-plates',action='store_true',help='Refresh docs and archive without changing sliced plate inputs')
    args=parser.parse_args()
    for asset_id in args.assets:package(asset_id,reuse_plates=args.reuse_plates)
