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

class History:
    def __init__(self):
        return

class Excel2FinalShell:
    def __init__(self, is_cached: bool, fold_name: str):
        self.manager = WindowManager()
        self.position = WindowPosition()
        self.is_cached = is_cached
        self.fold_name = fold_name
        self.ocr = OCR()
        self.history = None


    def single_task(self, config: excel_reader.Config):
        self.manager.call_window("连接管理器")

        is_finished = True
        if not self.is_cached or self.history is None:
            is_finished = False
            self.history = History()

            self.history.manager_box = get_windows_pos(self.manager.handle, self.position)
            self.history.manager_window_pos = self.history.manager_box.position()

            self.history.new_fold_pos = self.ocr.capture(self.history.manager_box).get_txt_pos(self.fold_name)

        moveTo(self.history.new_fold_pos.add(self.history.manager_window_pos).as_tuple())
        rightClick()

        if not self.is_cached or not is_finished:
            self.history.offset = ([0, 0, 0, self.position.handle_single_attr(self.history.new_fold_pos.y)])
            self.history.xinjian_pos = self.ocr.capture(
                self.history.manager_box.add_offset(self.history.offset)).get_txt_pos("新建")
            exit(-1)
        moveTo(self.history.xinjian_pos.add(self.history.manager_window_pos).as_tuple())
        sleep(0.2)
        if not self.is_cached or not is_finished:
            text_list = ["SSH连接(Linux)", "SSH连接（Linux)", "SSH连接(Linux）", "SSH连接（Linux）"]
            self.history.ssh_connect_pos = self.ocr.capture(
                self.history.manager_box.add_offset(self.history.offset)).get_txt_pos(text_list)
        moveTo(self.history.ssh_connect_pos.add(self.history.manager_window_pos).as_tuple())
        click()
        self.manager.unset_window_foreground()
        sleep(0.2)

        self.manager.call_window("新建连接")
        if not self.is_cached or not is_finished:
            self.history.connection_box = get_windows_pos(self.manager.handle, self.position)
            self.history.connection_window_pos = self.history.connection_box.position()
            self.history.fix_input_offset = Position(self.position.handle_single_attr(150), self.position.handle_single_attr(10))
            text_list = [["名称：", "名称", "名称:"], ["主机：", "主机", "主机:"], ["端口：", "端口", "端口:"],
                     ["用户名：", "用户名", "用户名:"], ["密码：", "密码", "密码:"], "确定"]
            self.history.pos_list = []
            is_find = False
            self.history.result_list = self.ocr.capture(self.history.connection_box).get_txt_list_pos(text_list)
            for (s, pos) in self.history.result_list:
                if len(text_list) + 1 == len(self.history.result_list) and s == "密码" and not is_find:
                    is_find = True
                    continue
                self.history.pos_list.append(pos.add(self.history.connection_window_pos))

            if len(self.history.pos_list) == len(text_list) + 1:
                self.history.pos_list.remove(("密码", any))
        pos = self.history.pos_list[0].add(self.history.fix_input_offset).as_tuple()
        click(x=pos[0], y=pos[1])
        write(config.name)

        pos = self.history.pos_list[1].add(self.history.fix_input_offset).as_tuple()
        click(x=pos[0], y=pos[1])
        write(config.host)

        pos = self.history.pos_list[2].add(self.history.fix_input_offset).as_tuple()
        click(x=pos[0], y=pos[1])
        write(str(config.port))

        pos = self.history.pos_list[3].add(self.history.fix_input_offset).as_tuple()
        click(x=pos[0], y=pos[1])
        write(config.username)

        pos = self.history.pos_list[4].add(self.history.fix_input_offset).as_tuple()
        click(x=pos[0], y=pos[1])
        write(config.password)

        pos = self.history.pos_list[5].as_tuple()
        click(x=pos[0], y=pos[1])


def start(path: str, is_cache: bool, fold_name: str):
    handle = Excel2FinalShell(is_cached=is_cache, fold_name=fold_name)
    reader = excel_reader.ExcelReader(path)
    while True:
        config = reader.read()
        if config is None:
            reader.close()
            return
        handle.single_task(config)

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout, QWidget, QLabel, \
    QCheckBox, QLineEdit
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

        self.folder_label = QLabel("添加到连接管理器的哪个文件夹内(需要能直接看到)：")
        self.layout.addWidget(self.folder_label)

        self.folder_input = QLineEdit()
        self.folder_input.setText("新建文件夹")  # 设置默认值
        self.layout.addWidget(self.folder_input)

        # 增加复选框，确定是否缓存位置信息
        self.cache_checkbox = QCheckBox("是否缓存位置信息")
        self.cache_checkbox.setChecked(True)
        self.layout.addWidget(self.cache_checkbox)

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
        start(self.excel_path,self.cache_checkbox.isChecked(),self.folder_input.text())

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
