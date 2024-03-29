#!/usr/bin/env python

'''
Classes and functions related to Nuke's icons
The way to derive the icon-path is kind of a hack.
It's been tested on OSX and Linux with default installations of Nuke 6.3 and 7.0v4
TODO: Add ability to set paths to icons through environment-variable
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
import constants

try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
    
    
class Icon(QtGui.QIcon):
    def __init__(self, name = None):
        QtGui.QIcon.__init__(self)
        fullIconPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', name)
        if os.path.isfile(fullIconPath):
            self.addFile(fullIconPath)
        else:
            raise Exception('Invalid path: %s' % fullIconPath)
    
class IconBlank(QtGui.QIcon):
    def __init__(self):
        QtGui.QIcon.__init__(self, QtGui.QPixmap(QtCore.QSize(*constants.ICONSIZE)))

class NodeIconLib(object): # Using singleton pattern
    def __init__(self):
        globals()[self.__class__.__name__] = self
        self.__iconPaths = self.__getNukeDefaultIconPaths()
        self.__icons = {}
        self.__getIcons()
        self.__getUnresolvedIcons()
            

    def __call__(self):
        return self

    def __getNukeDefaultIconPaths(self):
        iconPaths = []
        for path in nuke.pluginPath():
            if nuke.NUKE_VERSION_STRING in path and 'icons' in path:
                iconPaths.append(path)
        return iconPaths
            
    def __getIconForNodeType(self, nodeType):
        for path in self.__iconPaths:
            fullIconPath = os.path.join(path, nodeType)
            if os.path.isfile(fullIconPath):
                return QtGui.QIcon(fullIconPath)            
    
    def __getIcons(self):
        for menu in nuke.toolbar('Nodes').items():
            if isinstance(menu, nuke.Menu):
                for subItem in menu.items():
                    if isinstance(subItem, nuke.MenuItem) or isinstance(subItem, nuke.Menu):
                        self.__icons[subItem.name()] = self.__getIconForNodeType(subItem.icon())
                    elif isinstance(subItem, nuke.Menu):
                        for subSubItem in subItem.items():
                            self.__icons[subSubItem.name()] = self.__getIconForNodeType(subItem.icon())
                            
    def __getUnresolvedIcons(self):
        self.__icons['NukeApp32'] = self.__getIconForNodeType('NukeApp32.png')
        self.__icons['BackdropNode'] = self.__getIconForNodeType('Backdrop.png')
        self.__icons['Expression'] = self.__getIconForNodeType('Expression.png')
        self.__icons['Merge2'] = self.__getIconForNodeType('Merge.png')      

    def getIconForNodeType(self, nodeType):
        return self.__icons.get(nodeType, IconBlank())
    
    def getNukeIcon(self):
        return self.getIconForNodeType('NukeApp32')
        

    