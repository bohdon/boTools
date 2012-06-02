

from pymel.core import *
import logging
import os

LOG = logging.getLogger(__name__)


INCH_TO_MM = 25.4


def dumpCameraAuto(camera=None, fileName=None, st=None, et=None):
    #auto retrieve camera
    if camera is None:
        selList = selected()
        if len(selList) == 0:
            LOG.error('No camera was provided, and no camera was selected.')
            return
        camera = selList[0]
    
    #auto retrieve fileName
    if fileName is None:
        fileName = fileDialog2(fm=0, ff='*.chan')
        if fileName is None:
            LOG.warning('Operation cancelled by user.')
            return
        fileName = fileName[0]
    base, ext = os.path.splitext(fileName)
    fileName = '{0}.chan'.format(base)
    
    #auto retrieve animation range
    if st is None:
        st = playbackOptions(q=True, ast=True)
    if et is None:
        et = playbackOptions(q=True, aet=True)
    
    with open(fileName, 'wb') as fp:
        dumpCamera(camera, fp, st, et)


def dumpCamera(cam, fp, st=None, et=None):
    chanData, fl, hfa, vfa = getCameraData(cam, st, et)
    writeChanFile(chanData, fp)
    LOG.info('Apply these settings to the Nuke camera: Focal Length:{0}, HFA:{1}, VFA:{2}'.format(fl, hfa, vfa))
    return chanData, fl, hfa, vfa


def getCameraData(cam, st, et):
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
    LOG.info('Chan file written to {0}'.format(fp.name))


def getLensAttrs(cam):
    hfa = cam.horizontalFilmAperture.get()
    vfa = cam.verticalFilmAperture.get()
    fl = cam.focalLength.get()
    nhfa = hfa * INCH_TO_MM
    nvfa = vfa * INCH_TO_MM
    return fl, nhfa, nvfa


