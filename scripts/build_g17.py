import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from remaining_pistol_helpers import build_pistol
result=build_pistol('g17',80,'g17')
