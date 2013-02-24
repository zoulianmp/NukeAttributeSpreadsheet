#!/usr/bin/env python

''' The main class for building the UI '''

__author__ = 'Manuel Macha'
__copyright__ = 'Copyright 2013, Manuel Macha'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = __author__
__email__ = 'manuel@manuelmacha.de'
__website__ = 'http://www.manuelmacha.de'
__git__ = 'https://github.com/manuelmacha/NukeAttributeSpreadsheet'

import mainWidget
    
class NukeAttributeSpreadsheetWidget(mainWidget.MainWidget):
    def __init__(self, parent = None):    
        mainWidget.MainWidget.__init__(self, parent)
    