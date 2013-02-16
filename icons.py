#!/usr/bin/env python

'''
Classes and functions related to Nuke's icons
The way to derive the icon-path is kind of a hack and it's only been tested on OSX with a default installation of Nuke 7.0v4
'''

__author__ = 'Manuel Macha'
__copyright__ = 'Copyright 2013, Manuel Macha'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = __author__
__email__ = 'manuel@manuelmacha.de'
__website__ = 'http://www.manuelmacha.de'
__git__ = 'https://github.com/manuelmacha/NukeAttributeSpreadsheet'

import os
import nuke

try:
    from PyQt4 import QtGui
except ImportError:
    from PySide import QtGui

class NodeIconLib(object): # Using singleton pattern
    def __init__(self):
        globals()[self.__class__.__name__] = self
        self.__iconPath = self.__getNukeDefaultIconPath()
        self.__icons = {}
        self.__getIcons()        

    def __call__(self):
        return self

    def __getNukeDefaultIconPath(self):
        versionString = nuke.NUKE_VERSION_STRING
        for path in nuke.pluginPath():
            if versionString in path and 'icons' in path:
                return path
            
    def __getIconForNodeType(self, nodeType):
        fullIconPath = os.path.join(self.__iconPath, nodeType)
        if os.path.isfile(fullIconPath):
            return QtGui.QIcon(fullIconPath)            
    
    def __getIcons(self):
        for menu in nuke.toolbar('Nodes').items():
            if isinstance(menu, nuke.Menu):
                for subItem in menu.items():
                    if isinstance(subItem, nuke.MenuItem):
                        self.__icons[subItem.name()] = self.__getIconForNodeType(subItem.icon())
                    elif isinstance(subItem, nuke.Menu):
                        for subSubItem in subItem.items():
                            if isinstance(subSubItem, nuke.MenuItem):
                                self.__icons[subSubItem.name()] = self.__getIconForNodeType(subItem.icon())    

    def getIconForNodeType(self, nodeType):
        return self.__icons.get(nodeType, QtGui.QIcon())

    