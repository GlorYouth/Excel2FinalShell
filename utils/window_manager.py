import re
from time import sleep

import win32con
import win32gui

class __FindHandler:
    def __init__(self, pattern):
        self.pattern = pattern
        self.result = None

    def search_patten(self, hwnd):
        if re.search(self.pattern, win32gui.GetWindowText(hwnd)) and self.result is None:
            self.result = hwnd


def _find_window_by_title(pattern):
    handler = __FindHandler(pattern)
    win32gui.EnumWindows(lambda hwnd,_handler: handler.search_patten(hwnd), handler)
    if handler.result is not None:
        return handler.result
    return None

class WindowManager:
    def __init__(self):
        self.handle = None

    def call_window(self,title: str):
        _handle_and_name = _find_window_by_title(title)
        if _handle_and_name:
            handle = _handle_and_name
        else:
            exit("can't find window")
        win32gui.ShowWindow(handle, 4)
        win32gui.SetForegroundWindow(handle)
        self.handle = handle
        sleep(0.25)




    def unset_window_foreground(self):
        win32gui.SetWindowPos(self.handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)







