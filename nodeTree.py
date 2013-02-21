#!/usr/bin/env python

'''
This widget displays a selection of nodes in a treeView sorted by node-type.

Implemented from http://qt-project.org/doc/qt-4.8/itemviews-simpletreemodel.html
'''

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

class TreeItem(object):
    def __init__(self, data, parent = None):
        self.__childItems = []
        self.__itemData = data
        self.__parentItem = parent
        
    def childItems(self):
        return self.__childItems
        
    def appendChild(self, child):
        self.__childItems.append(child)
        
    def child(self, row):
        return self.__childItems[row]
    
    def childCount(self):
        return len(self.__childItems)

    def columnCount(self):
        return len(self.__itemData)
    
    def row(self):
        if not self.__parentItem is None:
            return self.parent().childItems().index(self)
        
    def data(self, column):
        if column < self.columnCount():
            return self.__itemData[column]
        return ''
    
    def parent(self):
        return self.__parentItem
    
class NodeTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self.__rootData = ['A', 'B']
        self.__rootItem = TreeItem(self.__rootData)
        self.setupModelData()
        
    def setupModelData(self):
        nodeDict = nodes.getNodeDict()
        print nodeDict
        for nodeType in nodes.getAllNodeTypes():
            print nodeType
            nodeTypeItem = TreeItem([nodeType], parent = self.__rootItem)
            self.__rootItem.appendChild(nodeTypeItem)
            for node in nodeDict[nodeType]:
                print '\t%s' % node['name'].value()
                nodeItem = TreeItem([node['name'].value()], parent = nodeTypeItem)
                nodeTypeItem.appendChild(nodeItem)
                
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        
        parentItem = None
        if not parent.isValid():
            parentItem = self.__rootItem
        else:
            parentItem = parent.internalPointer()
            
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
        
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        
        if parentItem == self.__rootItem:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentItem.row(), 0, parentItem)
    
    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        
        parentItem = None
        if not parent.isValid():
            parentItem = self.__rootItem
        else:
            parentItem = parent.internalPointer()
            
        return parentItem.childCount()
    
    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.__rootItem.columnCount()
        
    def data(self, index, role):
        if not index.isValid():
            return None
        if not role == QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0;
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
class NodeTreeView(QtGui.QTreeView):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self, parent)
        

    