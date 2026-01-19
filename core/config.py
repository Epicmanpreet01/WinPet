import os
import platform
import json
from PySide6.QtCore import QSize

APP_NAME = 'WinPet'

if platform.system() == 'Windows':
    BASE_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
else:
    BASE_DIR = os.path.join(os.path.expanduser('~'), f'.{APP_NAME.lower()}')

DATA_DIR = os.path.join(BASE_DIR, 'data')
LIBRARY_DIR = os.path.join(BASE_DIR, 'library')

CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LIBRARY_DIR, exist_ok=True)

data = {}

if os.path.isfile(CONFIG_FILE):
  try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
      content = f.read().strip()

      if content:
        data = json.loads(content)
      else:
        data = {}
  except (json.JSONDecodeError, OSError):
    data = {}

PLATFORM = platform.system()
LIBRARY_PATH = os.path.abspath(LIBRARY_DIR)

ACTIVE_SEQUENCE_NAME = (
  data.get('ACTIVE_SEQUENCE_NAME')
  if isinstance(data.get('ACTIVE_SEQUENCE_NAME'), str)
  else ''
)

ACTIVE_SEQUENCE_PATH = (
  data.get('ACTIVE_SEQUENCE_PATH')
  if isinstance(data.get('ACTIVE_SEQUENCE_PATH'), str)
  else ''
)

STANDARD_SIZE = QSize(256, 256)
FPS = 12
SEQUENCE_CHECK_INTERVAL_MS = 500
