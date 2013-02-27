try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
    
import constants, utils, icons

class SearchBox(QtGui.QLineEdit):
    # implementation from http://git.forwardbias.in/?p=lineeditclearbutton.git;a=blob;f=lineedit.cpp;hb=HEAD
    def __init__(self, parent = None, defaultText = None):
        QtGui.QLineEdit.__init__(self, parent = parent)
        
        self.defaultText = defaultText or 'Search...'
        self.clearButton = None
        self.searchLabel = None
        self.searchIcon = None
        self.setCompleter(QtGui.QCompleter([]))
        self.setCompleterDefaults()    
        self.initSearchBox()
        
    def __isTextEmpty(self):
        emptyText = True
        if utils.isFrameworkPyQt():
            emptyText = self.text().isEmpty()
        elif utils.isFrameWorkPyside():
            if self.text():
                emptyText = False
        return emptyText        
        
    def setCompleterDefaults(self):
        self.completer().setCaseSensitivity(QtCore.Qt.CaseInsensitive)        

    def addCompletion(self, word):
        #print 'adding completion ' + word
        completions = [word]
        for completionString in self.completer().model().stringList():
            if not word == completionString:
                completions.append(completionString)
        self.completer().model().setStringList(completions)
        self.setCompleterDefaults()

    def resizeEvent(self, event):
        sz = self.clearButton.sizeHint();
        defaultFrameWidth = QtGui.QStyle.PM_DefaultFrameWidth
        frameWidth = QtGui.QApplication.style().pixelMetric(defaultFrameWidth);
        self.clearButton.move(self.rect().right() - frameWidth - sz.width(), (self.rect().bottom() + 1 - sz.height()) * 0.5)
        self.searchIcon.move(self.clearButton.pos())
        self.searchLabel.move(5, 5)

    def focusInEvent(self, *args, **kwargs):
        self.searchLabel.setVisible(False)
        #self.searchIcon.setVisible(False)
        return QtGui.QLineEdit.focusInEvent(self, *args, **kwargs)
    
    def focusOutEvent(self, *args, **kwargs):
        if self.__isTextEmpty():
            self.searchLabel.setVisible(True)
            self.searchIcon.setVisible(True)
        return QtGui.QLineEdit.focusOutEvent(self, *args, **kwargs)
    
    def reset(self):
        self.clear()
        self.updateClearButton()
    
    def updateClearButton(self):
        if self.__isTextEmpty():
            self.searchLabel.setVisible(True)
            self.clearButton.setVisible(False)  # This line does exactly the same as the block above
            self.searchIcon.setVisible(True)
        else:
            self.clearButton.setVisible(True)
            self.searchLabel.setVisible(False)
            self.searchIcon.setVisible(False)
                       
    def adjustDimensions(self):
        defaultFrameWidth = QtGui.QStyle.PM_DefaultFrameWidth        
        frameWidth = QtGui.QApplication.style().pixelMetric(defaultFrameWidth);        
        width = self.clearButton.sizeHint().width() + frameWidth + 1        
        style = "QLineEdit { padding-right: %ipx; }" % width
        self.setStyleSheet(style)
        
        minimumSize = self.minimumSizeHint();        
        max1 = max([minimumSize.width(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2])
        max2 = max([minimumSize.height(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2])       
        self.setMinimumSize(max1, max2)               

    def initSearchIcon(self):
        icon = icons.Icon(name = 'magnifier.png')
        self.searchIcon = QtGui.QToolButton(self)                     
        self.searchIcon.setIcon(icon)
        self.searchIcon.setIconSize( QtCore.QSize(18, 18) )
        self.searchIcon.setStyleSheet("QToolButton { border: none; padding: 0px; background-color: rgba(0, 0, 0, 0)}")
        
    def initSearchLabel(self):
        self.searchLabel = QtGui.QLabel(self)
        self.searchLabel.setText(self.defaultText)
        self.searchLabel.setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 0); }")        

    def initClearButton(self):
        icon = icons.Icon(name = 'cross.png')
        self.clearButton = QtGui.QToolButton(self)                     
        self.clearButton.setIcon(icon)
        self.clearButton.setIconSize( QtCore.QSize(18, 18) )
        self.clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; background-color: rgba(0, 0, 0, 0) }")
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.clear)        
        
    def initSearchBox(self):
        self.setMinimumHeight(constants.BUTTONHEIGHT)
        self.setMaximumHeight(self.minimumHeight())         
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        
        self.initClearButton()
        self.initSearchLabel()
        self.initSearchIcon()
        self.adjustDimensions()


 
    