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
    
import nodes

class NodeTypesModel(QtCore.QAbstractTableModel):
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self.__nodeTypes = nodes.getAllNodeTypes()
        self.__numberOfNodesByType = nodes.getNumberOfNodesByType()
        self.__headerNames = ('NodeType', '#')
        
    def __nodeTypeForIndex(self, index):
        return self.__nodeTypes[index.row() - 1]
    
    def __numberOfNodesByTypeForIndex(self, index):
        return self.__numberOfNodesByType[self.__nodeTypeForIndex(index)]
        
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
                return self.__nodeTypeForIndex(index)
            elif columnHeader == '#':
                return self.__numberOfNodesByTypeForIndex(index)
        elif role == QtCore.Qt.TextAlignmentRole:
            if columnHeader == '#':
                return QtCore.Qt.AlignCenter

class NodeTypesTableView(QtGui.QTableView):
    def __init__(self, parent = None):
        QtGui.QTableView.__init__(self, parent)
        
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.updateModel()
        
    def updateModel(self):
        self.setModel(NodeTypesModel())
        
    def setModel(self, model):
        QtGui.QTableView.setModel(self, model)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        
        