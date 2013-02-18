#!/usr/bin/env python

''' This widget displays a list of all the different types of nodes present in the current nukescript '''

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

class NodeTypesModel(QtCore.QAbstractTableModel):
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self.__nodeTypes = nodes.getAllNodeTypes()
        self.__numberOfNodesByType = nodes.getNumberOfNodesByType()
        self.__headerNames = ('NodeType', '#')
        
    def nodeTypeForIndex(self, index):
        return self.__nodeTypes[index.row() - 1]
    
    def indexForNodeType(self, nodeType):
        try:
            return self.__nodeTypes.index(nodeType)
        except ValueError:
            return None
    
    def __numberOfNodesByTypeForIndex(self, index):
        return self.__numberOfNodesByType[self.nodeTypeForIndex(index)]
        
    def __columnHeaderForIndex(self, index):
        return self.__headerNames[index.column()]
        
    def rowCount(self, parent):
        return len(self.__nodeTypes)
    
    def columnCount(self, parent):
        return len(self.__headerNames)
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.__headerNames[section]
    
    def data(self, index, role):
        columnHeader = self.__columnHeaderForIndex(index)
        if role == QtCore.Qt.DisplayRole:
            if columnHeader == 'NodeType':
                if self.nodeTypeForIndex(index)[-1].isdigit():  # For cases where for example a 'Merge' is actually internally representing a 'Merge2' node 
                    return self.nodeTypeForIndex(index)[0:-1]                
                return self.nodeTypeForIndex(index)
            elif columnHeader == '#':
                return self.__numberOfNodesByTypeForIndex(index)
        elif role == QtCore.Qt.TextAlignmentRole:
            if columnHeader == '#':
                return QtCore.Qt.AlignCenter
        elif role == QtCore.Qt.DecorationRole:
            if columnHeader == 'NodeType':
                if self.nodeTypeForIndex(index)[-1].isdigit():  # For cases where for example a 'Merge' is actually internally representing a 'Merge2' node 
                    return icons.NodeIconLib().getIconForNodeType(self.nodeTypeForIndex(index)[0:-1])
                return icons.NodeIconLib().getIconForNodeType(self.nodeTypeForIndex(index))

class NodeTypesTableView(QtGui.QTableView):
    def __init__(self, parent = None):
        QtGui.QTableView.__init__(self, parent)
        
        self.setIconSize(QtCore.QSize(*constants.ICONSIZE))
        self.setAlternatingRowColors(True)  # TODO: change alternating color to something lest drastic than black
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.updateModel()
        
    def getCombinedColumnWidth(self):
        return self.columnWidth(0) + self.columnWidth(1)
        
    def getSelectedNodeTypes(self):
        return map(lambda modelIndex: self.model().nodeTypeForIndex(modelIndex), self.selectedIndexes())
        
    def selectNodeTypes(self, nodeTypes):
        self.clearSelection()
        for nodeType in nodeTypes:
            index = self.model().indexForNodeType(nodeType)
            if not index is None:
                modelIndex = self.model().index(index, 0)
                self.selectionModel().select(modelIndex, QtGui.QItemSelectionModel.Select)
        
    def updateModel(self):
        selectedNodeTypes = self.getSelectedNodeTypes()
        self.setModel(NodeTypesModel())
        self.selectNodeTypes(selectedNodeTypes)
        
    def setModel(self, model):
        QtGui.QTableView.setModel(self, model)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        
        