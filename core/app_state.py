from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import QApplication

qt_app = None
is_quitting = False

def quit_app():
  app = QApplication.instance()
  if app is None:
    return

  QMetaObject.invokeMethod(
    app,
    "closeAllWindows",
    Qt.QueuedConnection
  )

  QMetaObject.invokeMethod(
    app,
    "quit",
    Qt.QueuedConnection
  )
