from PIL import Image, ImageDraw
import json
import os

import core.config as config
from core.exceptions import UnsupportedOSException


def open_folder(folder):
  if not os.path.isdir(folder):
    return
  if config.PLATFORM == 'Windows':
    os.startfile(folder)
  elif config.PLATFORM == 'Darwin':
    os.system(f'open "{folder}"')
  elif config.PLATFORM == 'Linux':
    os.system(f'xdg-open "{folder}"')
  else:
    raise UnsupportedOSException('Unsupported OS')
  
def create_image(width, height, col1, col2):
  image = Image.new('RGB', (width, height), color=col1)
  draw = ImageDraw.Draw(image)
  draw.rectangle((width // 2, 0, width, height), fill=col2)
  draw.rectangle((0, height // 2, width, height), fill=col2)
  return image

def initialize_active_asset():
  def is_valid_sequence(name):
    base = os.path.join(config.LIBRARY_PATH, name)
    return (
      os.path.isdir(base)
      and os.path.isdir(os.path.join(base, 'idle'))
      and os.path.isdir(os.path.join(base, 'picked'))
    )

  if not os.path.isdir(config.LIBRARY_PATH):
    config.ACTIVE_SEQUENCE_NAME = ''
    config.ACTIVE_SEQUENCE_PATH = ''
    return

  assets = sorted(
    [
      name for name in os.listdir(config.LIBRARY_PATH)
      if is_valid_sequence(name)
    ],
    key=str.lower
  )

  if not assets:
    config.ACTIVE_SEQUENCE_NAME = ''
    config.ACTIVE_SEQUENCE_PATH = ''
    return

  if config.ACTIVE_SEQUENCE_NAME in assets:
    config.ACTIVE_SEQUENCE_PATH = os.path.join(
      config.LIBRARY_PATH,
      config.ACTIVE_SEQUENCE_NAME
    )
    return

  config.ACTIVE_SEQUENCE_NAME = assets[0]
  config.ACTIVE_SEQUENCE_PATH = os.path.join(
    config.LIBRARY_PATH,
    assets[0]
  )

def save_config():
  tmp_file = 'data/config.json.tmp'
  with open(tmp_file, 'w', encoding='utf-8') as f:
    json.dump(
      {
        'ACTIVE_SEQUENCE_NAME': config.ACTIVE_SEQUENCE_NAME,
        'ACTIVE_SEQUENCE_PATH': config.ACTIVE_SEQUENCE_PATH
      },
      f,
      indent=2
    )
  os.replace(tmp_file, 'data/config.json')
