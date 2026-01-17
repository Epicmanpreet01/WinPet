import os
from pystray import Menu, MenuItem

import core.config as config
from tray.utils import open_folder, save_config
from core.exceptions import UnsupportedOSException

def on_close(icon, item):
  save_config()
  icon.stop()

def on_directory_open(icon, item):
  try:
    open_folder(config.LIBRARY_PATH)
  except UnsupportedOSException as e:
    print('Exception: Current OS does not support the operation')


def on_asset_click(icon, item):
  config.ACTIVE_SEQUENCE_NAME = item.text
  config.ACTIVE_SEQUENCE_PATH = os.path.join(config.LIBRARY_PATH, item.text)
  save_config()
  icon.menu = build_menu()
  icon.title = f"WinPet – {config.ACTIVE_SEQUENCE_NAME}"

def on_reload_library(icon, item):
  icon.menu = build_menu()

def build_menu():
  asset_menu = [
    MenuItem(
      text=name,
      action=on_asset_click,
      checked=lambda item, name=name: name == config.ACTIVE_SEQUENCE_NAME
    )
    for name in sorted(
      name for name in os.listdir(config.LIBRARY_PATH)
      if os.path.isdir(os.path.join(config.LIBRARY_PATH, name))
      and not name.startswith('.')
    ) 
  ]

  return Menu(
    MenuItem('Open Library', on_directory_open),
    MenuItem(
      f'Current Look: {config.ACTIVE_SEQUENCE_NAME or "None"}',
      Menu(*asset_menu)
    ) if len(asset_menu) > 0 else MenuItem(
      'No looks found', None, enabled=False
    ),
    MenuItem('Reload Library', action=on_reload_library),
    MenuItem('Close', on_close)
  )
