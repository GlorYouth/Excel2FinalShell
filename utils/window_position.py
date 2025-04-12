import win32api
import win32con
import win32gui
import win32print
from utils import box


class WindowPosition:
    def __init__(self):
        # 获取屏幕设备上下文
        hDC = win32gui.GetDC(0)

        # 获取屏幕的真实宽度和缩放后的宽度
        real_w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        apparent_w = win32api.GetSystemMetrics(0)

        # 计算缩放比
        self.scale_radio = real_w / apparent_w

    def handle_rect(self, rect: list):
        return box.Box([int(item * self.scale_radio) for item in rect])

    def handle_single_attr(self, i: int):
        return int(i * self.scale_radio)