"""Lay out verified model renders for the local delivery overview."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from model_catalog import MODELS, ROOT


def write(batch):
    models = [m for m in MODELS if batch is None or m['batch'] == batch]
    evidence = {r['id']: r for r in json.loads((ROOT / 'reports/catalog-renders.json').read_text())}
    font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    assert Path(font_path).is_file(), 'Supply a Unicode font for this host'
    title_font = ImageFont.truetype(font_path, 35)
    label_font = ImageFont.truetype(font_path, 22)
    note_font = ImageFont.truetype(font_path, 17)
    cols, w, h, gap = 4, 360, 246, 16
    canvas = Image.new('RGB', (cols * (w + gap) + gap, 134 + math.ceil(len(models) / cols) * (h + gap)), '#111813')
    draw = ImageDraw.Draw(canvas)
    title = f'DELTA MODELS · {len(models)} 款' + (f' / 第 {batch} 批' if batch else ' / 全部收藏')
    draw.text((24, 20), title, font=title_font, fill='#d4dfad')
    draw.text((24, 79), '2026-09-22 工作清单 · 截图重建的微缩外观艺术模型 · 实机打印延后', font=note_font, fill='#bdc6be')
    for i, spec in enumerate(models):
        ident = spec['id']
        asset = ROOT / 'assets' / ident
        source = asset / 'source' / f'{ident}.blend'
        preview = asset / 'renders/catalog.png'
        digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        assert evidence[ident]['source_sha256'] == digest(source), ident
        assert evidence[ident]['preview_sha256'] == digest(preview), ident
        x, y = gap + (i % cols) * (w + gap), 122 + (i // cols) * (h + gap)
        draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill='#242e28')
        image = Image.open(preview).convert('RGB')
        image.thumbnail((w - 12, 202), Image.Resampling.LANCZOS)
        canvas.paste(image, (x + (w - image.width) // 2, y + 6))
        draw.text((x + 12, y + 211), spec['name'], font=label_font, fill='#edf1e8')
    suffix = f'batch{batch}' if batch is not None else 'collection'
    output = ROOT / 'output' / f'{suffix}-overview.jpg'
    canvas.save(output, quality=93, subsampling=0)
    print(json.dumps({'models': len(models), 'image': str(output), 'width': canvas.width, 'height': canvas.height}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=int)
    write(parser.parse_args().batch)
