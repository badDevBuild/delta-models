"""Owned helper for four distinct batch-three exterior sculptures, miniature units."""
import bpy,json,hashlib
from pathlib import Path
from model_helpers_amg import Sculpture

URLS={
'ak12':'https://www.imfdb.org/images/thumb/2/20/DFHO_AK12.jpg/600px-DFHO_AK12.jpg',
'aug':'https://www.imfdb.org/images/thumb/3/36/DFHO_AUG.jpg/600px-DFHO_AUG.jpg',
'asval':'https://www.imfdb.org/images/thumb/6/67/DFHO_ASVal.jpg/600px-DFHO_ASVal.jpg',
'k416':'https://www.imfdb.org/images/thumb/c/c1/DFHO_HK416.jpg/600px-DFHO_HK416.jpg'}

def side_plate(s,name,key,pts,y,mat,depth=.42,b=.25):
    for sign in [-1,1]:s.poly(name,key,pts,depth,mat,b,y=sign*y)

def dot_texture(s,key,rows,x,z,y,dx=.35,width=4,mat=None):
    for sign in [-1,1]:
        for row in range(rows):
            for j in range(width):s.box('Shallow molded texture',key,(x+row*dx+j*1.35,sign*y,z-row*1.7),(.67,.35,.6),mat or s.rubber,.12)

def sight(s,key,x,z,front=False):
    s.box('Sight attached lower foot',key,(x,0,z),(8,8,3),s.metal,.5)
    s.poly('Sight fixed raised tower',key,[(x-3,z),(x-2,z+9),(x-1,z+12),(x+2,z+12),(x+3,z+2)],5,s.metal,.5)
    s.cyl('Sight closed circular face',key,(x,0,z+8),2.25,3.4,s.edge,'X',.16)
    s.cyl('Sight blind inset',key,(x-1.72,0,z+8),1.1,.2,s.dark,'X',.05)

def optic(s,x,z):
    s.box('Optional digital optic attached base','optic',(x,0,z),(21,9,3.2),s.metal,.45)
    s.box('Optional optic short pedestal','optic',(x,0,z+2),(10,7,4),s.metal,.5)
    s.cyl('Optional opaque scope shell','optic',(x,0,z+8),6,25,s.metal,'X',.4)
    for xx in [x-12.6,x+12.6]:s.cyl('Opaque blue optic end','optic',(xx,0,z+8),4.7,.45,s.glass,'X',.13)
    for xx in [x-9,x+9]:s.cyl('Scope ring ornament','optic',(xx,0,z+8),6.35,2,s.polymer,'X',.2)
    s.cyl('Scope cosmetic side dial','optic',(x,-6.2,z+8),2.6,2.2,s.polymer,'Y',.22)

def finish(s,description):
    approx=[description,'实际查看游戏默认双侧图；横向比例据截图独立重建，宽度、遮蔽面、细小纹理和固定细节为艺术推断。','实心缩比外观艺术模型，封闭前端，无内部机构、膛室或真实安装接口；网页仅按外观分组，可选瞄具仅供数字展示。','未提取游戏网格或纹理；抽象浮雕替代商标与铭文，公开再分发授权尚未确认。']
    sources=['https://www.imfdb.org/wiki/Delta_Force:_Hawk_Ops',URLS[s.asset]]
    result=s.finish(sources,approx)
    note='# '+s.asset.upper()+' 外观参考记录\n\n2026-09-22 实际打开并查看以下游戏默认双侧截图。\n\n'+''.join('- '+u+'\n' for u in sources)+'\n'+''.join('- '+a+'\n' for a in approx)+'\n默认基础组整体融合后分平面胶合；可选瞄具不进入基础打印文件。尺寸是桌面艺术模型尺寸，不是实物机械尺寸。\n'
    (s.out/'SOURCE_NOTES.md').write_text(note)
    # Independent optional view from the editable master, without changing it.
    bpy.ops.wm.open_mainfile(filepath=str(s.out/'source'/f'{s.asset}.blend'))
    for o in bpy.context.scene.objects:
        if o.type=='EMPTY' and o.name.startswith('part_'):
            for c in o.children_recursive:c.hide_render=False
    bpy.context.scene.render.filepath=str(s.out/'renders'/'optional.png')
    bpy.ops.render.render(write_still=True)
    return result
