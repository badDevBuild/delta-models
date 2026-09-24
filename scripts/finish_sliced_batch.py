"""Finish a named set of frozen miniature assets, with one isolated slicer at a time.

This never sends a printer job. Existing current slice evidence can be reused;
missing or changed artist/geometry approvals fail before starting the slicer.
"""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from model_catalog import MODEL_IDS, ROOT
from package_sliced import package
from slicing_evidence import check_slicing
from audit_batch_packages import inspect


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight(asset_id):
    asset = ROOT / 'assets' / asset_id
    source = asset / 'source' / f'{asset_id}.blend'
    glb = asset / 'web' / f'{asset_id}.glb'
    source_hash, glb_hash = digest(source), digest(glb)
    review = json.loads((asset / 'visual-review.json').read_text())
    manifest = json.loads((asset / 'print/manifest.json').read_text())
    validation = json.loads((asset / 'print/validation.json').read_text())
    archive = json.loads((asset / 'print/archive-validation.json').read_text())
    assert review['passed'] and review['source_sha256'] == source_hash, asset_id
    assert review['glb_sha256'] == glb_hash, f'{asset_id}: changed visual export'
    assert manifest['source_sha256'] == source_hash and validation['passed'], asset_id
    assert validation['part_count'] == len(manifest['parts']), asset_id
    assert archive['zip_sha256'] == digest(asset / 'print' / f'{asset_id}-print.zip'), asset_id
    return source_hash, glb_hash


def finish(asset_ids):
    # The official CLI shares an isolated configuration directory across models.
    # An exclusive nonblocking lock prevents accidentally overlapping this runner.
    with (ROOT / 'reports/slicer-queue.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for asset_id in asset_ids:
            before = preflight(asset_id)
            asset = ROOT / 'assets' / asset_id
            print(json.dumps({'model': asset_id, 'stage': 'frozen-input-verified'}), flush=True)
            if not check_slicing(asset)['passed']:
                subprocess.run([sys.executable, str(ROOT / 'scripts/slice_with_bambu.py'), asset_id], check=True)
            package(asset_id)
            assert preflight(asset_id) == before, f'{asset_id}: model changed while finishing'
            evidence = inspect(asset_id)
            print(json.dumps({'model': asset_id, 'stage': 'sliced-and-archived',
                              'passed': evidence['passed'], 'pieces': evidence['pieces'],
                              'plates': evidence['plates']}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('assets', nargs='+', choices=MODEL_IDS)
    args = parser.parse_args()
    assert len(args.assets) == len(set(args.assets)), 'Duplicate models in one queue'
    assert 'm7' not in args.assets, 'M7 has a separately recorded custom layout'
    finish(args.assets)
