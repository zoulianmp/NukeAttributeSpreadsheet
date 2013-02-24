import PySide

class Framework:
    undefined = 0
    pyqt = 1
    pyside = 2

    @classmethod
    def getStringForValue(cls, value):
        if value == cls.undefined: return 'undefined'
        elif value == cls.pyqt: return 'pyqt'
        elif value == cls.pyside: return 'pyside'
        
def getFramework():
    try:
        import PyQt4.QtCore
        return Framework.pyqt
    except ImportError:
        try:
            import PySide.QtCore
            return Framework.pyside
        except ImportError:
            return Framework.undefined
    return Framework.undefined

def isFrameworkPyQt():
    return getFramework() == Framework.pyqt

def isFrameWorkPyside():
    return getFramework() == Framework.pyside