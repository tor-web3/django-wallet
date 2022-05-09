import sys,os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

INCLUDE_CODE_PATHS = [
    os.path.join(BASE_DIR / 'plugins'),
    os.path.join(BASE_DIR / 'libraries')
]

for path in INCLUDE_CODE_PATHS:
    sys.path.append(path)