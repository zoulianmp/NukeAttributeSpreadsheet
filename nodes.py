#!/usr/bin/env python

''' Convenience functions to access nodes/node-info '''

__author__ = 'Manuel Macha'
__copyright__ = 'Copyright 2013, Manuel Macha'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = __author__
__email__ = 'manuel@manuelmacha.de'

import nuke

def getAllNodes():
    return nuke.allNodes()

def getAllNodeTypes():
    return tuple(set(map(lambda node: node.Class(), getAllNodes())))

def getNumberOfNodesByType():
    types = {}
    for nodeType in getAllNodeTypes():
        types[nodeType] = 0
    for node in getAllNodes():
        types[node.Class()] = types[node.Class()] + 1
    return types

    