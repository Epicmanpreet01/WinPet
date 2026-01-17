import os
import time
import threading
import core.config as config
from tray.tray_helpers import build_menu

CHECK_INTERVAL = 2.0


def get_library_snapshot():
  if not os.path.isdir(config.LIBRARY_PATH):
    return set()

  snapshot = set()

  for name in os.listdir(config.LIBRARY_PATH):
    base = os.path.join(config.LIBRARY_PATH, name)
    if not os.path.isdir(base) or name.startswith('.'):
      continue

    snapshot.add((
      name,
      os.path.isdir(os.path.join(base, 'idle')),
      os.path.isdir(os.path.join(base, 'picked'))
    ))

  return snapshot


def watch_library(icon):
  last_snapshot = get_library_snapshot()

  while icon.visible:
    time.sleep(CHECK_INTERVAL)
    current_snapshot = get_library_snapshot()

    if current_snapshot != last_snapshot:
      last_snapshot = current_snapshot

      from tray.utils import initialize_active_asset
      initialize_active_asset()

      icon.menu = build_menu()
