import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_compact_helpers import build_pistol
result=build_pistol('pistol93r',90,'beretta')
