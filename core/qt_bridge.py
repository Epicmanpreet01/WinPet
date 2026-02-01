from PySide6.QtCore import QObject, Signal

class QtBridge(QObject):
  fps_changed = Signal()
  companion_toggled = Signal()

qt_bridge = QtBridge()
