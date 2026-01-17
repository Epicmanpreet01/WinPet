from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

import core.config as config

def load_sequence_frames(path):
  frames = []

  for name in sorted(os.listdir(path), key=lambda n: int(os.path.splitext(n)[0])):
    full = os.path.join(path, name)
    pixmap = QPixmap(full).scaled(
      config.STANDARD_SIZE,
      Qt.KeepAspectRatio,
      Qt.SmoothTransformation
    )
    frames.append(pixmap)

  return frames