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
    
import nodeTypesTable, nodes
import nuke
    
class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):    
        QtGui.QWidget.__init__(self, parent)
        
        self.__btnReload = None
        self.__vSplitter = None
        self.__hSplitter = None
        self.__nodeTypesTableView = None
    
        self.__initNukeAttributeSpreadsheetWidget()                         # Init the main UI-elements
        self.__connectSignalsToSlots()                                      # Connect all signals and slots
        self.__initCallbacks()                                              # Init the callbacks that act upon node creation/deletion
        
    def updateNodeTypesTableView(self):
        self.__nodeTypesTableView.updateModel()                             # Call 'updateModel()' in the nodeType tableView
        
    def __initCallbacks(self):
        nuke.addOnCreate(self.updateNodeTypesTableView)                     # If a new node is created, the nodeType tableView will be updated
        nuke.addOnDestroy(self.updateNodeTypesTableView)                    # TODO: Doesn't seem to update, looks like we need to find a way to call the update AFTER the node is destroyed
        
    def __connectSignalsToSlots(self):
        self.__btnReload.clicked.connect(self.updateNodeTypesTableView)     # Licking the 'Reload' button will update the nodeType tableView
        
    def __initNukeAttributeSpreadsheetWidget(self):
        self.setLayout(QtGui.QVBoxLayout())                                 # Create the main layout
        
        self.__btnReload = QtGui.QPushButton('Reload', self)                # Create the 'Reload' button
        self.layout().addWidget(self.__btnReload)                           # Add button to layout
        
        self.__vSplitter = QtGui.QSplitter(self)                            # Create the main splitter
        self.layout().addWidget(self.__vSplitter)                           # Add splitter to main-layout
        
        self.__vSplitter.setLayout(QtGui.QVBoxLayout())                     # Add a vertical layout to the main splitter
        self.__hSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)              # Create a horizontal splitter 
        self.__vSplitter.layout().addWidget(self.__hSplitter)               # Add the horizontal splitter to the left layout of the main splitter
        
        self.__nodeTypesTableView = nodeTypesTable.NodeTypesTableView(self.__hSplitter) # Create a tableView which will be responsible for displaying the types of nodes in teh current nukescript
        self.__hSplitter.addWidget(self.__nodeTypesTableView)               # Add the tableView to the layout of the horizontal splitter
        self.__hSplitter.addWidget(QtGui.QTreeView(self.__hSplitter))
        
        self.__vSplitter.addWidget(QtGui.QTableView(self.__vSplitter))
        
        
        
        
        
        
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    nass = MainWidget()
    nass.show()
    nass.raise_()
    sys.exit(app.exec_())        