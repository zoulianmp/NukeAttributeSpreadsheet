#!/usr/bin/env python

''' The main widget'''


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
    
import nodeTree
from searchBox import SearchBox
import nuke
    
class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):    
        QtGui.QWidget.__init__(self, parent)
        
        self.__btnReload = None
        self.__vSplitter = None
        self.__hSplitter = None
        self.__nodeSearchBox = None
        self.__nodeTreeView = None
    
        self.__initNukeAttributeSpreadsheetWidget()                         # Init the main UI-elements
        self.__connectSignalsToSlots()                                      # Connect all signals and slots
        self.__initCallbacks()                                              # Init the callbacks that act upon node creation/deletion
        #self.__fitVSplitterToLeftColumn()
        
    def closeEvent(self, event):
        ''' The purpose of this overloaded method is to call the method that is responsible for removing any callbacks previsouly created in case the UI is being closed ''' 
        self.__removeCallbacks()
        return QtGui.QWidget.closeEvent(self, event)

    def __fitVSplitterToLeftColumn(self):
        splitterWidth = self.__vSplitter.width()                            # Get the entire width of the main-splitter
        leftWidth = self.__nodeTypesTableView.getCombinedColumnWidth()      # Calculate left splitter width using the width of the nodeTypesTableView including it's margins
        rightWidth = splitterWidth - leftWidth                              # Calculate the resulting right splitter-width
        self.__vSplitter.setSizes([leftWidth, rightWidth])                  # Set the size of the individual columns
        
    def updateNodeTree(self):
        nodeTree.NodeTreeFilter().setFilter(str(self.__nodeSearchBox.text()))
        self.__nodeTreeView.updateModel()                                   # Call 'updateModel()' in the nodeType tableView
        #self.__fitVSplitterToLeftColumn()                                   # Adjust the width of the left column
        
    def __removeCallbacks(self):
        ''' Call this method when the UI is being closed in order to remove any callbacks to update the UI which will no longer be required'''
        nuke.removeOnCreate(self.updateNodeTree)                            # Remove callback responsible for updating the UI when nodes are created               
        nuke.removeOnDestroy(self.updateNodeTree)                           # Remove callback responsible for updating the UI when nodes are destroyed
        
    def __initCallbacks(self):
        nuke.addOnCreate(self.updateNodeTree)                               # If a new node is created, the nodeType tableView will be updated
        nuke.addOnDestroy(self.updateNodeTree)                              # TODO: Doesn't seem to update, looks like we need to find a way to call the update AFTER the node is destroyed
        
    def __connectSignalsToSlots(self):
        self.__btnReload.clicked.connect(self.updateNodeTree)     # Licking the 'Reload' button will update the nodeType tableView
        self.__nodeSearchBox.textChanged.connect(self.updateNodeTree)
        self.__nodeSearchBox.textChanged.connect(self.__nodeSearchBox.updateClearButton)
        
    def __initNukeAttributeSpreadsheetWidget(self):
        self.setLayout(QtGui.QVBoxLayout())                                 # Create the main layout
        
        self.__btnReload = QtGui.QPushButton('Reload', self)                # Create the 'Reload' button
        self.layout().addWidget(self.__btnReload)                           # Add button to layout
        
        self.__vSplitter = QtGui.QSplitter(self)                            # Create the main splitter
        self.layout().addWidget(self.__vSplitter)                           # Add splitter to main-layout
        
        self.__vSplitter.setLayout(QtGui.QVBoxLayout())                     # Add a vertical layout to the main splitter
        
        self.__nodeSearchBox = SearchBox(self.__vSplitter)
        self.__nodeTreeView = nodeTree.NodeTreeView(self.__vSplitter)       # Create a tableView which will be responsible for displaying the types of nodes in teh current nukescript
        self.__nodeTreeView.setModel(nodeTree.NodeTreeModel())
        
        w = QtGui.QWidget()
        w.setLayout(QtGui.QVBoxLayout())
        self.__vSplitter.layout().addWidget(w) 
        
        w.layout().addWidget(self.__nodeSearchBox) 
        w.layout().addWidget(self.__nodeTreeView)
        
        self.__vSplitter.addWidget(QtGui.QTableView(self.__vSplitter))
        
        self.__vSplitter.setStretchFactor(0, 0)                             # Set the stretch factor of the left splitter
        self.__vSplitter.setStretchFactor(1, 100)                           # Set the stretch factor of the right splitter
        
              