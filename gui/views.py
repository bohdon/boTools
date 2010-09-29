"""
All view classes that make up the boTools gui.
"""

__version__ = '0.2.0'

import logging
from view import View
from pymel.core import *

logger = logging.getLogger('Views')
logger.setLevel(logging.DEBUG)


class Main(View):
    """The main view of the GUI.
    Contains several large buttons for accessing other
    feature sections.
    
    Currently sections is hard-coded. Should replace
    with a global list and use a loop to generate the buttons.
    """
    
    def getPath(self):
        return [('Main', self.name)]
    
    def content(self):
        self.frame.setMarginWidth(20)
        self.frame.setMarginHeight(20)
        
        with columnLayout(adj=True, rs=10):
            self.viewItem( l='Organizing', view='OrganizingMain')
            self.viewItem( l='Modeling', view='ModelingMain')
            self.viewItem( l='Rendering', view='RenderingMain')
            self.viewItem( l='Misc', view='MiscMain')
            button( l='Reload boTools...', c=self.run_reload)
    
    def run_reload(self, *args):
        import boTools
        reload(boTools)
        reload(boTools.gui)
        reload(boTools.gui.gui)
        reload(boTools.gui.views)
        boTools.GUI()


class OrganizingMain(View):
    
    def getPath(self):
        return [('Main', 'Main'), ('Organizing', self.name)]
    
    def content(self):
        self.frameItemWidth = 115
        template = uiTemplate('OrganizingMainTemplate', force=True)
        template.define(frameLayout, lv=False, mw=4, mh=4, bs='etchedIn')
        template.define(columnLayout, adj=True, rs=4)
        with template:
            with columnLayout(rs=15):
                self.viewItem( l='Renaming', view='RenamingMain')
                with frameLayout():
                    with columnLayout():
                        button('Lock File Paths', c=lambda x:x, ann='Lock selected File Texture paths.\nAlso converts all paths to relative.\n(Select none for all file textures)')
                        button('Unlock File Paths', c=lambda x:x, ann='Unlock selected File Texture paths.\n(Select none for all file textures)')
                with frameLayout():
                    with columnLayout():
                        button('Find PSDs', c=lambda x:x, ann='Find all PSD file textures and\npsdFileTex nodes (Used for RenderMan).')
                        button('Find Multi-Shader', c=lambda x:x, ann='Find shapes that have more than\none material assigned.')
                with frameLayout():
                    with columnLayout():
                        button('Delete Light-Cameras', c=lambda x:x, ann='Delete all cameras in the scene that\nwere created by looking through lights.')
                        button('Delete Extra Panels', c=lambda x:x, ann='Delete extra model panels from the\nscene. (Panels without names).')
                        button('Delete Display Layers', c=Callback(self.deleteDisplayLayers), ann='Delete all display layers in the\nscene. Referenced layers cannot be removed.')
                        button('Delete Render Layers', c=Callback(self.deleteRenderLayers), ann='Delete all render layers in the\nscene. Referenced layers cannot be removed.')
    
    def deleteDisplayLayers(self):
        """Delete all display layers in the
        current scene.
        TODO: automatically remove reference edits
        if the scenes display layer was overriding
        a referenced display layer"""
        layerList = ls(typ='displayLayer')
        for layer in layerList:
            if layer != nt.DisplayLayer('defaultLayer'):
                try:
                    delete(layer)
                except:
                    cons = layer.listConnections(c=True, p=True)
                    for con in cons:
                        try: con[0] // con[1]
                        except: pass
                    delete(layer)
    
    def deleteRenderLayers(self):
        """Delete all render layers except the master layer"""
        editRenderLayerGlobals(crl=nt.RenderLayer('defaultRenderLayer'))
        layerList = ls(typ='renderLayer')
        for layer in layerList:
            if layer != nt.RenderLayer('defaultRenderLayer'):
                try:
                    delete(layer)
                except:
                    cons = layer.listConnections(c=True, p=True)
                    for con in cons:
                        try: con[0] // con[1]
                        except: pass
                    delete(layer)


