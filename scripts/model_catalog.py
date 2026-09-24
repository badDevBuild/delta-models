"""Single model registry shared by export, print validation and viewer delivery."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'config/models.json').read_text())
MODELS=CONFIG['models']
MODEL_IDS=[m['id'] for m in MODELS]
if len(set(MODEL_IDS))!=len(MODEL_IDS) or any(not re.fullmatch('[a-z][a-z0-9_]*',id) for id in MODEL_IDS):
    raise ValueError('Model registry IDs must be unique safe directory names')
