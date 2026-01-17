import os
import time
import threading
import core.config as config
from tray.tray_helpers import build_menu

CHECK_INTERVAL = 2.0


def get_library_snapshot():
  if not os.path.isdir(config.LIBRARY_PATH):
    return set()

  return {
    name
    for name in os.listdir(config.LIBRARY_PATH)
    if os.path.isdir(os.path.join(config.LIBRARY_PATH, name))
    and not name.startswith('.')
  }


def watch_library(icon):
  last_snapshot = get_library_snapshot()

  while True:
    time.sleep(CHECK_INTERVAL)
    current_snapshot = get_library_snapshot()

    if current_snapshot != last_snapshot:
      last_snapshot = current_snapshot

      from tray.utils import initialize_active_asset
      initialize_active_asset()

      icon.menu = build_menu()
