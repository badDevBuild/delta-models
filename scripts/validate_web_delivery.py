"""Check served download metadata and built copies of every registered model."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from urllib.request import Request, urlopen
from model_catalog import ROOT, MODEL_IDS


def validate(base_url):
    public = ROOT / 'web/public'
    built = ROOT / 'web/dist'
    catalog = json.loads((public / 'catalog.json').read_text())
    assert [m['id'] for m in catalog['models']] == MODEL_IDS
    jobs = []
    for model in catalog['models']:
        paths = {'model': model['model'], 'preview': model['preview'], **model['downloads']}
        assert set(paths) == {'model', 'preview', 'blend', 'print', 'sliced'}, model['id']
        jobs.extend((model['id'], kind, path) for kind, path in paths.items())

    def check(job):
        asset_id, kind, path = job
        source = public / path.lstrip('/')
        target = built / path.lstrip('/')
        expected = source.stat().st_size
        with urlopen(Request(base_url.rstrip('/') + path, method='HEAD'), timeout=30) as response:
            status = response.status
            received = int(response.headers['Content-Length'])
        assert status == 200 and received == expected, job
        digest = hashlib.sha256(source.read_bytes()).digest()
        assert hashlib.sha256(target.read_bytes()).digest() == digest, job
        return {'id': asset_id, 'kind': kind, 'url': path, 'status': status,
                'bytes': expected, 'built_asset_matches': True}

    with ThreadPoolExecutor(max_workers=4) as pool:
        checks = list(pool.map(check, jobs))
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'passed': True,
              'models': len(MODEL_IDS), 'resources': len(checks), 'checks': checks}
    report = ROOT / 'reports' / f'{len(MODEL_IDS)}-model-http-validation.json'
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': True, 'resources': len(checks), 'report': str(report)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:5174')
    validate(parser.parse_args().base_url)
