"""
All view classes that make up the boTools gui.
"""


from pymel.core import *
import viewGui
import logging
import boTools
import viewGui
import names
import nukeCam
import polyUtils
import utils

LOG = logging.getLogger(__name__)

DEFAULT_VIEW = 'MainView'

class MainView(viewGui.View):
    displayName = 'Main'
    _bodyMargins = (20, 20)
    def links(self):
        return [self.viewName]
    def buildBody(self):        
        with columnLayout(adj=True, rs=10):
            self.viewItem(viewName='NamingView', l='Naming')
            self.viewItem(viewName='CleanupView', l='Cleanup')
            self.viewItem(viewName='ModelingView', l='Modeling')
            self.viewItem(viewName='LightingView', l='Lighting')
            self.viewItem(viewName='RenderingView', l='Rendering')
            self.viewItem(viewName='MiscView', l='Misc')
            self.viewItem(viewName='HotkeyUtils', l='Setup Hotkey Utils', en=False)

class NamingView(viewGui.View):
    displayName = 'Naming'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        with columnLayout(adj=True, rs=15):
            with frameLayout(l='Batch Renaming', mw=4, mh=4, bs='out'):
                with columnLayout(adj=True, rs=4):
                    button('Bo Rename', en=False)
                    button('Inherit Name', c=Callback(self.tool_inheritNamePrompt), ann='Name a node after another node and\nadd a suffix. Select the node to copy\nthen the node to rename.')
                    button('Comet Rename', c=Callback(mel.eval, 'cometRename'), ann='A basic node renamer include prefixes,\nsuffixes, search, replace and batch rename.')
            with frameLayout(l='Namespaces', mw=4, mh=4, bs='out'):
                with columnLayout(adj=True, rs=4):
                    button('Strip First Namespace', c=Callback(self.tool_stripFirstNamespace), ann='Remove the first namespace of all\nthe selected nodes')
            with frameLayout(l='Automatic Naming', mw=4, mh=4, bs='out'):
                with columnLayout(adj=True, rs=4):
                    button('Auto-Name File Textures', c=lambda x:x, ann='Rename selected file textures based\non the names of the images they use.')
                    button('Auto-Name Shading Groups', c=lambda x:x, ann='Rename selected shading groups based\non the names of the materials\nthat they belong to.')
                    button('Auto-Name Shapes', en=False)
    
    def tool_inheritNamePrompt(self):
        from boTools import gui
        names.inheritNamePrompt(gui.WIN_NAME)
    
    def tool_stripFirstNamespace(self):
        names.stripFirstNamespace(selected())

class CleanupView(viewGui.View):
    displayName = 'Cleanup'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        template = uiTemplate('GeneralViewTemplate', force=True)
        template.define(frameLayout, lv=False, mw=4, mh=4, bs='etchedIn')
        template.define(columnLayout, adj=True, rs=4)
        with template:
            with columnLayout(rs=15):
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


class ModelingView(viewGui.View):
    displayName = 'Modeling'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        with columnLayout(adj=True, rs=15):
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('Batch UV Snapshots', c=Callback(sourceAndRunMel, 'boBatchUVSnapshot'), ann='Tool for taking UV snapshots on\nseveral objects at once.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('Get Vertex Distance', c=lambda x:x, ann='Return the distance between two points\nSelect two points.')
            with frameLayout(l='Vertex Pairs', mw=4, mh=4, bs='out'):
                with columnLayout(adj=True, rs=2):
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
        vp = polyUtils.VertexPairs(self.vertsA, self.vertsB, True, False)
        vp.run(self.progBar)
    
    def snapVerts(self):
        vp = polyUtils.VertexPairs(self.vertsA, self.vertsB, False, True, True)
        vp.run(self.progBar)
        

class RenderingView(viewGui.View):
    displayName = 'Rendering'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        with columnLayout(adj=True, rs=15):
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                button('Render Stats', c=Callback(sourceAndRunMel, 'boRenderStats'), ann='GUI for setting render stats\non multiple objects at once.')                
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('Batch File Maker', c=Callback(self.tool_boBatchFileMaker), ann='Tool for creating render bat files\nquickly and easily. Includes functions\nfor distributing frame ranges among files.')
                    button('Frame Checker', c=Callback(self.tool_boFrameChecker), ann='Tool to check an image sequence\nfor missing files.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('nCloth Pre-Roll', c=Callback(sourceAndRunMel, 'boNClothPreroll'), ann='Tool for pre-rolling nCloth shapes\nin order to easily create initial states.')
                    button('Z-Depth Shader', c=Callback(sourceAndRunMel, 'boZDepthShader'), ann='Tool for creating Z-Depth shaders\nfor all objects in the scene.\nPreserves displacement and transparency textures.')
            with frameLayout(l='Nuke Tools', mw=4, mh=4, bs='out'):
                with columnLayout(adj=True, rs=2):
                    button('Export Selected Camera', c=Callback(self.tool_exportNukeCam), ann='Export a .chan file for importing onto\na nuke camera node. Focal Length, HFA, and VFA\nwill be printed to the script editor')
    
    def tool_boBatchFileMaker(self):
        import boBatchFileMaker
        boBatchFileMaker.doIt()
    
    def tool_boFrameChecker(self):
        import boFrameChecker
        boFrameChecker.GUI()
    
    def tool_exportNukeCam(self):
        nukeCam.dumpCameraAuto()


class LightingView(viewGui.View):
    displayName = 'Lighting'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        pass

class MiscView(viewGui.View):
    displayName = 'Misc'
    def links(self):
        return ['MainView', self.viewName]
    
    def buildBody(self):
        pass


def sourceAndRunMel(scriptName):
    mel.eval('source {0}'.format(scriptName))
    getattr(mel, scriptName)()


VIEWS = [
    MainView,
    NamingView,
    CleanupView,
    ModelingView,
    LightingView,
    RenderingView,
    MiscView,
]



