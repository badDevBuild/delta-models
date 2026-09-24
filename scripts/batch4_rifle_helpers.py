"""Batch four: shared presentation ornaments, never mechanical interfaces."""
import bpy,json,hashlib
from pathlib import Path
from model_helpers_amg import Sculpture
from rifle_batch3_helpers import side_plate, dot_texture, optic

URLS={
'aks74u':'https://www.imfdb.org/images/thumb/9/9f/DFHO_AKS74U.jpg/600px-DFHO_AKS74U.jpg',
'm16a4':'https://www.imfdb.org/images/thumb/d/d3/DFHO_M16A4.jpg/600px-DFHO_M16A4.jpg',
'g3':'https://www.imfdb.org/images/thumb/f/f1/DFHO_G3A3.jpg/600px-DFHO_G3A3.jpg',
'qbz95':'https://www.imfdb.org/images/thumb/5/53/DFHO_QBZ95.jpg/600px-DFHO_QBZ95.jpg'}

def guard(s,key,outline,hole,depth=6):
    o=s.poly('Fixed solid guard frame',key,outline,depth,s.metal,.5)
    s.cut(o,s.poly('Temporary silhouette cutter',key,hole,30,s.dark,.3))
    return o

def woodgrain(s,key,x0,x1,z,y,mat,count=6):
    # Small modeled veneers retain their color in GLB, no procedural-only texture.
    for sign in [-1,1]:
        for row in range(count):
            s.poly('Shallow wood grain relief',key,[(x0,z+row*1.45),(x1,z+row*1.45+.6),(x1,z+row*1.45+.9),(x0,z+row*1.45+.2)],.24,mat,.07,y=sign*y)

def finish(s,description):
    approx=[description,'2026-09-22 实际打开并查看游戏默认双侧截图；横向轮廓独立重建，宽度、遮蔽面、细小纹理和固定细节为艺术推断。','实心缩比外观艺术模型，封闭前端，无内部机构、膛室或真实安装接口；网页按外观分组，可选瞄具仅供数字展示。','未提取游戏网格或纹理；使用抽象浮雕替代商标与铭文，公开再分发授权尚未确认。']
    sources=['https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops',URLS[s.asset]]
    result=s.finish(sources,approx)
    (s.out/'SOURCE_NOTES.md').write_text('# '+s.asset.upper()+' 外观参考记录\n\n'+''.join('- '+u+'\n' for u in sources)+'\n'+''.join('- '+a+'\n' for a in approx)+'\n默认基础组整体融合后分平面胶合；可选瞄具不进入基础打印文件。尺寸是桌面艺术模型尺寸，不是实物机械尺寸。未进行实机打印。\n')
    return result

def optional_render(asset):
    root=Path(__file__).resolve().parents[1]/'assets'/asset
    bpy.ops.wm.open_mainfile(filepath=str(root/'source'/f'{asset}.blend'))
    for o in bpy.context.scene.objects:
        if o.type=='EMPTY' and o.name.startswith('part_'):
            for c in o.children_recursive:c.hide_render=False
    bpy.context.scene.render.filepath=str(root/'renders'/'optional.png')
    bpy.ops.render.render(write_still=True)
    return {'id':asset,'optional':str(root/'renders'/'optional.png')}
