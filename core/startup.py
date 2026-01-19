import sys
import winreg

def add_to_startup(app_name="WinPet"):
  exe_path = sys.executable

  key = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    0,
    winreg.KEY_SET_VALUE
  )

  winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
  winreg.CloseKey(key)
