

import logging
from pymel.core import *

LOG = logging.getLogger('Nuke Cam Exporter')
LOG.setLevel(logging.DEBUG)


def doIt(filename):
    dumpSelectedCamToFile(filename)


def dumpSelectedCamToFile(filename, st=None, et=None):
    with open(filename, 'wb') as fp:
        chanData, fl, hfa, vfa = dumpCameraChan(selected()[0], fp)
    LOG.debug('Focal Length, HFA, VFA: {0}, {1}, {2}'.format(fl, hfa, vfa))


def dumpCameraChan(cam, fp, st=None, et=None):
    if st is None:
        st = playbackOptions(q=True, ast=True)
    if et is None:
        et = playbackOptions(q=True, aet=True)
    chanData, fl, hfa, vfa = getCameraChanData(cam, st, et)
    writeChanFile(chanData, fp)
    return chanData, fl, hfa, vfa


def getCameraChanData(cam, st, et):
    data = []
    
    camShape = None
    if nodeType(cam) == 'transform':
        camShape = cam.getShape()
    else:
        camShape = cam
        cam = camShape.getParent()
    LOG.debug('camera: {0}, {1}'.format(cam, camShape))
    
    fl, hfa, vfa = getLensAttrs(camShape)
    
    storeTime = currentTime()
    refresh(su=True)
    currentTime(st)
    while currentTime() < et:
        item = [currentTime()]
        item.extend(xform(q=True, ws=True, a=True, t=True))
        item.extend(xform(q=True, ws=True, a=True, ro=True))
        data.append(item)
        currentTime(currentTime()+1)
    refresh(su=False)
    currentTime(storeTime)
    return data, fl, hfa, vfa


def writeChanFile(chanData, fp):
    contents = '\n'.join(['\t'.join([str(subitem) for subitem in item]) for item in chanData])
    LOG.debug(contents)
    fp.write(contents)
    LOG.debug('Chan Data written to {0}'.format(fp.name))


def getLensAttrs(cam):
    hfa = cam.horizontalFilmAperture.get()
    vfa = cam.verticalFilmAperture.get()
    fl = cam.focalLength.get()
    nhfa = hfa * 25.4
    nvfa = vfa * 25.4
    return fl, nhfa, nvfa



