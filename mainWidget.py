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
    from PyQt4 import QtGui
except ImportError:
    from PySide import QtGui
    
import nodeTypesTable
import nuke
    
class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):    
        QtGui.QWidget.__init__(self, parent)
        
        self.__btnReload = None
        self.__vSplitter = None
        self.__nodeTypesTableView = None
    
        self.__initNukeAttributeSpreadsheetWidget()
        self.__initCallbacks()
        
    def updateNodeTypesTableView(self):
        self.__nodeTypesTableView.updateModel()
        
    def __initCallbacks(self):
        nuke.addOnCreate(self.updateNodeTypesTableView)
        nuke.addOnDestroy(self.updateNodeTypesTableView) # Doesn't seem to update
        
    def __initNukeAttributeSpreadsheetWidget(self):
        self.setLayout(QtGui.QVBoxLayout())                                 # Create the main layout
        
        self.__btnReload = QtGui.QPushButton('Reload', self)                # Create the 'Reload' button
        self.layout().addWidget(self.__btnReload)                           # Add button to layout
        
        self.__vSplitter = QtGui.QSplitter(self)                            # Create the main splitter
        self.layout().addWidget(self.__vSplitter)                           # Add splitter to main-layout
        
        self.__nodeTypesTableView = nodeTypesTable.NodeTypesTableView(self.__vSplitter)
        
        self.__vSplitter.addWidget(self.__nodeTypesTableView)
        self.__vSplitter.addWidget(QtGui.QPushButton(self.__vSplitter))
        
        self.__btnReload.clicked.connect(self.updateNodeTypesTableView)
        
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    nass = MainWidget()
    nass.show()
    nass.raise_()
    sys.exit(app.exec_())        