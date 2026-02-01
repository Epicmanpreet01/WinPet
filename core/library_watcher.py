import os
import time
import core.config as config
from tray.tray_helpers import build_menu
from tray.sequence_utils import is_valid_sequence
import core.app_state as app_state

CHECK_INTERVAL = 2.0


def get_library_snapshot():
  if not os.path.isdir(config.LIBRARY_PATH):
    return set()

  snapshot = set()

  for name in os.listdir(config.LIBRARY_PATH):
    base = os.path.join(config.LIBRARY_PATH, name)
    if not os.path.isdir(base):
      continue

    snapshot.add((
      name,
      is_valid_sequence(base)
    ))

  return snapshot


def watch_library(icon):
  last_snapshot = get_library_snapshot()

  while icon.visible and not app_state.is_quitting:
    time.sleep(CHECK_INTERVAL)
    current_snapshot = get_library_snapshot()

    if current_snapshot != last_snapshot:
      last_snapshot = current_snapshot

      from tray.utils import initialize_active_asset
      initialize_active_asset()

      icon.menu = build_menu()
      icon.visible = False
      icon.visible = True
