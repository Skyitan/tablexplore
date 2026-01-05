#!/usr/bin/env python

"""
    TableExplore 应用程序
    创建于 2020 年 11 月
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

try:
    from PySide2.QtWidgets import *
except:
    from PyQt5.QtWidgets import *

from tablexplore import app

def main():
    import sys, os

    from argparse import ArgumentParser
    parser = ArgumentParser()
    #parser.add_argument("-f", "--file", dest="msgpack",
    #                    help="以 msgpack 格式打开 DataFrame", metavar="FILE")
    parser.add_argument("-p", "--project", dest="project_file",
                        help="打开 TableExplore 项目文件", metavar="FILE")
    parser.add_argument("-i", "--csv", dest="csv_file",
                        help="导入 CSV 文件", metavar="FILE")
    #parser.add_argument("-x", "--excel", dest="excel",
    #                    help="导入 Excel 文件", metavar="FILE")
    #parser.add_argument("-t", "--test", dest="test",  action="store_true",
    #                    default=False, help="运行一个基本测试应用")
    args, unknown = parser.parse_known_args()
    args = vars(args)
    qapp = QApplication(sys.argv)
    aw = app.Application(**args)
    aw.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
