#!/usr/bin/env python

''' This widget displays a selection of nodes in a treeView sorted by node-type  '''

__author__ = 'Manuel Macha'
__copyright__ = 'Copyright 2013, Manuel Macha'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = __author__
__email__ = 'manuel@manuelmacha.de'
__website__ = 'http://www.manuelmacha.de'
__git__ = 'https://github.com/manuelmacha/NukeAttributeSpreadsheet'

try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
    
import nodes
    
class NodeTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self.__nodeDict = nodes.getNodeDict()
        
    def columnCount(self, parent = None):
        return 1
    
    def rowCount(self, parent = None):
        return len(self.__nodeDict.keys())
    
    def index(self, row, column, parent = None):
        return self.createIndex(row, column)
    
    def parent(self, index):
        return self.createIndex(0, 0)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return 'ad'
        
        
class NodeTreeView(QtGui.QTreeView):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self, parent)
        

    