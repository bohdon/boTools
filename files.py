

import pymel.core as pm
import logging
import os
import sys

LOG = logging.getLogger(__name__)
CLEANLOG = logging.getLogger('Maya')

MAYA_EXTS = ['ma', 'mb']

def saveAsciiAndBinary(binaryFirst=True, applyInfo=False):
    """Saves the current scene as both .ma and .mb"""
    if binaryFirst: saveBinary(applyInfo=applyInfo)
    saveAscii(applyInfo=applyInfo)
    if not binaryFirst: saveBinary(applyInfo=applyInfo)

def saveAscii(applyInfo=False):
    """Save the current scene as an ascii file"""
    save(ext='ma', applyInfo=applyInfo)

def saveBinary(applyInfo=False):
    """Save the current scene as a binary file"""
    save(ext='mb', applyInfo=applyInfo)

def save(fileName=None, ext=None, applyInfo=False, mayaExts=MAYA_EXTS):
    """A wrapper for cmds.file(s=True) for convenience"""
    saveName = fileName
    if saveName is None:
        saveName = pm.sceneName()
        if 'untitled' in saveName:
            LOG.warning('The current scene has not yet been saved.')
            return None
    if ext is not None:
        if ext not in mayaExts:
            LOG.error('The provided file type `{0}` is not valid.'.format(ext))
            return None
        saveName = forceExt(saveName, ext)
    
    if applyInfo:
        setFileInfo()
    result = pm.saveAs(saveName)
    CLEANLOG.info('Result: {0}'.format(result))


def forceExt(path, ext):
    """Return the path with the given extension"""
    base = os.path.splitext(path)[0]
    if '.' in ext:
        ext.replace('.', '')
    newPath = '{0}.{1}'.format(base, ext)
    return newPath


def setFileInfo():
    """Apply common file info to the current file"""
    pm.fileInfo['lastUser'] = pm.env.user()


def importAllReferences(loadUnloaded=True, force=False, depthLimit=10):
    """Recursively import all references in the scene"""
    if not force:
        if not importAllReferencesConfirm():
            return False
    
    i = 0
    while getFileReferences() != []:
        fileRefs = getFileReferences()
        for f in fileRefs:
            fileName = str(f)
            if isTopLevelReference(fileName): 
                if not f.isLoaded():
                    if loadUnloaded:
                        f.load(loadReferenceDepth='all')
                    else:
                        continue
                try:
                    f.importContents()
                    LOG.info('Imported Reference: {0}'.format(fileName))
                except RuntimeError, e:
                    LOG.warning('Could not import reference: {0}\n{1}'.format(fileName, e))
            else:
                LOG.debug('Skipping non-top level reference: {0} {1}'.format(f.refNode, f))
        
        i += 1
        if i > depthLimit:
            break
    
    return True

def importAllReferencesConfirm():
    confirmKw = {
        't':'Import All References',
        'm':'This action is not undoable.\nContinue?',
        'b':['OK', 'Cancel'],
        'cb':'Cancel',
        'ds':'dismiss',
        'icn':'warning',
    }
    result = pm.confirmDialog(**confirmKw)
    if result != 'OK':
        return False
    return True

def getFileReferences():
    """Return a list of the referenced files in the current scene"""
    refNodes = pm.ls(rf=True)
    if refNodes == []:
        return []
    
    fileRefs = []
    for ref in refNodes:
        fileRefs.append(ref.referenceFile())
    
    return fileRefs

def isTopLevelReference(fileName):
    """Returns True if the given fileName represents a top level reference node"""
    refNode = pm.referenceQuery(fileName, rfn=True)
    topRefNode = pm.referenceQuery(fileName, rfn=True, tr=True)
    if refNode == topRefNode:
        return True
    else:
        return False




