import os
from pystray import Menu, MenuItem

import core.config as config
from tray.utils import open_folder, save_config
from core.exceptions import UnsupportedOSException

def on_close(icon, item):
  save_config()
  icon.visible = False
  icon.stop()

def on_directory_open(icon, item):
  try:
    open_folder(config.LIBRARY_PATH)
  except UnsupportedOSException as e:
    print('Exception: Current OS does not support the operation')


def on_asset_click(icon, item):
  if item.text == config.ACTIVE_SEQUENCE_NAME:
    return

  config.ACTIVE_SEQUENCE_NAME = item.text
  config.ACTIVE_SEQUENCE_PATH = os.path.join(
    config.LIBRARY_PATH,
    item.text
  )
  save_config()

  icon.menu = build_menu()
  icon.title = f"WinPet – {config.ACTIVE_SEQUENCE_NAME}"

def on_reload_library(icon, item):
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

  asset_menu = [
    MenuItem(
      text=format_name(name),
      action=on_asset_click,
      checked=lambda item, name=name: name == config.ACTIVE_SEQUENCE_NAME,
      radio=True
    )
    for name in sorted(asset_dirs, key=str.lower)
  ]

  return Menu(
    MenuItem('Open Library Folder', on_directory_open),
    Menu.SEPARATOR,

    MenuItem(
      f'Current Look: {config.ACTIVE_SEQUENCE_NAME or "None"}',
      Menu(*asset_menu) if asset_menu else Menu(
        MenuItem('No Looks Available', None, enabled=False)
      )
    ),

    Menu.SEPARATOR,
    MenuItem(
      'Refresh Looks',
      on_reload_library,
      enabled=bool(asset_menu)
    ),
    Menu.SEPARATOR,
    MenuItem('Quit WinPet', on_close)
  )
