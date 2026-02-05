import os
from pystray import Menu, MenuItem
from PySide6.QtCore import QSize

import core.config as config
from tray.utils import open_folder, save_config
from tray.sequence_utils import is_valid_sequence
from core.exceptions import UnsupportedOSException
import core.app_state as app_state
from core.qt_bridge import qt_bridge

FPS_OPTIONS = [12, 24, 30, 60]
SIZE_OPTIONS = [128, 192, 256, 320, 384, 448]

def on_size_change(icon, item):
  size = int(item.text)

  if config.SIZE == size:
    return

  config.SIZE = size
  config.STANDARD_SIZE = QSize(size, size)
  save_config()

  qt_bridge.size_changed.emit()


def format_name(name, max_len=20):
  return name if len(name) <= max_len else name[:17] + '...'

def on_close(icon, item):
  app_state.is_quitting = True
  try:
    save_config()
  except Exception:
    pass

  try:
    icon.visible = False
    icon.stop()
  except Exception:
    pass

  try:
    app_state.quit_app()
  except Exception:
    pass

  import os
  os._exit(0)

def on_fps_change(icon, item):
  config.FPS = int(item.text)
  save_config()
  qt_bridge.fps_changed.emit()


def on_toggle_companion(icon, item):
  config.COMPANION_ENABLED = not config.COMPANION_ENABLED
  save_config()
  qt_bridge.companion_toggled.emit()

def on_directory_open(icon, item):
  try:
    open_folder(config.LIBRARY_PATH)
  except UnsupportedOSException:
    pass

def on_asset_click(icon, item):
  real_name = next(
    name for name in os.listdir(config.LIBRARY_PATH)
    if format_name(name) == item.text
  )

  base = os.path.join(config.LIBRARY_PATH, real_name)

  if not is_valid_sequence(base):
    return

  if real_name == config.ACTIVE_SEQUENCE_NAME:
    return

  config.ACTIVE_SEQUENCE_NAME = real_name
  config.ACTIVE_SEQUENCE_PATH = base
  save_config()

  icon.menu = build_menu()
  icon.visible = False
  icon.visible = True

def on_reload_library(icon, item):
  from tray.utils import initialize_active_asset
  initialize_active_asset()

  icon.menu = build_menu()
  icon.visible = False
  icon.visible = True

def build_menu():
  asset_dirs = [
    name for name in os.listdir(config.LIBRARY_PATH)
    if os.path.isdir(os.path.join(config.LIBRARY_PATH, name))
    and not name.startswith('.')
  ] if os.path.isdir(config.LIBRARY_PATH) else []

  asset_menu = []

  for name in sorted(asset_dirs, key=str.lower):
    base = os.path.join(config.LIBRARY_PATH, name)
    valid = is_valid_sequence(base)

    asset_menu.append(
      MenuItem(
        text=format_name(name),
        action=on_asset_click,
        checked=lambda item, real=name: real == config.ACTIVE_SEQUENCE_NAME,
        radio=True,
        enabled=valid
      )
    )

    fps_menu = Menu(
      *[
        MenuItem(
          text=str(fps),
          action=on_fps_change,
          checked=lambda item, f=fps: config.FPS == f,
          radio=True
        )
        for fps in FPS_OPTIONS
      ]
    )

    size_menu = Menu(
      *[
        MenuItem(
          text=str(size),
          action=on_size_change,
          checked=lambda item, s=size: config.SIZE == s,
          radio=True
        )
        for size in SIZE_OPTIONS
      ]
    )

  return Menu(
    MenuItem('Open Library Folder', on_directory_open),
    Menu.SEPARATOR,

    MenuItem(
      'Companion Enabled',
      on_toggle_companion,
      checked=lambda item: config.COMPANION_ENABLED
    ),

    MenuItem('Animation FPS', fps_menu),
    MenuItem('Companion Size', size_menu),

    Menu.SEPARATOR,
    MenuItem(
      'Current Look',
      Menu(*asset_menu) if asset_menu else Menu(
        MenuItem('No Looks Found', None, enabled=False)
      )
    ),

    Menu.SEPARATOR,
    MenuItem('Refresh Looks', on_reload_library),
    Menu.SEPARATOR,
    MenuItem('Quit WinPet', on_close)
  )