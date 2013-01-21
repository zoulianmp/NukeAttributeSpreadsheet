try:
    from PyQt4 import QtGui
except ImportError:
    from PySide import QtGui
    
class NukeAttributeSpreadsheetWidget(QtGui.QWidget):
    def __init__(self, parent = None):    
        QtGui.QWidget.__init__(self, parent)
    
    
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    nass = NukeAttributeSpreadsheetWidget()
    nass.show()
    nass.raise_()
    sys.exit(app.exec_())