class RenamingMain(View):
    def getPath(self):
        return [('Main', 'Main'), ('Organizing', 'OrganizingMain'), ('Renaming', self.name)]
    
    def content(self):
        with columnLayout(adj=True, rs=15):
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('Inherit Name', c=Callback(self.inheritNamePrompt), ann='Name a node after another node and\nadd a suffix. Select the node to copy\nthen the node to rename.')
                    button('Comet Rename', c=Callback(mel.eval, 'cometRename'), ann='A basic node renamer include prefixes,\nsuffixes, search, replace and batch rename.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('Auto-Name File Textures', c=lambda x:x, ann='Rename selected file textures based\non the names of the images they use.')
                    button('Auto-Name Shading Groups', c=lambda x:x, ann='Rename selected shading groups based\non the names of the materials\nthat they belong to.')
    
    def inheritNamePrompt(self):
        pairs = self.getPairs()
        print pairs
        msg = ''
        for a, b in pairs:
            msg += '%s -> %s\n' % (a, b)
        msg += 'Suffix'
        result = promptDialog(t='Inherit Name...', m=msg, ma='center', p=self.gui.win, b=['Rename', 'Cancel'], db='Rename', cb='Cancel')
        if result == 'Rename':
            suffix = promptDialog(q=True, tx=True)
            self.inheritName(suffix)
            self.showView(self.name)
        else:
            self.showView(self.name)
    
    def inheritName(self, suffix):
        pairs = self.getPairs()
        for a, b in pairs:
            rename(b, '%s%s' % (a, suffix))
    
    def getPairs(self):
        pairs = []
        selList = ls(sl=True)
        if len(selList) % 2 == 0:
            i = len(selList) / 2
            pairs = zip(selList[:i], selList[i:])
        return pairs


class ModelingMain(View):
    def getPath(self):
        return [('Main', 'Main'), ('Modeling', self.name)]
    
    def content(self):
        self.frameItemWidth = 115
        with columnLayout(adj=True, rs=15):
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('Batch UV Snapshots', c=lambda x:x, ann='Tool for taking UV snapshots on\nseveral objects at once.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('Get Vertex Distance', c=lambda x:x, ann='Return the distance between two points\nSelect two points.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                self.vertsABtn = button('Get Verts A', c=Callback(self.getVertsA), ann='')
                self.vertsBBtn = button('Get Verts B', c=Callback(self.getVertsB), ann='')
                button('Associate Verts', c=Callback(self.assocVerts), ann='')
                button('Snap Associated Verts', c=Callback(self.snapVerts), ann='')
                self.progBar = progressBar()
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('UV Texture', c=Callback(self.assignUVTexture))
    
    def assignUVTexture(self):
        fileTex = shadingNode('file', asTexture=True)
        place2d = shadingNode('place2dTexture', asUtility=True)
        place2d.coverage >> fileTex.coverage
        place2d.translateFrame >> fileTex.translateFrame
        place2d.rotateFrame >> fileTex.rotateFrame
        place2d.mirrorU >> fileTex.mirrorU
        place2d.mirrorV >> fileTex.mirrorV
        place2d.stagger >> fileTex.stagger
        place2d.wrapU >> fileTex.wrapU
        place2d.wrapV >> fileTex.wrapV
        place2d.repeatUV >> fileTex.repeatUV
        place2d.offset >> fileTex.offset
        place2d.rotateUV >> fileTex.rotateUV
        place2d.noiseUV >> fileTex.noiseUV
        place2d.vertexUvOne >> fileTex.vertexUvOne
        place2d.vertexUvTwo >> fileTex.vertexUvTwo
        place2d.vertexUvThree >> fileTex.vertexUvThree
        place2d.vertexCameraOne >> fileTex.vertexCameraOne
        place2d.outUV >> fileTex.uv
        place2d.outUvFilterSize >> fileTex.uvFilterSize
        place2d.repeatU.set(4)
        place2d.repeatV.set(4)
        fileTex.outColor >> SCENE.lambert1.color
        setAttr('%s.fileTextureName' % fileTex, 'sourceimages/outUV/uvTexture.jpg', typ='string')
    
    def getVertsA(self):
        self.vertsA = ls(fl=True, sl=True)
        self.vertsABtn.setLabel('Get Verts A (%d)' % len(self.vertsA))
    
    def getVertsB(self):
        self.vertsB = ls(fl=True, sl=True)
        self.vertsBBtn.setLabel('Get Verts B (%d)' % len(self.vertsB))
    
    def assocVerts(self):
        vp = VertexPairs(self.vertsA, self.vertsB, True, False)
        vp.run(self.progBar)
    
    def snapVerts(self):
        vp = VertexPairs(self.vertsA, self.vertsB, False, True, True)
        vp.run(self.progBar)
        

class VertexPairs(object):
    import math
    
    def __init__(self, vts1, vts2, curves=False, snap=False, interactive=False):
        self.vts1, self.vts2, self.curves, self.snap, self.interactive = vts1, vts2, curves, snap, interactive
    
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


class RenderingMain(View):
    
    def getPath(self):
        return [('Main', 'Main'), ('Rendering', self.name)]
    
    def content(self):
        self.frameItemWidth = 140
        with columnLayout(adj=True, rs=15):
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('Render Stats', c=lambda x:x, ann='GUI for setting render stats\non multiple objects at once.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('Z-Depth Shader', c=lambda x:x, ann='Tool for creating Z-Depth shaders\nfor all objects in the scene.\nPreserves displacement and transparency textures.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('Batch File Maker', c=lambda x:x, ann='Tool for creating render bat files\nquickly and easily. Includes functions\nfor distributing frame ranges among files.')
                    button('Frame Checker', c=lambda x:x, ann='Tool to check an image sequence\nfor missing files.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('nCloth Pre-Roll', c=lambda x:x, ann='Tool for pre-rolling nCloth shapes\nin order to easily create initial states.')
                    button('Setup Pre-Render nCloth', c=lambda x:x, ann='Causes all nCloths in the scene to\nbe cached before every render.')
                    button('Remove Pre-Render nCloth', c=lambda x:x, ann='Removes nCloth caching feature.')


class MiscMain(View):
    def getPath(self):
        return [('Main', 'Main'), ('Misc', self.name)]
    
    def content(self):
        pass



