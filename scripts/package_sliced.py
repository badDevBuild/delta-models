"""Package only current, verified native slice outputs; never submit a print job."""
from pathlib import Path
import argparse
import json
import zipfile
from slicing_evidence import check_slicing,digest

ROOT=Path(__file__).resolve().parents[1]

def package(asset_id):
    directory=ROOT/'assets'/asset_id/'print'
    evidence=check_slicing(directory.parent)
    if not evidence['passed']:
        raise ValueError(f'{asset_id}: '+', '.join(evidence['errors']))
    report=evidence['report']
    output=directory/(asset_id+'-sliced.zip')
    instruction='''# P1S 切片工程\n\n配置为 P1S、0.4 mm 喷嘴、PLA。使用 Bambu Studio 打开包内原生 .3mf，核对设备、实际耗材和热床，查看逐层预览后再手动决定是否打印。\n\n耗时与重量是切片器估算，不是实机测量。本包未发送打印任务，实体强度、外观细节和胶合装配尚未实测。\n\n基础盘与 M7 可选配件盘分开；M7 长短前端按选定外观择一使用。几何原件和装配坐标见单独的 *-print.zip。\n\n如果基础几何排版的支撑互相碰撞，切片工程采用加宽后的布局；每盘来源、输入输出 SHA-256 和布局记录见 slice-validation.json。\n'''
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        archive.writestr('OPEN-FIRST.md',instruction+'\n装配时直接查看本包的 [ASSEMBLY.md](ASSEMBLY.md)，附侧视图和文件名配对说明。\n')
        archive.write(directory/'slice-validation.json','slice-validation.json')
        for name in ['ASSEMBLY.md','assembly-reference.png','assembly-map.svg','assembly-guide.png']:
            if (directory/name).is_file():archive.write(directory/name,name)
        for entry in report['native_projects']:
            src=directory/entry['file']
            archive.write(src,src.name)
        profile_dir=ROOT/'tools/slicer-profiles/bambu-2.8.2.61'
        for name in ['machine.json','process.json','filament.json','provenance.json']:
            if (profile_dir/name).is_file():
                archive.write(profile_dir/name,'profiles/'+name)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError('Archive failed CRC validation')
    result={'asset':asset_id,'file':output.name,'bytes':output.stat().st_size,'sha256':digest(output),
            'report_sha256':digest(directory/'slice-validation.json')}
    (directory/'sliced-package-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('assets',nargs='+')
    for asset_id in parser.parse_args().assets:print(json.dumps(package(asset_id)))
