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
    
import nodes, icons, constants

class NodeTreeFilter(object): # Using singleton pattern
    def __init__(self):
        globals()[self.__class__.__name__] = self
        
        self.__filter = None
        
    def __call__(self):
        return self
    
    def setFilter(self, filter_):
        self.__filter = filter_
    
    def getFilter(self):
        return self.__filter
    
    def isStringInFilter(self, string):
        if self.getFilter() is None:
            return True
        return self.getFilter().lower() in string.lower()

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

        self.__nodeDict = nodes.getNodeDict()
        self.__rootData = ['Nodes', '#']
        self.__rootItem = TreeItem(self.__rootData)
        self.__filter = NodeTreeFilter()
        
        self.setupModelData()
        
    def __nodeTypeMatchesFilter(self, nodeType):
        if self.__filter.getFilter() is None:
            return True
        if not self.__nodeDict.has_key(nodeType):
            return False
        return True in map(lambda x: self.__filter.isStringInFilter( x['name'].value()), nodes.getAllNodesByNodeType(nodeType))
        
    def setupModelData(self):
        numberOfNodesByType = nodes.getNumberOfNodesByType()
        for nodeType in nodes.getAllNodeTypes():
            if self.__nodeTypeMatchesFilter(nodeType):  
                nodeTypeItem = TreeItem([nodeType, numberOfNodesByType[nodeType]], parent = self.__rootItem)
                self.__rootItem.appendChild(nodeTypeItem)
                for node in self.__nodeDict[nodeType]:
                    if self.__filter.isStringInFilter(node['name'].value()):
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
        item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())
        elif role == QtCore.Qt.DecorationRole and index.column() == 0:
            if item.parent() == self.__rootItem:
                return icons.NodeIconLib().getIconForNodeType(item.data(0))
        elif role == QtCore.Qt.FontRole and item.parent() == self.__rootItem:
            font = QtGui.QFont()
            font.setBold(True)
            return font

    def flags(self, index):
        if not index.isValid():
            return 0;
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.__rootItem.data(section)
        
        
class NodeTreeView(QtGui.QTreeView):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self, parent)
        
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(*constants.ROWBASECOLOR))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(*constants.ALTERNATEROWBASECOLOR))
        self.setIconSize(QtCore.QSize(*constants.ICONSIZE))
        self.setAlternatingRowColors(True)
        self.setPalette(palette)
        #self.setSelectionMode() # TODO: enable multi-select
        
    def updateModel(self):
        self.setModel(NodeTreeModel())
        
    def setModel(self, model):
        QtGui.QTreeView.setModel(self, model)
        for columnIndex in range(self.model().columnCount(self.model().index(0, 0, QtCore.QModelIndex()))): # TODO: fix resizing
            self.resizeColumnToContents(columnIndex)       
        

    