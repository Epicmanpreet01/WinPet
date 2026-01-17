import os
from pystray import Menu, MenuItem

import core.config as config
from tray.utils import open_folder, save_config
from tray.sequence_utils import is_valid_sequence
from core.exceptions import UnsupportedOSException


def on_close(icon, item):
  save_config()
  icon.visible = False
  icon.stop()


def on_directory_open(icon, item):
  try:
    open_folder(config.LIBRARY_PATH)
  except UnsupportedOSException:
    pass


def on_asset_click(icon, item):
  base = os.path.join(config.LIBRARY_PATH, item.text)

  if not is_valid_sequence(base):
    return

  if item.text == config.ACTIVE_SEQUENCE_NAME:
    return

  config.ACTIVE_SEQUENCE_NAME = item.text
  config.ACTIVE_SEQUENCE_PATH = base
  save_config()

  icon.menu = build_menu()
  icon.title = f"WinPet – {config.ACTIVE_SEQUENCE_NAME}"


def on_reload_library(icon, item):
  from tray.utils import initialize_active_asset
  initialize_active_asset()

  icon.menu = build_menu()
  icon.visible = False
  icon.visible = True


def build_menu():
  def format_name(name, max_len=20):
    return name if len(name) <= max_len else name[:17] + '...'

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
        checked=lambda item, name=name: name == config.ACTIVE_SEQUENCE_NAME,
        radio=True,
        enabled=valid
      )
    )

  return Menu(
    MenuItem('Open Library Folder', on_directory_open),
    Menu.SEPARATOR,
    MenuItem(
      f'Current Look: {config.ACTIVE_SEQUENCE_NAME or "None"}',
      Menu(*asset_menu) if asset_menu else Menu(
        MenuItem('No Looks Found', None, enabled=False)
      )
    ),
    Menu.SEPARATOR,
    MenuItem('Refresh Looks', on_reload_library, enabled=True),
    Menu.SEPARATOR,
    MenuItem('Quit WinPet', on_close)
  )
