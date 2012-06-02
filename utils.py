

import pymel.core as pm
import logging

LOG = logging.getLogger(__name__)


def simpleFilter(objs, filters):
    """Return a list of objs whose names contain a simple string"""
    if type(filters) != list:
        filters = [filters]
    result = []
    for obj in objs:
        for f in filters:
            if f in obj.name():
                result.append(obj)
    return result

def filterSelection(filters):
    """Return a list of the selected items that contain the given filter strings"""
    result = simpleFilter(pm.selected(), filters)
    return result

def filterSelectionPrompt():
    result = pm.promptDialog(t='Filter Selection', m='Filters (space separated):', b=['Ok', 'Cancel'], cb='Cancel')
    if result == 'Ok':
        filterStr = pm.promptDialog(q=True)
        filters = filterStr.split()
        pm.select(filterSelection(filters))



def lsAttr(attr, value=None, objs=None, returnAttrs=True, **kwargs):
    """Return all objects within `objs` that have the
    attribute `attr`. If `value` is set, the attribute
    must be of that value. `returnAttrs` determines whether to
    return the objects or the attributes themselves."""
    if objs is None:
        objs = pm.ls(**kwargs)
    results = []
    for obj in objs:
        if hasattr(obj, attr):
            objAttr = getattr(obj, attr)
            if value is None:
                if returnAttrs:
                    results.append(objAttr)
                else:
                    results.append(obj)
            elif objAttr.get() == value:
                if returnAttrs:
                    results.append(objAttr)
                else:
                    results.append(obj)
    return results



def getObjectPairs(objs, method='firstLast'):
    """Return a list of tuples that associate objects
    by their position in the given list.
    method -> 'everyOther' or 'firstLast'
        The method to use for associating objects.
            firstLast: Associate objects by splitting the list in half and pairing same indeces
            everyOther: Associate objects by pairing up every other object"""
    if len(objs) % 2 != 0:
        LOG.error('getObjectPairs : The given object list contains an odd number of objects. Must be even.')
        return
    
    pairs = []
    half = len(objs) / 2
    if method == 'firstLast':
        pairs = zip(objs[:half], objs[half:])
    
    if method == 'everyOther':
        for i in range(half):
            pairs.append( (objs[i*2], objs[i*2+1]) )
    
    return pairs


def copyPivot(objA, objB, scalePivot=True, rotatePivot=True):
    """Copy the pivots of objA to objB"""
    if scalePivot:
        sp = pm.xform(objA, q=True, a=True, ws=True, sp=True)
        pm.xform(objB, a=True, ws=True, sp=sp)
    if rotatePivot:
        rp = pm.xform(objA, q=True, a=True, ws=True, rp=True)
        pm.xform(objB, a=True, ws=True, rp=rp)

def copyPivotSelected():
    """Copy the pivots of the first selected item to all the rest"""
    selList = pm.selected()
    if selList >= 2:
        objA = selList[0]
        objBs = selList[1:]
        for objB in objBs:
            copyPivot(objA, objB)


def printSelection(longNames=True):
    """Print the selection in an organized, numbered list"""
    selList = pm.selected()
    print '\n//{0} Nodes Selected'.format(len(selList))
    nameMethod = None
    if longNames:
        nameMethod = 'longName'
    else:
        nameMethod = 'name'
    
    maxLen = 0
    for obj in selList:
        if hasattr(obj, nameMethod):
            name = getattr(obj, nameMethod)()
        else:
            name = obj.name()
        if len(name) > maxLen:
            maxLen = len(name)
    
    for i in range(len(selList)):
        obj = selList[i]
        typ = pm.nodeType(obj)
        if hasattr(obj, nameMethod):
            name = getattr(obj, nameMethod)()
        else:
            name = obj.name()
        print '{index:03}. {name:<{maxLen}} - {type}'.format(index=i, name=name, type=typ, maxLen=maxLen)


def printCons(node):
    inCons = node.inputs(connections=True, plugs=True)
    outCons = node.outputs(connections=True, plugs=True)
    print '\n# Connections for {0}:'.format(node)
    for outAttr, inAttr in inCons:
        print '{0} -> {1}'.format(outAttr, inAttr)
    for inAttr, outAttr in outCons:
        print '{0} -> {1}'.format(outAttr, inAttr)
    inLen = len(inCons)
    outLen = len(outCons)
    print '{0} inputs, {1} outputs'.format(inLen, outLen)
    

