import os
import time
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QPointF
import core.config as config
from companion.companion_utils import load_sequence_frames
from core.qt_bridge import qt_bridge


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

    # Animation State
    self.states = {}
    self.state = None
    self.current_frames = []
    self.frame_index = 0

    # Interaction State
    self.is_holding = False
    self._drag_offset = None
    self.last_mouse_pos = None

    now = time.time()
    self.last_interaction_time = now
    self.last_idle_phase_time = now

    self.IDLE_MEDIUM_AFTER = 10
    self.IDLE_LONG_AFTER = 20
    self.idle_long_runs = 0
    self.MAX_IDLE_LONG_RUNS = 3

    self.idle_long_active = False

    # Physics
    self.velocity = QPointF(0, 0)
    self.friction = 0.95
    self.bounce = 0.85

    self.current_sequence_path = None
    self.load_states()

    # Animation Timer
    self.anim_timer = QTimer(self)
    self.anim_timer.timeout.connect(self.advance_frame)
    self.anim_timer.start(int(1000 / config.FPS))

    # Sequence / Idle Watcher
    self.sequence_timer = QTimer(self)
    self.sequence_timer.timeout.connect(self.check_sequence_change)
    self.sequence_timer.start(config.SEQUENCE_CHECK_INTERVAL_MS)

    # Physics Loop
    self.physics_timer = QTimer(self)
    self.physics_timer.timeout.connect(self.update_physics)
    self.physics_timer.start(16)

    # Config Signals
    qt_bridge.size_changed.connect(self.on_size_changed)
    qt_bridge.fps_changed.connect(self.on_fps_changed)
    qt_bridge.companion_toggled.connect(self.on_companion_toggled)

  # State Management

  def load_states(self):
    self.states.clear()
    self.current_frames = []
    self.frame_index = 0

    base = config.ACTIVE_SEQUENCE_PATH
    if not base or not os.path.isdir(base):
      return

    for name in os.listdir(base):
      path = os.path.join(base, name)
      if not os.path.isdir(path):
        continue

      frames = load_sequence_frames(path)
      if frames:
        self.states[name] = frames

    if 'idle' not in self.states:
      self.states.clear()
      return
    self.idle_long_runs = 0
    self.idle_long_active = False
    self.last_idle_phase_time = time.time()

    self.change_state('idle', force=True)
    self.current_sequence_path = base

  def change_state(self, name, force=False):
    if not self.states:
      return

    if name not in self.states:
      name = 'idle'

    if not force and self.state == name:
      return

    self.state = name
    self.current_frames = self.states[name]
    self.frame_index = 0

  # Animation

  def advance_frame(self):
    if not self.current_frames:
      return

    self.label.setPixmap(self.current_frames[self.frame_index])
    self.frame_index = (self.frame_index + 1) % len(self.current_frames)

  # Input

  def mousePressEvent(self, event):
    if event.button() != Qt.LeftButton:
      return

    now = time.time()
    self.last_interaction_time = now
    self.last_idle_phase_time = now
    self.idle_long_runs = 0
    self.idle_long_active = False

    self.is_holding = True
    self.velocity = QPointF(0, 0)
    self.last_mouse_pos = event.globalPosition()
    self._drag_offset = (
      event.globalPosition().toPoint()
      - self.frameGeometry().topLeft()
    )

    self.change_state('picked')
    event.accept()

  def mouseMoveEvent(self, event):
    if not self.is_holding or not event.buttons() & Qt.LeftButton:
      return

    delta = event.globalPosition() - self.last_mouse_pos
    self.velocity = QPointF(delta.x(), delta.y())
    self.last_mouse_pos = event.globalPosition()

    self.move(event.globalPosition().toPoint() - self._drag_offset)
    event.accept()

  def mouseReleaseEvent(self, event):
    now = time.time()
    self.last_interaction_time = now
    self.last_idle_phase_time = now
    self.idle_long_runs = 0
    self.idle_long_active = False

    self.is_holding = False
    self._drag_offset = None
    self.change_state('idle')
    event.accept()

  # Idle Logic
  def update_idle_state(self):
    if self.is_holding or not self.states:
      return
    
    if self.idle_long_active:
      return


    now = time.time()
    idle_time = now - self.last_idle_phase_time
    if 'idle_long' in self.states:
      if not self.idle_long_active and idle_time >= self.IDLE_LONG_AFTER:
        self.change_state('idle_long')
        self.idle_long_active = True
        self.last_idle_phase_time = now
        return
      if self.idle_long_active and idle_time >= self.IDLE_LONG_AFTER:
        self.idle_long_runs += 1
        self.last_idle_phase_time = now

        if self.idle_long_runs >= self.MAX_IDLE_LONG_RUNS:
          self.idle_long_runs = 0
          self.idle_long_active = False
          self.change_state('idle')
        return

    if (
      not self.idle_long_active
      and idle_time >= self.IDLE_MEDIUM_AFTER
      and 'idle_medium' in self.states
    ):
      self.change_state('idle_medium')
      return

    self.change_state('idle')

  # Physics
  def update_physics(self):
    if self.is_holding:
      return

    self.move(self.pos() + self.velocity.toPoint())
    self.velocity *= self.friction

    if abs(self.velocity.x()) < 0.1:
      self.velocity.setX(0)
    if abs(self.velocity.y()) < 0.1:
      self.velocity.setY(0)

    screen = QApplication.primaryScreen().availableGeometry()
    x, y = self.x(), self.y()
    w, h = self.width(), self.height()

    if x <= screen.left() or x + w >= screen.right():
      self.velocity.setX(-self.velocity.x() * self.bounce)

    if y <= screen.top() or y + h >= screen.bottom():
      self.velocity.setY(-self.velocity.y() * self.bounce)

  # Config Hooks

  def check_sequence_change(self):
    if config.ACTIVE_SEQUENCE_PATH != self.current_sequence_path:
      self.load_states()

    self.update_idle_state()

  def on_size_changed(self):
    self.resize(config.STANDARD_SIZE)
    self.label.resize(config.STANDARD_SIZE)
    self.load_states()

  def on_fps_changed(self):
    self.anim_timer.start(int(1000 / config.FPS))

  def on_companion_toggled(self):
    self.setVisible(config.COMPANION_ENABLED)
