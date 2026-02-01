from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QSize
import os

import core.config as config
from companion.companion_utils import load_sequence_frames
from tray.utils import save_config
from core.qt_bridge import qt_bridge


class Companion(QWidget):
  MIN_SIZE = 64
  MAX_SIZE = 512
  WHEEL_SCALE_STEP = 1.1

  def __init__(self):
    super().__init__()

    self.setWindowFlags(
      Qt.WindowType.Tool
      | Qt.WindowType.WindowStaysOnTopHint
      | Qt.WindowType.FramelessWindowHint
    )
    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    self.label = QLabel(self)
    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.resize(config.STANDARD_SIZE)
    self.label.resize(self.size())

    self.state = 'idle'
    self.current_frames = []
    self.frame_index = 0

    self.is_holding = False
    self._drag_offset = None

    self._scaled_cache = {}
    self._last_scaled_size = None

    self.current_sequence_path = None
    self.reload_sequence()

    self.anim_timer = QTimer(self)
    self.anim_timer.timeout.connect(self.advance_frame)
    self.anim_timer.start(int(1000 / config.FPS))

    self.sequence_timer = QTimer(self)
    self.sequence_timer.timeout.connect(self.check_sequence_change)
    self.sequence_timer.start(config.SEQUENCE_CHECK_INTERVAL_MS)

    qt_bridge.fps_changed.connect(self.on_fps_changed)
    qt_bridge.companion_toggled.connect(self.on_companion_toggled)

    self.setVisible(config.COMPANION_ENABLED)

  def on_fps_changed(self):
    self.anim_timer.start(int(1000 / config.FPS))

  def on_companion_toggled(self):
    self.setVisible(config.COMPANION_ENABLED)

  def advance_frame(self):
    if not self.current_frames:
      return

    target_size = self.label.size()

    if self._last_scaled_size != target_size:
      self._scaled_cache.clear()
      self._last_scaled_size = target_size

    if self.frame_index not in self._scaled_cache:
      original = self.current_frames[self.frame_index]
      self._scaled_cache[self.frame_index] = original.scaled(
        target_size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
      )

    self.label.setPixmap(self._scaled_cache[self.frame_index])
    self.frame_index = (self.frame_index + 1) % len(self.current_frames)

  def resizeEvent(self, event):
    self.label.resize(self.size())
    super().resizeEvent(event)

  def wheelEvent(self, event):
    delta = event.angleDelta().y()
    if delta == 0:
      return

    factor = self.WHEEL_SCALE_STEP if delta > 0 else 1 / self.WHEEL_SCALE_STEP
    self.apply_size(int(self.width() * factor))
    event.accept()

  def apply_size(self, size: int):
    size = max(self.MIN_SIZE, min(self.MAX_SIZE, size))
    if size == self.width():
      return

    self.resize(QSize(size, size))
    self._scaled_cache.clear()
    self._last_scaled_size = None

    config.SIZE = size
    config.STANDARD_SIZE = QSize(size, size)
    save_config()

  def reload_sequence(self):
    base = config.ACTIVE_SEQUENCE_PATH
    if not base or not os.path.isdir(base):
      self.current_frames = []
      return

    self.idle_frames = load_sequence_frames(os.path.join(base, 'idle'))
    self.picked_frames = load_sequence_frames(os.path.join(base, 'picked'))

    self._scaled_cache.clear()
    self._last_scaled_size = None

    self.set_idle()
    self.current_sequence_path = base

  def check_sequence_change(self):
    if config.ACTIVE_SEQUENCE_PATH != self.current_sequence_path:
      self.reload_sequence()

  def set_idle(self):
    self.state = 'idle'
    self.current_frames = self.idle_frames
    self.frame_index = 0

  def set_picked(self):
    self.state = 'picked'
    self.current_frames = self.picked_frames
    self.frame_index = 0

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.is_holding = True
      self._drag_offset = (
        event.globalPosition().toPoint()
        - self.frameGeometry().topLeft()
      )
      self.set_picked()
      event.accept()

  def mouseMoveEvent(self, event):
    if self.is_holding and event.buttons() & Qt.LeftButton:
      self.move(event.globalPosition().toPoint() - self._drag_offset)
      event.accept()

  def mouseReleaseEvent(self, event):
    self.is_holding = False
    self.set_idle()
    self._drag_offset = None
    event.accept()
