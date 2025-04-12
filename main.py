from pyautogui import moveTo, rightClick, click, sleep, write

from utils.window_manager import WindowManager
from utils.window_position import WindowPosition
import win32gui
from utils import excel_reader
from utils.box import Position
from utils.ocr_utils import OCR


def get_windows_pos(_handle, window_position: WindowPosition):
    # 获取原始窗口坐标
    origin_window_rect = win32gui.GetWindowRect(_handle)

    # 根据缩放比修正窗口坐标
    return window_position.handle_rect(origin_window_rect)

def single_task(ocr: OCR, position: WindowPosition, config: excel_reader.Config):
    manager = WindowManager()

    manager.call_window("连接管理器")
    box = get_windows_pos(manager.handle, position)
    window_pos = box.position()

    pos = ocr.capture(box).get_txt_pos("新建文件夹")
    moveTo(pos.add(window_pos).as_tuple())
    rightClick()

    offset = ([0, 0, 0, position.handle_single_attr(150)])
    pos = ocr.capture(box.add_offset(offset)).get_txt_pos("新建")
    moveTo(pos.add(window_pos).as_tuple())

    sleep(0.2)
    text_list = ["SSH连接(Linux)", "SSH连接（Linux)","SSH连接(Linux）","SSH连接（Linux）"]
    pos = ocr.capture(box.add_offset(offset)).get_txt_one_of_list_pos(text_list)
    moveTo(pos.add(window_pos).as_tuple())
    click()

    manager.unset_window_foreground()
    sleep(0.2)

    manager.call_window("新建连接")
    box = get_windows_pos(manager.handle, position)
    window_pos = box.position()

    fix_input_offset = Position(position.handle_single_attr(150), position.handle_single_attr(10))

    text_list = ["名称：", "主机：", "端口：", "用户名：", "密码：", "确定"]
    pos_list = [p.add(window_pos) for p in ocr.capture(box).get_txt_list_pos(text_list)]
    pos = pos_list[0].add(fix_input_offset).as_tuple()
    click(x=pos[0],y=pos[1])
    write(config.name)

    pos = pos_list[1].add(fix_input_offset).as_tuple()
    click(x=pos[0],y=pos[1])
    write(config.host)

    pos = pos_list[2].add(fix_input_offset).as_tuple()
    click(x=pos[0],y=pos[1])
    write(str(config.port))

    pos = pos_list[3].add(fix_input_offset).as_tuple()
    click(x=pos[0],y=pos[1])
    write(config.username)

    pos = pos_list[4].add(fix_input_offset).as_tuple()
    click(x=pos[0],y=pos[1])
    write(config.password)

    pos = pos_list[5].as_tuple()
    click(x=pos[0],y=pos[1])


def start(path: str):
    ocr = OCR()
    position = WindowPosition()
    reader = excel_reader.ExcelReader(path)
    while True:
        config = reader.read()
        if config is None:
            reader.close()
            return
        single_task(ocr, position, config)

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt

class FileDragDropWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("批量导入ssh")
        self.setFixedSize(400, 300)  # 设置固定窗口大小

        # 用于存储拖入的文件路径
        self.excel_path = None

        # 创建中心部件与布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 提示标签
        self.label = QLabel("1.打开连接管理器，将excel文件拖入此窗口")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.label = QLabel("2.新建一个文件夹(不改名)，然后开始运行")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        # 显示文件列表的控件
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        # “开始运行”按钮
        self.start_button = QPushButton("开始运行")
        self.start_button.clicked.connect(self.start_running)
        self.layout.addWidget(self.start_button)

        # 开启拖拽功能
        self.setAcceptDrops(True)


    # 重写 dragEnterEvent 以接受拖入文件事件
    def dragEnterEvent(self, event):
        # 判断拖入的数据中是否包含文件（URL）
        if event.mimeData().hasUrls():
            event.acceptProposedAction()  # 接受拖入动作
        else:
            event.ignore()

    # 重写 dropEvent 处理释放拖入的文件
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            # 提取本地文件路径
            file_path = url.toLocalFile()
            # 避免重复添加相同文件，并检查文件路径非空
            if file_path:
                if not self.excel_path is None:
                    self.list_widget.clear()
                self.excel_path = file_path
                self.list_widget.addItem(file_path)

    # 点击“开始运行”按钮后执行的操作
    def start_running(self):
        # 示例逻辑：在控制台中打印拖入文件的列表
        start(self.excel_path)

        # 此处可以添加进一步处理拖入文件的逻辑

# 重写 keyPressEvent 方法监听键盘事件，检测 ESC 键
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            print("检测到 ESC 按键，程序将退出。")
            self.close()  # 关闭主窗口，退出程序
        else:
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileDragDropWindow()
    window.show()
    sys.exit(app.exec())
