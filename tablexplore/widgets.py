#!/usr/bin/env python
"""
    为 tablexplore 实现各种小部件
    创建于 2021 年 10 月
    版权所有 (C) Damien Farrell

    本程序为自由软件；您可以在 GNU 通用公共许可证（第3版或更高版本）
    的条款下重新分发和/或修改它。

    本程序是希望有用，但不提供任何担保；甚至不包含对适销性或适合于特定用途的暗示性担保。
    有关详细信息，请参阅 GNU 通用公共许可证。
"""

from __future__ import absolute_import, division, print_function
import os, types, io
import string, copy
from collections import OrderedDict
import pandas as pd
import pylab as plt
from .qt import *
from . import util, core, plotting, dialogs

module_path = os.path.dirname(os.path.abspath(__file__))
iconpath = os.path.join(module_path, 'icons')
homepath = os.path.expanduser("~")

style = '''
    QLabel {
        font-size: 10px;
    }
    QWidget {
        max-width: 250px;
        min-width: 60px;
        font-size: 14px;
    }
    QPlainTextEdit {
        max-height: 80px;
    }
'''

class ScratchPad(QWidget):
    """用于临时存储绘图和其他项目的小部件。
    目前支持存储文本、matplotlib 图形和 pandas DataFrame。"""
    def __init__(self, parent=None):
        super(ScratchPad, self).__init__(parent)
        self.parent = parent
        self.setMinimumSize(400,300)
        self.setGeometry(QtCore.QRect(300, 200, 800, 600))
        self.setWindowTitle("草稿板")
        self.createWidgets()
        sizepolicy = QSizePolicy()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # 存储对象的字典，这些对象应当可序列化
        self.items = {}
        return

    def createWidgets(self):
        """创建控件：左侧为标签页，右侧用于工具（草稿板内部布局）。"""

        self.main = QTabWidget(self)
        self.main.setTabsClosable(True)
        self.main.tabCloseRequested.connect(lambda index: self.remove(index))
        layout = QVBoxLayout(self)
        toolbar = QToolBar("工具栏")
        layout.addWidget(toolbar)
        items = {
            '新建文本': {'action': self.newText, 'file': 'document-new'},
            '保存': {'action': self.save, 'file': 'save'},
            '全部保存': {'action': self.saveAll, 'file': 'save-all'},
            '清除': {'action': self.clear, 'file': 'clear'},
        }
        for name in items:
            item = items[name]
            if 'file' in item:
                iconfile = os.path.join(iconpath, item['file'] + '.png')
                icon = QIcon(iconfile)
            else:
                icon = QIcon.fromTheme(item.get('icon', ''))
            btn = QAction(icon, name, self)
            btn.triggered.connect(item['action'])
            toolbar.addAction(btn)
        layout.addWidget(self.main)
        return

    def update(self, items):
        """显示存储对象的字典"""

        self.main.clear()
        for name in items:
            obj = items[name]
            #print (name,type(obj))
            if type(obj) is str:
                te = dialogs.PlainTextEditor()
                te.setPlainText(obj)
                self.main.addTab(te, name)
            elif type(obj) is pd.DataFrame:
                tw = core.DataFrameTable(self.main, dataframe=obj)
                self.main.addTab(tw, name)
            else:
                pw = plotting.PlotWidget(self.main)
                self.main.addTab(pw, name)
                pw.figure = obj
                pw.draw()
                plt.tight_layout()
        self.items = items
        return

    def remove(self, idx):
        """移除选中的标签页和对应对象"""

        index = self.main.currentIndex()
        name = self.main.tabText(index)
        del self.items[name]
        self.main.removeTab(index)
        return

    def save(self):
        """保存所选项目（图形）"""

        index = self.main.currentIndex()
        name = self.main.tabText(index)
        suff = "PNG 文件 (*.png);;JPG 文件 (*.jpg);;PDF 文件 (*.pdf);;所有文件 (*.*)"
        filename, _ = QFileDialog.getSaveFileName(self, "保存图片", name, suff)
        if not filename:
            return

        fig = self.items[name]
        fig.savefig(filename+'.png', dpi=core.DPI)
        return

    def saveAll(self):
        """将所有图形保存到指定文件夹"""

        dir =  QFileDialog.getExistingDirectory(self, "保存文件夹",
                                             homepath, QFileDialog.ShowDirsOnly)
        if not dir:
            return
        for name in self.items:
            fig = self.items[name]
            fig.savefig(os.path.join(dir,name+'.png'), dpi=core.DPI)
        return

    def clear(self):
        """清除所有图形"""

        self.items.clear()
        self.main.clear()
        return

    def newText(self):
        """新增文本编辑器"""

        name, ok = QInputDialog.getText(self, '名称', '名称：',
                    QLineEdit.Normal, '')
        if ok:
            tw = dialogs.PlainTextEditor()
            self.main.addTab(tw, name)
            self.items[name] = tw.toPlainText()
        return

    def closeEvent(self, event):
        """关闭"""

        for idx in range(self.main.count()):
            name = self.main.tabText(idx)
            #print (name)
            w = self.main.widget(idx)
            #print (w)
            if type(w) == dialogs.PlainTextEditor:
                self.items[name] = w.toPlainText()
        return
