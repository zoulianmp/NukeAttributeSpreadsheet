#!/usr/bin/env python

''' Convenience functions to access nodes/node-info '''

__author__ = 'Manuel Macha'
__copyright__ = 'Copyright 2013, Manuel Macha'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = __author__
__email__ = 'manuel@manuelmacha.de'
__website__ = 'http://www.manuelmacha.de'
__git__ = 'https://github.com/manuelmacha/NukeAttributeSpreadsheet'

import nuke

def getAllNodes():
    return nuke.allNodes()

def getAllNodeTypes():
    nodeTypes = tuple(set(map(lambda node: node.Class(), getAllNodes())))
    return sorted(nodeTypes)

def getNumberOfNodesByType():
    types = {}
    for nodeType in getAllNodeTypes():
        types[nodeType] = 0
    for node in getAllNodes():
        types[node.Class()] += 1
    return types

def getAllNodesByNodeType(nodeType):
    return filter(lambda x: x != None, map(lambda node: node if node.Class() == nodeType else None, getAllNodes()))

def getNodeDict():
    nodeDict = {}
    for nodeType in getAllNodeTypes():
        nodeDict[nodeType] = getAllNodesByNodeType(nodeType)
    return nodeDict


    