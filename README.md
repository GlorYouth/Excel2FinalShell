# Excel2FinalShell
A script for automatically batch importing SSH configuration from Excel into Final Shell  
一个自动将excel中ssh配置批量导入finalshell的脚本  

## 使用方法

### 方法 1
去 Release 页下载最新的exe文件打开，然后拖入.xlsx，打开finalshell的连接管理器，保证“新建连接窗口”不会与“连接管理器”窗口重叠，然后点击程序的“开始运行”

### 方法 2
推荐python版本:3.11.11，也可以使用3.12.9  
拉取本仓库，使用```pip install -r requirements.txt```安装本仓库的依赖，然后```python .\main.py```即可

额外补充，若你想手动打包，你可以在方法2的基础上用如下方法，但python版本目前仅限于3.12以下，且不包括3.12
``` bash
pip install nuitka
nuitka --mingw64 --show-progress --standalone --plugin-enable=numpy  --plugin-enable=pyside6 --onefile --remove-output  --follow-imports  --disable-console main.py
```
