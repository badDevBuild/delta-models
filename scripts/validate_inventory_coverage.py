"""Compare the project registry with the dated, alias-deduplicated work roster.

This checks project coverage, not a claim of an officially confirmed game total.
"""
import csv
from datetime import datetime, timezone
import hashlib
import json

from model_catalog import MODELS, ROOT


def validate():
    source = ROOT.parent / 'm7-display/research/weapons-working-list-2026-09-22.csv'
    with source.open(encoding='utf-8-sig', newline='') as handle:
        roster = list(csv.DictReader(handle))
    aliases = {'SVCH（部分资料写 SVTH）': 'SVCH'}
    expected = [aliases.get(row['name'], row['name']) for row in roster]
    actual = [model['name'] for model in MODELS]
    assert len(expected) == len(set(expected)), 'Duplicate work-roster name'
    assert len(actual) == len(set(actual)), 'Duplicate registered display name'
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    report = {'checked_at': datetime.now(timezone.utc).isoformat(),
              'scope': 'Registered names cover the dated project work roster; no official total or artifact completeness claim.',
              'roster_file': str(source), 'roster_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'roster_count': len(expected), 'registered_count': len(actual),
              'aliases': aliases, 'missing': missing, 'unexpected': unexpected,
              'passed': not missing and not unexpected,
              'models': [{'name': m['name'], 'id': m['id'], 'batch': m['batch']} for m in MODELS]}
    output = ROOT / 'reports/inventory-coverage.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['passed', 'roster_count', 'registered_count', 'missing', 'unexpected']}, ensure_ascii=False))
    assert report['passed'], 'Inventory names do not match the agreed work roster'


if __name__ == '__main__':
    validate()
