

import os, logging, math
from pymel.core import *
import boTools

LOG = boTools.getLogger('Poly Utils')



class VertexPairs(object):
    """VertexPairs provides a class for associating
    two sets of vertices with each other, from same or different
    objects.  The basic options are to create curves representing
    vertex associations, or to snap vertex set 2 to vertex set 1
    
    >>> vp = VertexPairs(vertsA, vertsB, snap=True)
    >>> vp.run(myProgressBar)
    """
    def __init__(self, vts1, vts2, curves=False, snap=False, interactive=False):
        self.vts1, self.vts2 = vts1, vts2 
        self.curves, self.snap, self.interactive = curves, snap, interactive
    
    def run(self, progBar):
        self.progBar = progBar
        if len(self.vts1) != len(self.vts2):
            error('Vert lists must be the same length')
        self.pairs = self.getVertexPairs()
        print ('%d pairs' % len(self.pairs))
        if self.curves: self.createCurves()
        if self.snap: self.snapVertices()
        
    def getVertexPairs(self):
        vts1 = self.vts1[:]
        vts2 = self.vts2[:]
        vt1Pts, vt2Pts = {}, {}
        pairs = []
        for vt in vts1: vt1Pts[vt] = pointPosition(vt)
        for vt in vts2: vt2Pts[vt] = pointPosition(vt)
        progressBar(self.progBar, e=True, max=len(vts1))
        progressBar(self.progBar, e=True, pr=0)
        for vt1 in vt1Pts.keys():
            pt1 = vt1Pts[vt1]
            pairVt = None
            min = 1000
            for vt2 in vt2Pts.keys():
                pt2 = vt2Pts[vt2]
                d = sum([abs(pt1.x - pt2.x), abs(pt1.y - pt2.y), abs(pt1.z - pt2.z)])
                if d < min:
                    min = d
                    pairVt = vt2
            pair = (vt1, pairVt)
            print ('%s -> %s' % (pair[0], pair[1]))
            pairs.append(pair)
            progressBar(self.progBar, e=True, s=1)
        return pairs
    
    def createCurves(self):
        curves = []
        for pair in self.pairs:
            pts = [pointPosition(pair[0]), pointPosition(pair[1])]
            curves.append(self.createCurve(pts))
        select(group(curves, n='associateVertsCurves_GRP'))
    
    def createCurve(self, pts):
        return curve(d=1, p=pts, k=[0, 1])
    
    def snapVertices(self):
        print 'Snapping vertices...'
        for pair in self.pairs:
            pt1 = pointPosition(pair[0])
            move(pair[1], pt1, a=True, ws=True)
            if self.interactive: refresh()

