from PIL import Image, ImageDraw
import json
import os

import core.config as config
from core.exceptions import UnsupportedOSException
from tray.sequence_utils import is_valid_sequence
from core.utils import resource_path


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

def load_icon(path):
  real_path = resource_path(path)

  if not os.path.exists(real_path):
    return create_image(60, 60, 'black', 'white')

  image = Image.open(real_path).resize((60, 60))
  return image

def initialize_active_asset():
  if not os.path.isdir(config.LIBRARY_PATH):
    config.ACTIVE_SEQUENCE_NAME = ''
    config.ACTIVE_SEQUENCE_PATH = ''
    return

  valid_sequences = []

  for name in os.listdir(config.LIBRARY_PATH):
    base = os.path.join(config.LIBRARY_PATH, name)
    if is_valid_sequence(base):
      valid_sequences.append(name)

  valid_sequences.sort(key=str.lower)

  if not valid_sequences:
    config.ACTIVE_SEQUENCE_NAME = ''
    config.ACTIVE_SEQUENCE_PATH = ''
    return

  if config.ACTIVE_SEQUENCE_NAME in valid_sequences:
    config.ACTIVE_SEQUENCE_PATH = os.path.join(
      config.LIBRARY_PATH,
      config.ACTIVE_SEQUENCE_NAME
    )
    return

  config.ACTIVE_SEQUENCE_NAME = valid_sequences[0]
  config.ACTIVE_SEQUENCE_PATH = os.path.join(
    config.LIBRARY_PATH,
    valid_sequences[0]
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
