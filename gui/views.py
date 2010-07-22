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
        with columnLayout(adj=True, rs=15):
            self.viewItem( l='Renaming', view='RenamingMain')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('Lock File Paths', c=lambda x:x, ann='Lock selected File Texture paths.\nAlso converts all paths to relative.\n(Select none for all file textures)')
                    button('Unlock File Paths', c=lambda x:x, ann='Unlock selected File Texture paths.\n(Select none for all file textures)')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('Find PSDs', c=lambda x:x, ann='Find all PSD file textures and\npsdFileTex nodes (Used for RenderMan).')
                    button('Find Multi-Shader', c=lambda x:x, ann='Find shapes that have more than\none material assigned.')
            with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
                with columnLayout(adj=True, rs=4):
                    button('Delete Light-Cameras', c=lambda x:x, ann='Delete all cameras in the scene that\nwere created by looking through lights.')
                    button('Delete Extra Panels', c=lambda x:x, ann='Delete extra model panels from the\nscene. (Panels without names).')


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



