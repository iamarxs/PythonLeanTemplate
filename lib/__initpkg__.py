"""
Insert the project root dir into PYTHONPATH, then import from config to have everything else
set up for us.
"""
# pylint: disable=C0413,W0611
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if ROOT_DIR not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# An import from the top level. Slightly ugly because not instantly obvious where import is coming
# from.
from config import CONFIG  # noqa: E402,F401
