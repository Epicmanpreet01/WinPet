import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer
import core.config as config
from companion.companion_utils import load_sequence_frames


class Companion(QWidget):
  def __init__(self):
    super().__init__()

    self.setWindowFlags(
      Qt.WindowType.Tool
      | Qt.WindowType.WindowStaysOnTopHint
      | Qt.WindowType.FramelessWindowHint
    )
    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    self.label = QLabel(self)
    self.label.resize(config.STANDARD_SIZE)
    self.label.move(0, 0)
    self.resize(config.STANDARD_SIZE)

    self.state = 'idle'
    self.current_frames = []
    self.frame_index = 0
    self.is_holding = False
    self._drag_offset = None

    self.current_sequence_path = None
    self.reload_sequence()

    self.anim_timer = QTimer(self)
    self.anim_timer.timeout.connect(self.advance_frame)
    self.anim_timer.start(int(1000 / config.FPS))

    self.sequence_timer = QTimer(self)
    self.sequence_timer.timeout.connect(self.check_sequence_change)
    self.sequence_timer.start(config.SEQUENCE_CHECK_INTERVAL_MS)

  def reload_sequence(self):
    base = config.ACTIVE_SEQUENCE_PATH

    if not base or not os.path.isdir(base):
      self.idle_frames = []
      self.picked_frames = []
      self.current_frames = []
      self.frame_index = 0
      return

    self.idle_frames = load_sequence_frames(os.path.join(base, 'idle'))
    self.picked_frames = load_sequence_frames(os.path.join(base, 'picked'))

    self.set_idle()
    self.current_sequence_path = base

  def check_sequence_change(self):
    if config.ACTIVE_SEQUENCE_PATH != self.current_sequence_path:
      self.reload_sequence()

  def advance_frame(self):
    if not self.current_frames:
      return

    self.label.setPixmap(self.current_frames[self.frame_index])
    self.frame_index += 1

    if self.frame_index >= len(self.current_frames):
      self.frame_index = 0

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


if __name__ == '__main__':
  app = QApplication(sys.argv)
  app.setQuitOnLastWindowClosed(False)

  window = Companion()
  window.show()

  sys.exit(app.exec())
