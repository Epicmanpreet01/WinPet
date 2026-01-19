from pystray import Icon
import threading
from PySide6.QtWidgets import QApplication
import sys

from tray.utils import load_icon, initialize_active_asset
from tray.tray_helpers import build_menu
import core.config as config
from core.library_watcher import watch_library
from companion.companion_window import Companion
import core.app_state as app_state
from core.startup import add_to_startup
from tray.utils import save_config


if __name__ == '__main__':
  initialize_active_asset()
  if not config.STARTUP_ENABLED:
    try:
      add_to_startup()
      config.STARTUP_ENABLED = True
      save_config()
    except Exception:
      pass

  icon = Icon(
    name='WinPet',
    icon=load_icon('assets/icon.ico'),
    title="WinPet",
    menu=build_menu()
  )

  watcher_thread = threading.Thread(
    target=watch_library,
    args=(icon,),
    daemon=True
  )
  watcher_thread.start()

  icon.run_detached()

  app = QApplication(sys.argv)

  app_state.qt_app = app

  window = Companion()
  window.show()

  sys.exit(app.exec())

