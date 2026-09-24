"""Generate printable-sculpture pairing instructions from the actual part manifest."""
from pathlib import Path
import shutil

def write_assembly_docs(asset,manifest):
    asset=Path(asset);directory=asset/'print';asset_id=asset.name
    reference=asset/'renders/side.png'
    if not reference.is_file():raise ValueError('Missing side reference: '+str(reference))
    shutil.copy2(reference,directory/'assembly-reference.png')
    lines=[f'# {asset_id.upper()} 微缩收藏件装配图解','',
        '本说明仅用于包内实心外观雕塑的胶合。先去除打印支撑并干拼，确认轮廓吻合后再使用适合 PLA 的模型胶。实体没有反复拆装机构。','',
        '## 完整轮廓与方向','',
        '![完整侧视参考](assembly-reference.png)','',
        '图中左端为模型前端，右端为尾部。所有分段按这个方向排列。打印盘上零件的位置只为排版，不能当作装配位置。',
        '侧视图来自外观母版；打印版的微小纹理可能经过简化，以打印文件的实际表面为准。','']
    parts=manifest['parts']
    if asset_id!='m7':
        segments=sorted({p['segment'] for p in parts})
        pairs=[]
        for segment in segments:
            group=[p for p in parts if p['segment']==segment]
            by_side={p['assembly_side']:p for p in group}
            if len(group)!=2 or set(by_side)!={'left','right'}:
                raise ValueError('Expected exactly one left/right pair per segment')
            if abs(by_side['left']['source_bounds_mm']['min'][0]-by_side['right']['source_bounds_mm']['min'][0])>.001:
                raise ValueError('Left/right segment bounds differ')
            pairs.append((segment,by_side))
        lines+=['## 按文件名配对','',
            '`left` 与 `right` 表示同一段的两半；紧邻 `left/right` 前的数字是段号，例如 `display_body_01_02_left_01` 属于第 02 段。直接按下表配对，无需读取坐标。','',
            '| 装配位置 | 左半文件 | 右半文件 |','|---|---|---|']
        for index,(segment,pair) in enumerate(pairs):
            location='整件左右半' if len(pairs)==1 else ('前段（图中左侧）' if index==0 else '后段（图中右侧）')
            lines.append(f"| 第 {segment:02} 段：{location} | `{Path(pair['left']['stl']).name}` | `{Path(pair['right']['stl']).name}` |")
        lines+=['','![左右配对及分段顺序示意，非尺寸图](assembly-map.svg)','',
            '1. 找到同段号的左右两片。两片的大平整剖面相对，外侧纹理朝外；通过外轮廓对齐。右片在打印盘上的朝向可能与左片不同，需要拿起翻转后配对。',
            '2. 先干拼，检查上下轮廓和边缘是否连续。支撑残留应清理到不妨碍接触，不能靠强压消除错位。']
        if len(pairs)==2:
            lines += ['3. 第 01 段组成前段，第 02 段组成后段。将前段右端的平截面与后段左端的平截面对接；按上方侧视图核对上沿和下沿。四片整体干拼确认后，再依次胶合左右半片和前后两段。']
        else:
            lines += ['3. 本款只有这一对左右半片，没有额外前后分段。干拼吻合后即可胶合。']
        lines += ['','这些分件面为微缩雕塑自定义胶合面，与网页的外观组件边界不同。未观察实物前，不能保证打印后的接缝和强度已经通过。','']
        width=760;height=290
        elements=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="同号左右半片配对，然后前后连接">',
            '<rect width="760" height="290" fill="#fafaf7"/>',
            '<g font-family="sans-serif" fill="#253129">',
            '<text x="28" y="33" font-size="19">前端 ←　按段号排列　→ 尾部（配对示意，非尺寸图）</text>']
        for index,(segment,pair) in enumerate(pairs):
            x=50+index*355;w=300 if len(pairs)>1 else 650
            for row,side in enumerate(['left','right']):
                y=58+row*88
                elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="56" rx="7" fill="'+('#dce8cf' if index==0 else '#d5e1ed')+'" stroke="#627164"/>')
                elements.append(f'<text x="{x+16}" y="{y+34}" font-size="20">第 {segment:02} 段　'+('L / left 左半' if side=='left' else 'R / right 右半')+'</text>')
            elements.append(f'<text x="{x+12}" y="136" font-size="14">同号配对：大平整剖面相对</text>')
        elements += ['<text x="28" y="251" font-size="16">先干拼完整轮廓，确认贴合后再胶合。</text>','</g></svg>']
        (directory/'assembly-map.svg').write_text('\n'.join(elements)+'\n')
    else:
        lines+=['## 零件位置与配对','',
            '![M7 装饰分件图](assembly-guide.png)','',
            '| 文件名前缀 | 配对与位置 |','|---|---|',
            '| `handguard_left / right` | 护木左右两半，位于主体前方。 |',
            '| `receiver_left / right` | 中部外壳左右两半，前接护木、后接尾托。 |',
            '| `stock_left / right` | 尾托左右两半，位于最右侧。 |',
            '| `grip_left / right` | 后握把左右两半，位于中部外壳下方靠后。 |',
            '| `magazine_left / right` | 实心弹匣外观左右两半，位于外壳下方靠前。 |',
            '| `sights_01_left / right` | 前部小瞄具外观，安装于护木上方靠前。 |',
            '| `sights_02_left / right` | 后部小瞄具外观，安装于外壳上方靠后。 |',
            '| `barrel_short_whole` 或 `barrel_long_whole` | 封闭前端外观，二选一，位于护木最前端。 |',
            '| `optic_whole` | 可选瞄具装饰，位于中部外壳上方。 |',
            '| `foregrip_whole` | 可选前握把装饰，位于护木下方。 |','',
            '先把各组左右两半的平整剖面相对，按轮廓干拼；再排列护木—中部外壳—尾托，核对完整侧视轮廓。握把、实心弹匣外观和小瞄具按图定位。确认整体干拼后再胶合。小装饰件的最终贴合需实物试打核对。','']
    lines+=['## 试打后记录','',
        '记录支撑是否易拆、纹理是否缺失、平面接缝是否贴合和是否有断裂；保留干拼与胶合后的照片。打印问题按具体文件名反馈，便于只修复受影响的雕塑块。','']
    (directory/'ASSEMBLY.md').write_text('\n'.join(lines))
