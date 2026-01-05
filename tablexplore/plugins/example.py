"""
    示例插件（TableExplore）
    创建于 2021 年 1 月
    版权所有 (C) Damien Farrell

    本模块为插件开发示例，包含简单的文本框和表格示例。
"""

from __future__ import absolute_import, division, print_function
import inspect
import sys,os,platform,time,traceback
import pickle, gzip
from collections import OrderedDict
from tablexplore.qt import *
import pandas as pd
from tablexplore import util, core, dialogs
from tablexplore.plugin import Plugin

class ExamplePlugin(Plugin):
    """TableExplore 的示例插件模板"""

    #uncomment capabilities list to appear in menu
    capabilities = ['gui']
    requires = ['']
    menuentry = '示例插件'
    name = '示例插件'

    def __init__(self, parent=None, table=None):
        """为你的控件定制初始化逻辑或创建布局"""

        if parent==None:
            return
        self.parent = parent
        self.table = table
        self.createWidgets()
        return

    def _createMenuBar(self):
        """为应用创建菜单栏。"""

        return

    def createWidgets(self):
        """如果为 GUI 插件，创建界面控件"""

        self.main = QWidget()

        layout = self.layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.main.setLayout(layout)
        tb = self.textbox = dialogs.PlainTextEditor()
        tb.resize(300,300)
        layout.addWidget(tb)
        text = '这是一个示例插件。\n'\
        '有关更多示例代码，请参见 https://github.com/dmnfarrell/tablexplore/tree/master/plugins'
        tb.insertPlainText(text)
        #add a table widget
        t = self.tablewidget = core.DataFrameWidget(self.main, font=core.FONT,
                                    statusbar=False, toolbar=False)
        t.resize(300,300)
        layout.addWidget(self.tablewidget)
        #add some buttons
        bw = self.createButtons(self.main)
        layout.addWidget(bw)
        return

    def createButtons(self, parent):

        bw = QWidget(parent)
        vbox = QVBoxLayout(bw)
        button = QPushButton("关闭")
        button.clicked.connect(self.quit)
        vbox.addWidget(button)
        return bw

    def apply(self):
        """执行操作（自定义实现）"""

        return

    def quit(self, evt=None):
        """重写以处理面板关闭"""

        self.main.close()
        return

    def about(self):
        """关于此插件"""

        txt = "此插件实现了示例功能...\n"+\
               "版本: %s" % getattr(self, 'version', '未知')
        return txt
