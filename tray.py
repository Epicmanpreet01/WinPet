from pystray import Icon
import threading
from PySide6.QtWidgets import QApplication
import sys

from tray.utils import create_image, initialize_active_asset
from tray.tray_helpers import build_menu

import core.config as config
from core.library_watcher import watch_library
from companion.companion_window import Companion

if __name__ == '__main__':
  initialize_active_asset()
  title = (
      f"WinPet – {config.ACTIVE_SEQUENCE_NAME}"
      if config.ACTIVE_SEQUENCE_NAME
      else "WinPet"
  )
  icon = Icon(
    name='WinPet',
    icon=create_image(60, 60, 'black', 'white'),
    title=title,
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
  app.setQuitOnLastWindowClosed(False)

  window = Companion()
  window.show()

  sys.exit(app.exec())
  
  