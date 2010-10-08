

from pymel.core import *
import boTools

LOG = boTools.getLogger('Utils')


def simpleFilter(objs, filters):
    """Return a list of objs whose names contain a simple string"""
    result = []
    for obj in objs:
        for f in filters:
            if f in obj.name():
                result.append(obj)
    return result

def filterSelection(filters):
    """Return a list of the selected items that contain the given filter strings"""
    result = simpleFilter(selected(), filters)
    return result

def filterSelectionPrompt():
    result = promptDialog(t='Filter Selection', m='Filters (space separated):', b=['Ok', 'Cancel'], cb='Cancel')
    if result == 'Ok':
        filterStr = promptDialog(q=True)
        filters = filterStr.split()
        select(filterSelection(filters))



def lsAttr(attr, value=None, objs=None, returnAttrs=True, **kwarg):
    """Return all objects within `objs` that have the
    attribute `attr`. If `value` is set, the attribute
    must be of that value. `returnAttrs` determines whether to
    return the objects or the attributes themselves."""
    if objs is None:
        objs = ls(**kwarg)
    results = []
    for obj in objs:
        if hasattr(obj, attr):
            if value is None:
                if returnAttrs:
                    results.append(getattr(obj, attr))
                else:
                    results.append(obj)
            elif getattr(obj, attr).get() == value:
                if returnAttrs:
                    results.append(getattr(obj, attr))
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



def printSelection(longNames=True):
    """Print the selection in an organized, numbered list"""
    selList = selected()
    print '\n//{0} Nodes Selected'.format(len(selList))
    nameMethod = None
    if longNames:
        nameMethod = 'longName'
    else:
        nameMethod = 'name'
    
    maxLen = 0
    for obj in selList:
        name = getattr(obj, nameMethod)()
        if len(name) > maxLen:
            maxLen = len(name)
    
    for i in range(len(selList)):
        typ = nodeType(obj)
        name = getattr(selList[i], nameMethod)()
        print '{index:03}. {name:<{maxLen}} - {type}'.format(index=i, name=name, type=typ, maxLen=maxLen)





