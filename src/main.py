import sys
from PySide6 import QtWidgets
from datetime import datetime
from ui import AppUI
from handler import SaveHandlerThread, HideHandlerThread

sys_app = QtWidgets.QApplication(sys.argv)
app_ui = AppUI()
last_filename = None

def handler_selection(is_secret):
  global last_filename
  if not is_secret:
    last_filename = f'outputs/{datetime.now().strftime("%Y%m%d_%H%M%S%f")}.avi'
  return HideHandlerThread(last_filename) if is_secret else SaveHandlerThread(last_filename)

app_ui.on('capture', handler_selection)
app_ui.show()

sys.exit(sys_app.exec())

