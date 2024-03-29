#!/usr/bin/env python

'''
This widget displays a selection of nodes in a treeView sorted by node-type.
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

class NodeTreeFilter(object):
    '''
    Stores a string that is being used in order to filter items from the TreeViewModel.
    This class is using some sort of singleton pattern so it can only be initialized once.
    Every other call to this class will return the same instance.
    '''
    def __init__(self): 
        globals()[self.__class__.__name__] = self
        
        self.__filter = None                                # Stores the string that is being used to filter the NodeTreeModel
        
    def __call__(self):
        return self                                         # Overridden method in order to enforce singleton-pattern
    
    def setFilter(self, filter_):
        ''' Set the filter string '''
        self.__filter = filter_
    
    def getFilter(self):
        ''' Get the filter string '''
        return self.__filter
    
    def isStringInFilter(self, string):
        '''
        Determines if a given string is identical or a substring of the filter-string
        The comparison is not case-sensitive!
        Return value: True or False (Bool) 
        '''
        if self.getFilter() is None:
            return True
        return self.getFilter().lower() in string.lower()

class TreeItem(object):
    '''
    
    TreeItem and TreeModel implemented from http://qt-project.org/doc/qt-4.8/itemviews-simpletreemodel.html
    '''
    def __init__(self, data, parent = None):
        self.__childItems = []
        self.__itemData = data
        self.__parentItem = parent
        self.__representsRoot = False
        self.__representsNodeType = False
        self.__representsNode = False
        
    def representsRoot(self): return self.__representsRoot
    def representsNodeType(self): return self.__representsNodeType
    def representsNode(self): return self.__representsNode
    def setRepresentsRoot(self, value): self.__representsRoot = value
    def setRepresentsNodeType(self, value): self.__representsNodeType = value
    def setRepresentsNode(self, value): self.__representsNode    = value 
        
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
        self.__rootData = ['Nodes', '#', '']
        self.__rootItem = TreeItem(self.__rootData)
        self.__rootItem.setRepresentsRoot(True)
        self.__filter = NodeTreeFilter()
        
        self.setupModelData()
        
    def getRoot(self):
        return self.__rootItem
    
    def getNodeTypeItems(self):
        return self.getRoot().childItems()
        
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
                nodeTypeItem = TreeItem([nodeType, numberOfNodesByType[nodeType], ''], parent = self.__rootItem)
                nodeTypeItem.setRepresentsNodeType(True)
                self.__rootItem.appendChild(nodeTypeItem)
                for node in self.__nodeDict[nodeType]:
                    if self.__filter.isStringInFilter(node['name'].value()):
                        nodeItem = TreeItem([node['name'].value(), '', ''], parent = nodeTypeItem)
                        nodeItem.setRepresentsNode(True)
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
        elif role == QtCore.Qt.DecorationRole:
            if item.representsNodeType():
                if index.column() == 0:
                    return icons.NodeIconLib().getIconForNodeType(item.data(0))
                elif index.column() == 2:
                    return QtGui.QIcon(icons.Icon('node-select-all.png'))
            elif item.representsNode():
                if index.column() == 2:
                    return QtGui.QIcon(icons.Icon('node-select-child.png'))
                

                    #return icons.Icon('node-select-all.png')
            
        elif role == QtCore.Qt.FontRole and item.parent() == self.__rootItem and index.column() == 0:
            font = QtGui.QFont()
            font.setBold(True)
            return font

    def flags(self, index):
        if not index.isValid():
            return 0;
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return self.__rootItem.data(section)
            elif role == QtCore.Qt.DecorationRole:
                if section == 0:
                    return icons.NodeIconLib().getNukeIcon()
                elif section ==2:
                    return QtGui.QIcon(icons.Icon('node.png'))

        
        
class NodeTreeView(QtGui.QTreeView):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self, parent)
        
        self.__selectedNodes = []
        self.__selectedNodeTypes = []
        self.__expandedItems = []
        self.__preventRecursion = True

        self.__initNodeTreeView()
    
    def setExpandedItems(self, modelIndex):
        expandedItems = []
        for index_ in self.model().persistentIndexList():
            if self.isExpanded(index_):
                expandedItems.append(index_.internalPointer())
        self.__expandedItems = expandedItems
        
    def getSelectedNodeTypes(self):
        selectedNodeTypes = []
        for index_ in self.selectedIndexes():
            if index_.internalPointer().representsNodeType():
                selectedNodeTypes.append(index_.internalPointer().data(0))
        return sorted(list(set(selectedNodeTypes)))   
    
    def getSelectedNodeNames(self):
        selectedNodes = []
        for index_ in self.selectedIndexes():
            if index_.internalPointer().representsNode():
                selectedNodes.append(index_.internalPointer().data(0))
        return sorted(list(set(selectedNodes)))   
    
    def getSelectedNodes(self):
        return nodes.getNodesFromNodeNames(self.getSelectedNodeNames())       
    
    def __getModelIndexesFromItemSelectionIfIndexRepresentsNodeType(self, itemSelection):
        modelIndexesRepresentingNodeTypes = []
        for index_ in itemSelection.indexes():
            if index_.column() == 0 and index_.internalPointer().representsNodeType():
                modelIndexesRepresentingNodeTypes.append(index_)
        return modelIndexesRepresentingNodeTypes
    
    def __modifyChildNodeSelectionForNodeTypeModelIndexes(self, modelIndexes, select = True, deselect = False):
        ''' If a nodeType is being selected or deselected, select/deselect all nodes under it. ''' 
        for modelIndex in modelIndexes:                                                                             # Loop through the provided modelIndexes. These always represent nodeTyes
            i = 0                                                                                                   # Counter to identify the position of nodes in the list of the nodeType's children
            while modelIndex.child(i, 0).isValid():                                                                 # We don't know how many children the nodeType has so we just cycle through them until an invalid modelIndex is being returned
                if select == True:                                                                                  # Check if the method is supposed to select items in the treeView
                    self.selectionModel().select(modelIndex.child(i, 0), QtGui.QItemSelectionModel.Select)          # Modify the selectionModel
                elif deselect == True:                                                                              # Check if the method is supposed to deselect items in the treeView
                    for k in range(modelIndex.internalPointer().columnCount()):                                     # When deselecting, we need to also make sure that all columns for a certain item are being deselected, not only the first one              
                        self.selectionModel().select(modelIndex.child(i, k), QtGui.QItemSelectionModel.Deselect)    # Modify the selectionModel
                i+=1                                                                                                # Increase the counter                                                                                                             
        
    def selectionChanged(self, selected, deselected):
        self.__selectedNodes = self.getSelectedNodes()
        self.__selectedNodeTypes = self.getSelectedNodeTypes()        
        selectedModelIndexes = self.__getModelIndexesFromItemSelectionIfIndexRepresentsNodeType(selected)
        deselectedModelIndexes = self.__getModelIndexesFromItemSelectionIfIndexRepresentsNodeType(deselected)
        self.__modifyChildNodeSelectionForNodeTypeModelIndexes(selectedModelIndexes)
        self.__modifyChildNodeSelectionForNodeTypeModelIndexes(deselectedModelIndexes, select = False, deselect = True)
        return QtGui.QTreeView.selectionChanged(self, selected, deselected)
    
    def __restoreExpanded(self):
        expandedNodeTypes = tuple(set(map(lambda x: x.data(0), self.__expandedItems)))
        for i in range(len(self.model().getRoot().childItems())):
            modelIndex = self.model().createIndex(i, 0, self.model().getRoot().child(i))
            if modelIndex.internalPointer().data(0) in expandedNodeTypes:
                self.setExpanded(modelIndex, True) 
                
    def __restoreSelectedNodeTypes(self, selectedNodeTypesBeforeModelUpdate):
        for i in range(len(self.model().getRoot().childItems())):
            modelIndex = self.model().createIndex(i, 0, self.model().getRoot().child(i))
            if str(modelIndex.internalPointer().data(0)) in selectedNodeTypesBeforeModelUpdate:
                self.selectionModel().select(modelIndex, QtGui.QItemSelectionModel.Select)
                
    def __restoreSelectedNodes(self, selectedNodeNamesBeforeModelUpdate):
        k = 0
        for nodeTypeItem in self.model().getRoot().childItems():
            for i in range(len(nodeTypeItem.childItems())):
                nodeName = nodeTypeItem.childItems()[i].data(0)
                if nodeName in selectedNodeNamesBeforeModelUpdate:
                    parentModelIndex = self.model().createIndex(k, 0, self.model().getRoot().child(k))
                    if parentModelIndex.isValid():  
                        childModelIndex = parentModelIndex.child(i, 0)
                        if childModelIndex.isValid():
                            self.selectionModel().select(childModelIndex, QtGui.QItemSelectionModel.Select)
            k+=1

    
    def __restoreState(self):
        selectedNodeTypesBeforeModelUpdate = self.__selectedNodeTypes
        selectedNodeNamesBeforeModelUpdate = map(lambda x: x['name'].value(), self.__selectedNodes)
        self.__restoreExpanded()
        self.__restoreSelectedNodeTypes(selectedNodeTypesBeforeModelUpdate)
        self.__restoreSelectedNodes(selectedNodeNamesBeforeModelUpdate)

        
    def updateModel(self):
        self.setModel(NodeTreeModel())
        
    def setModel(self, model):
        QtGui.QTreeView.setModel(self, model)
        for columnIndex in range(self.model().columnCount(self.model().index(0, 0, QtCore.QModelIndex()))): # TODO: fix resizing
            self.resizeColumnToContents(columnIndex)   
        self.__restoreState()
            
    def __initNodeTreeView(self):  
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(*constants.ROWBASECOLOR))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(*constants.ALTERNATEROWBASECOLOR))
        self.setIconSize(QtCore.QSize(*constants.ICONSIZE))
        self.setAlternatingRowColors(True)
        self.setPalette(palette)
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection) 
        self.expanded.connect(self.setExpandedItems)
        self.collapsed.connect(self.setExpandedItems)
        
        
                
        

    