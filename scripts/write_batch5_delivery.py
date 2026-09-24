"""Summarize the final batch from current, independently produced evidence."""
from datetime import datetime, timezone
import hashlib
import json

from model_catalog import MODELS, ROOT


def read(path):
    return json.loads((ROOT / path).read_text())


def write():
    expected = [m for m in MODELS if m['batch'] == 5]
    assert len(expected) == 31 and len(MODELS) == 67
    reports = {
        '母版回读': 'batch5-blender-readback.json',
        '材质核对': 'batch5-material-review.json',
        '归档回读': 'batch5-archive-readback.json',
        '排版检查': 'batch5-plate-layout-validation.json',
        '实际浏览器检查': 'batch5-browser-validation.json',
        '原有资产保留': 'batch5-existing-assets-preserved.json',
        '资源与构建副本': '67-model-http-validation.json',
        '清单覆盖': 'inventory-coverage.json',
    }
    for path in reports.values():
        assert read('reports/' + path)['passed'], path
    expected_ids = {model['id'] for model in expected}
    for name in ['batch5-blender-readback.json', 'batch5-material-review.json',
                 'batch5-archive-readback.json', 'batch5-browser-validation.json']:
        records = read('reports/' + name)['models']
        assert len(records) == 31 and {row['id'] for row in records} == expected_ids, name
    placements = read('reports/batch5-plate-layout-validation.json')['assets']
    assert len(placements) == 31 and {row['asset'] for row in placements} == expected_ids
    resources = read('reports/67-model-http-validation.json')
    assert resources['models'] == 67 and resources['resources'] == 335
    audit = read('reports/delivery-audit.json')
    for key in ['all_digital_artifacts_present', 'all_print_geometry_current', 'all_sliced']:
        assert audit[key], key
    assert audit['expected_model_count'] == 67 and not audit['physical_print_required_now']
    viewer = read('output/viewer-validation.json')
    assert viewer['passed'] and len(viewer['models']) == 67
    table, rows = [], []
    for spec in expected:
        ident = spec['id']
        manifest = read(f'assets/{ident}/manifest.json')
        print_manifest = read(f'assets/{ident}/print/manifest.json')
        plates = read(f'assets/{ident}/print/plates.json')['plates']
        visual = read(f'assets/{ident}/visual-review.json')
        source = ROOT / f'assets/{ident}/source/{ident}.blend'
        glb = ROOT / f'assets/{ident}/web/{ident}.glb'
        digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
        assert visual['passed'] and visual['source_sha256'] == digest(source)
        assert visual['glb_sha256'] == digest(glb)
        row = {'id': ident, 'name': spec['name'], 'length_mm': manifest['display_length_mm'],
               'groups': len(manifest['parts']), 'editable_meshes': manifest['mesh_count'],
               'pieces': len(print_manifest['parts']), 'plates': len(plates),
               'source_sha256': visual['source_sha256'], 'glb_sha256': visual['glb_sha256']}
        rows.append(row)
        table.append(f"| [{spec['name']}](../assets/{ident}/renders/studio.png) | {spec['category']} | {row['length_mm']:.2f} | {row['groups']} | {row['editable_meshes']} | {row['pieces']} / {row['plates']} | [来源](../assets/{ident}/SOURCE_NOTES.md) / [复核](../assets/{ident}/visual-review.json) |")
    totals = {key: sum(row[key] for row in rows) for key in ['groups', 'editable_meshes', 'pieces', 'plates']}
    lines = ['# 第五批：剩余 31 款数字模型', '',
             '按用户“一次性把剩下的都做完”的安排，本批补齐截至 2026-09-22 核对的项目工作清单，收藏馆由 36 款增至 **67 款**。这是有日期和范围的项目清单，不是官方公布的实时游戏总数。核对方法见 [清单研究](../research/remaining-roster-2026-09-22.md)。', '',
             '**本批 31 款数字模型已完成并接入同一网页。** 原有 36 款关键资产保持一致，继续按用户安排暂不实机打印。', '',
             '[打开第五批](http://127.0.0.1:5174/?batch=5) · [全部 67 款文件索引](COLLECTION.md) · [打开全部模型](http://127.0.0.1:5174/)', '',
             '| 模型预览 | 分类 | 微缩长度 mm | 外观组 | 编辑网格 | 胶合件 / 盘 | 外观依据 |',
             '|---|---|---:|---:|---:|---:|---|', *table, '',
             f"本批合计 {totals['groups']} 个外观组、{totals['editable_meshes']} 个可编辑源网格、{totals['pieces']} 个胶合分件、{totals['plates']} 个数字排版盘。外观组含数字可选附件，编辑网格数量不代表网页绘制次数或打印件数。", '',
             '每款包含 Blender 母版、网页 GLB、默认/侧视/配件渲染、可重建脚本、来源记录、装饰几何包与离线数字切片包。网页支持旋转缩放、视角切换、爆炸展示、选件、隐藏、单独查看、取下装回、配件切换和复原。实体胶合片采用独立的平面分件方案；可选光学附件仅供网页展示。', '',
             '外观依据实际查看的游戏图片独立重建，三维厚度、遮蔽面与微细纹理含艺术推断。SVCH、RM277 与 MK4 的部分参考为宣传或改装画面，不能确认完整默认配置；FS-12 的尾托细部也含推断，各款来源记录已单列。模型属于截图重建的微缩艺术版本，不是游戏原始网格或逐顶点复制。所有前端封闭，无内部机构或真实功能接口。', '',
             '数字切片沿用 P1S、0.4 mm 喷嘴、Bambu PLA Basic、0.16 mm 层高、3 道墙、15% 填充、树状支撑与纹理 PEI 板，在隔离配置中执行，没有连接或启动打印机。网格与切片通过不能代替最小壁厚、实物强度、接缝和支撑拆除效果的试打。', '',
             '## 检查证据', '',
             f"Three.js 自动回归 {len(viewer['checks'])} 项通过；新增 31 款均执行了实际浏览器配件切换、取下组件、爆炸展示和复原检查。全库 335 个模型、预览与下载资源可访问，静态构建副本与网页资源逐文件一致。", '',
             *[f'- [{label}](../reports/{path})：通过，详细范围和文件身份见报告。' for label, path in reports.items()],
             '- [Three.js 自动回归](../output/viewer-validation.json) 与实际浏览器操作分别记录。',
             '- [全库阶段审计](../reports/delivery-audit.json)：67 款数字、几何和切片均为当前版本，实机状态保持未验证。', '',
             '静态构建成功，主 JavaScript 包约 659 kB（gzip 约 168 kB），触发 Vite 的 500 kB 分包建议；这是后续加载优化项，当前模型按需载入。手机宽度检查仅覆盖 390 × 844 的页面尺寸、无横向溢出和侧视控件，未作为真实手机设备验收。', '',
             '当前产物保存在本地，尚未公开发布；游戏外观美术再分发的授权与开放许可仍需单独处理。', '',
             '历史批次：[第一批](DELIVERY.md)、[第二批](BATCH-2.md)、[第三批](BATCH-3.md)、[第四批](BATCH-4.md)。', '']
    (ROOT / 'docs/BATCH-5.md').write_text('\n'.join(lines))
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'passed': True,
              'scope': 'Evidence-backed fifth-batch digital completion; physical printing deferred; no publication.',
              'new_models': 31, 'collection_models': 67, 'totals': totals, 'models': rows}
    (ROOT / 'reports/batch5-completion.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'new_models': 31, 'collection_models': 67, **totals}))


if __name__ == '__main__':
    write()
