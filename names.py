

import os, logging
from pymel.core import *
import boTools
from boTools import utils

LOG = boTools.getLogger('Names')



def inheritNamePrompt(parentWin=None):
    """Run inheritName by using a promptDialog first"""
    pairs = utils.getObjectPairs(selected())
    msgChunks = []
    for a, b in pairs:
        msgChunks.append('{0} -> {1}'.format(a, b))
    msgChunks.append('Suffix:')
    msg = '\n'.join(msgChunks)
    
    promptKw = {
        't':'Inherit Name...',
        'm':msg,
        'ma':'center',
        'b':['Rename', 'Cancel'],
        'db':'Rename',
        'cb':'Cancel'
    }
    if parentWin is not None:
        promptKw['p']=parentWin
    result = promptDialog(**promptKw)
    if result == 'Rename':
        suffix = promptDialog(q=True, tx=True)
        inheritNamePairs(pairs, suffix=suffix)
    
def inheritNamePairs(pairs, prefix=None, suffix=None):
    """Run inheritName on a series of (a, b) pairs"""
    for a, b in pairs:
        inheritName(a, b, prefix, suffix)

def inheritName(objA, objB, prefix=None, suffix=None):
    """Rename objB to '<prefix>objA<suffix>'"""
    name = objA
    if prefix is not None:
        name = prefix + name
    if suffix is not None:
        name = name + suffix
    LOG.debug('{0} -> {1}'.format(objB, name))
    nsRename(objB, name)




def createNamespace(ns, p=None):
    if p is None:
        if not namespace(exists=ns):
            namespace(add=ns)
    else:
        fullns = '{0}:{1}'.format(p, ns)
        if not namespace(exists=fullns):
            namespace(add=ns, p=p)

def createNestedNamespaces(nsList):
    """Create namespaces in the given list, parenting
    each namespaces to the previous one.
    
    ie. ['first', 'second', 'third'] -> first:second:third:
    """
    for i in range(len(nsList)):
        if i == 0:
            createNamespace(nsList[i])
        else:
            p = ':'.join(nsList[0:i])
            createNamespace(nsList[i], p)
    return True

def nsRename(obj, newName, **kwargs):
    """Rename the given object creating namespaces as needed"""
    obj = PyNode(str(obj))
    if obj.name() == newName:
        return
    if obj.isReadOnly() or obj.isReferenced():
        LOG.error('Cannot rename read-only or referenced object: {0}'.format(obj))
        return
    if ':' in newName:
        nsList = newName.split(':')[:-1]
        createNestedNamespaces(nsList)
    
    rename(obj, newName, **kwargs)


def stripFirstNamespace(objs):
    """Rename all the given objects to exclude their primary
    namespace. Use nsRename to ensure namespaces
    are created as necessary"""
    for obj in objs:
        if ':' in obj.name():
            newName = ':'.join( obj.name().split(':')[1:] )
            LOG.debug('{0} -> {1}'.format(obj, newName))
            nsRename(obj, newName)




def getSelectedNamespaces():
    """Return the first namespace of the selected objects"""
    return getNamespaces(selected())

def getNamespaces(nodes):
    """Return the first namespace of the given object"""
    nsList = []
    for node in nodes:
        ns = getNamespace(node)
        if ns not in nsList:
            nsList.append(ns)
    nsList.sort()
    return nsList

def getNamespace(node):
    """Return the first namespace of the given object"""
    nsPat = re.compile('[^:]*(?=:)')
    m = nsPat.match(node.name())
    ns = None
    if m is not None:
        ns = m.group()
    return ns

def hasReferencedNamespace(node):
    """Return true if the given node has the
    same namespace as a reference in the scene."""
    result = False
    ns = getNamespace(node)
    refs = ls(references=True)
    refNsList = []
    for ref in refs:
        refNsList.extend(ref.namespaceList())
    if ns in refNsList:
        result = True
    return result



