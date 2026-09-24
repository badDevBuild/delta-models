"""Write a local collection index only after all registered files are present."""
from collections import Counter
from pathlib import Path
import json

from model_catalog import CONFIG, MODELS, ROOT
from slicing_evidence import check_slicing


def write_index():
    rows = []
    totals = Counter()
    for spec in MODELS:
        ident = spec['id']
        asset = ROOT / 'assets' / ident
        manifest = json.loads((asset / 'manifest.json').read_text())
        validation = json.loads((asset / 'print/validation.json').read_text())
        assert validation['passed'] and check_slicing(asset)['passed'], ident
        files = {'母版': f'source/{ident}.blend', 'GLB': f'web/{ident}.glb',
                 '预览': 'renders/studio.png', '几何包': f'print/{ident}-print.zip',
                 '切片包': f'print/{ident}-sliced.zip'}
        for name in files.values():
            assert (asset / name).is_file(), (ident, name)
        links = ' / '.join(f'[{label}](../assets/{ident}/{path})' for label, path in files.items())
        count = len(manifest['parts'])
        rows.append(f"| {spec['name']} | {spec['category']} | {spec['batch']} | {count} | {links} |")
        totals[spec['category']] += 1
    count = len(MODELS)
    scope = CONFIG.get('inventoryScope', {})
    lines = [f'# {count} 款模型文件索引', '',
             f"覆盖截至 {scope.get('asOf', '2026-09-22')} 核对的项目工作清单；不是官方公布的当前游戏总数。", '',
             '[打开交互收藏馆](http://127.0.0.1:5174/) · [清单核对依据](../research/remaining-roster-2026-09-22.md)', '',
             '每款可下载可编辑母版、网页 GLB、预览、装饰几何包和数字切片包。全部为非功能微缩外观模型；实机打印延后，公开再分发授权尚未确认。', '',
             '网页的外观组用于选件和分解展示，不等于打印胶合分件。', '',
             '| 模型 | 分类 | 批次 | 外观组 | 本地文件 |',
             '|---|---|---:|---:|---|', *rows, '',
             '分类数量按本项目展示标签统计：' + '、'.join(f'{name} {n}' for name, n in totals.items()) + '。', '']
    output = ROOT / 'docs/COLLECTION.md'
    output.write_text('\n'.join(lines))
    print(json.dumps({'models': count, 'index': str(output)}, ensure_ascii=False))


if __name__ == '__main__':
    write_index()
