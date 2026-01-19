import os
import sys
import winshell
from win32com.client import Dispatch

def add_to_startup(app_name="WinPet"):
  startup_dir = winshell.startup()
  exe_path = sys.executable

  shortcut_path = os.path.join(startup_dir, f"{app_name}.lnk")

  if os.path.exists(shortcut_path):
    return

  shell = Dispatch('WScript.Shell')
  shortcut = shell.CreateShortCut(shortcut_path)
  shortcut.Targetpath = exe_path
  shortcut.WorkingDirectory = os.path.dirname(exe_path)
  shortcut.save()
