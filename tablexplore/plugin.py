#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    插件基类与插件系统工具
    创建于 2021 年 1 月

    提供插件基类 `Plugin` 以及帮助发现、加载和管理插件的工具函数。
"""

from __future__ import absolute_import, division, print_function
import inspect
import sys,os,platform,time,traceback
import pickle, gzip
import shutil
from collections import OrderedDict
from .qt import *
import pandas as pd
from .plotting import PlotViewer
from . import util

homepath = os.path.expanduser("~")
module_path = os.path.dirname(os.path.abspath(__file__))
stylepath = os.path.join(module_path, 'styles')
iconpath = os.path.join(module_path, 'icons')

class Plugin(object):
    """插件基类：其它插件应继承此类并实现 `createWidgets` 等方法。"""

    #capabilities can be 'gui', 'docked'
    capabilities = []
    requires = []
    menuentry = ''

    def __init__(self, parent=None):
        self.parent = parent
        return

    def main(self, parent=None):
        if parent==None:
            return
        self.parent = parent
        self.ID = self.menuentry
        self.createWidgets()
        return

    def createWidgets(self, width=600, height=600):
        """创建插件主界面控件（子类必须重写）。"""

        return

    def _getmethods(self):
        """返回插件中可用的公有方法列表。"""

        mems = inspect.getmembers(self, inspect.ismethod)
        methods = [m for m in mems if not m[0].startswith('_')]
        return methods

    def _update(self):
        """当关联表格发生变化时调用（可重写）。"""

        return

    def _aboutWindow(self):
        """显示关于对话框（可重写）。"""

        return

    def __repr__(self):
        return '<%s %r>' % (
            self.__class__.__name__,
            self.capabilities)

    def quit(self, evt=None):

        return

def load_plugins(plugins):
    """Load plugins"""

    failed = []
    for plugin in plugins:
        try:
            #print (plugin)
            __import__(plugin, None, None, [''])
        except Exception as e:
            print('failed to load %s plugin' %plugin)
            print(e)
            failed.append((plugin,e))
    return failed

def init_plugin_system(folders):
    """Find available plugins"""

    for folder in folders:
        if not os.path.exists(folder):
            continue
        if not folder in sys.path:
             sys.path.insert(0, folder)
        plugins = parsefolder(folder)
        #print (plugins)
        failed = load_plugins(plugins)
    return failed

def find_plugins():
    return Plugin.__subclasses__()

def parsefolder(folder):
    """Parse for all .py files in plugins folder or zip archive"""

    filenms=[]
    homedir = os.path.expanduser("~")
    if os.path.isfile(folder):
        #if in zip file, we need to handle that (installer distr)
        import zipfile
        zf = zipfile.ZipFile(folder,'r')
        dirlist = zf.namelist()
        for x in dirlist:
            if 'plugins' in x and x.endswith('.py'):
                print (x)
                zf.extract(x)
        zf.close()
        #copy plugins to home dir where they will be found
        shutil.copytree('plugins', os.path.join(homedir,'plugins'))

    elif os.path.isdir(folder):
        dirlist = os.listdir(folder)
        filenm=""
        for x in dirlist:
             filenm = x
             if filenm.endswith("py"):
                 filenms.append(os.path.splitext(filenm)[0])
        filenms.sort()
        filenameslist = [os.path.basename(y) for y in filenms]
        return filenameslist

_instances = {}

def get_plugins_instances(capability):
    """Returns instances of available plugins"""

    result = []
    for plugin in Plugin.__subclasses__():
        print (plugin)
        if capability in plugin.capabilities:
            if not plugin in _instances:
                _instances[plugin] = plugin()
            result.append(_instances[plugin])
    return result

def get_plugins_classes(capability):
    """Returns classes of available plugins"""

    result = []
    for plugin in Plugin.__subclasses__():
        if capability in plugin.capabilities:
            result.append(plugin)
    return result

def describe_class(obj):
    """ Describe the class object passed as argument,
       including its methods """

    import inspect
    methods = []
    cl = obj.__class__
    print ('Class: %s' % cl.__name__)
    count = 0
    for name in cl.__dict__:
       item = getattr(cl, name)
       if inspect.ismethod(item):
           count += 1
           #describe_func(item, True)
           methods.append(item)

    if count==0:
      print ('No members')
    return methods


def describe_func(obj, method=False):
   """ Describe the function object passed as argument.
   If this is a method object, the second argument will
   be passed as True """

   try:
       arginfo = inspect.getargspec(obj)
   except TypeError:
      print
      return

   args = arginfo[0]
   argsvar = arginfo[1]

   if args:
       if args[0] == 'self':
           print('\t%s is an instance method' % obj.__name__)
           args.pop(0)

       print('\t-Method Arguments:', args)

       if arginfo[3]:
           dl = len(arginfo[3])
           al = len(args)
           defargs = args[al-dl:al]
           print('\t--Default arguments:',zip(defargs, arginfo[3]))

   if arginfo[1]:
       print('\t-Positional Args Param: %s' % arginfo[1])
   if arginfo[2]:
       print('\t-Keyword Args Param: %s' % arginfo[2])
