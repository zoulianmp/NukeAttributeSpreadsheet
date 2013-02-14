import mainWidget
    
class NukeAttributeSpreadsheetWidget(mainWidget.MainWidget):
    def __init__(self, parent = None):    
        mainWidget.MainWidget.__init__(self, parent)

           
if __name__ == '__main__':
    try:
        from PyQt4 import QtGui
    except ImportError:
        from PySide import QtGui    
    import sys
    app = QtGui.QApplication(sys.argv)
    nass = NukeAttributeSpreadsheetWidget()
    nass.show()
    nass.raise_()
    sys.exit(app.exec_())  
