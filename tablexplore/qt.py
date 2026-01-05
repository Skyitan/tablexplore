
"""
    Qt 导入与兼容层
    创建于 2021 年 1 月

    该文件根据系统上可用的 Qt 绑定（PySide2 或 PyQt5）选择合适的导入，并导出常用 Qt 名称。
"""

# 根据系统上可用的 Qt 库选择导入（PySide2 优先，否则使用 PyQt5）
# 使用通配符导入是为了在其它模块中更方便地使用 Qt 类

import sys

try:
    from PySide2 import QtCore
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import QObject, Signal, Slot
except:
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
