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
import re

def __humanKey(key):
    # TODO: make this work so that numbered node names are returned in a nicer ways    
    parts = re.split('(\d*\.\d+|\d+)', key)
    return tuple((e.swapcase() if i % 2 == 0 else float(e)) for i, e in enumerate(parts))

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
    nodes = filter(lambda x: x != None, map(lambda node: node if node.Class() == nodeType else None, getAllNodes()))
    return sorted(nodes, key=lambda x: x['name'].value(), reverse = False)

def getNodeDict():
    nodeDict = {}
    for nodeType in getAllNodeTypes():
        nodeDict[nodeType] = getAllNodesByNodeType(nodeType)
    return nodeDict

def getNodeFromNodeName(name):
    return nuke.toNode(name)

def getNodesFromNodeNames(names):
    nodes = []
    for name in names:
        nodes.append(getNodeFromNodeName(name))
    return nodes


    