#!/usr/bin/env python

''' The main widget'''

__author__ = 'Manuel Macha'
__copyright__ = 'Copyright 2013, Manuel Macha'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = __author__
__email__ = 'manuel@manuelmacha.de'

try:
    from PyQt4 import QtGui
except ImportError:
    from PySide import QtGui
    
class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):    
        QtGui.QWidget.__init__(self, parent)
        
        self.__btnReload = None
        self.__vSplitter = None
    
        self.__initNukeAttributeSpreadsheetWidget()
        
    def __initNukeAttributeSpreadsheetWidget(self):
        self.setLayout(QtGui.QVBoxLayout())                                 # Create the main layout
        
        self.__btnReload = QtGui.QPushButton('Reload', self)                # Create the 'Reload' button
        self.layout().addWidget(self.__btnReload)                           # Add button to layout
        
        self.__vSplitter = QtGui.QSplitter(self)                            # Create the main splitter
        self.layout().addWidget(self.__vSplitter)                           # Add splitter to main-layout
        
        self.__vSplitter.addWidget(QtGui.QPushButton(self.__vSplitter))
        self.__vSplitter.addWidget(QtGui.QPushButton(self.__vSplitter))
        
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    nass = MainWidget()
    nass.show()
    nass.raise_()
    sys.exit(app.exec_())        