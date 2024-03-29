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

class Margins():
    ''' Margins object used for backwards-compatibility when running Qt-versions < 4.6 '''
    def __init__(self, *args):
        self.__left = args[0] if len(args) == 4 else constants.MARGIN
        self.__top = args[1] if len(args) == 4 else constants.MARGIN
        self.__right = args[2] if len(args) == 4 else constants.MARGIN
        self.__bottom = args[3] if len(args) == 4 else constants.MARGIN
    def left(self): return self.__left
    def top(self): return self.__top
    def right(self): return self.__right
    def bottom(self): return self.__bottom          
            

class NodeTypesTableModel(QtCore.QAbstractTableModel):
    ''' Implementation of model for use with NodeTypeTableView '''
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self.__nodeTypes = nodes.getAllNodeTypes()
        self.__numberOfNodesByType = nodes.getNumberOfNodesByType()
        self.__headerNames = ('NodeType', '#')
        
    def nodeTypeForIndex(self, index):
        return self.__nodeTypes[index.row()]
    
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
        
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(*constants.ROWBASECOLOR))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(*constants.ALTERNATEROWBASECOLOR))
        self.setIconSize(QtCore.QSize(*constants.ICONSIZE))
        self.setAlternatingRowColors(True)
        self.setPalette(palette)
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.updateModel()
        
    def contentsMargins(self):
        try:
            return QtGui.QTableView.contentsMargins(self)
        except:
            return Margins()
        
    def getCombinedColumnWidth(self, includingMargins = True):
        margins = self.contentsMargins().left() + self.contentsMargins().right() if includingMargins == True else 0
        return self.columnWidth(0) + self.columnWidth(1) + margins
        
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
        self.setModel(NodeTypesTableModel())
        self.selectNodeTypes(selectedNodeTypes)
        
    def setModel(self, model):
        QtGui.QTableView.setModel(self, model)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        
class NodeTypesWidget(QtGui.QGroupBox):
    def __init__(self, parent = None):
        QtGui.QGroupBox.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())

        
        



        
        