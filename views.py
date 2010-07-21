"""
All view classes that make up the GUI pages/sections.
"""

__version__ = '0.1.5'

import logging
from pymel.core import *

logger = logging.getLogger('Views')
logger.setLevel(logging.DEBUG)


class View(object):
    """Template class for a View object of the boTools GUI.
    
    Views mainly consist of a frameLayout containing any controls
    and their corresponding methods.
    
    showView is provided as a convenience for control commands
    to change views.
    other methods are provided for creating common controls/layouts.
    """
    
    def __init__(self, parent, gui):
        """Initiate the view's main variables.
        self.parent -> a reference of the form in which the
        view is contained for attachment purposes.
        self.gui -> a reference of the GUI class that
        created the view to allow changing of views from views"""
        self.parent, self.gui = parent, gui
        self.name = self.__class__.__name__
    
    def create(self):
        """Create layout here"""
        logger.debug('Creating %s' % self.name)
        pathLayout = None
        with self.parent:
            with formLayout(nd=100) as self.layout:
                with frameLayout('%sHeadFrame' % self.name, lv=False, bs='out') as self.headFrame:
                    with formLayout(nd=100, bgc=[0.2, 0.2, 0.2]) as self.headForm:
                        self.headContent()
                with frameLayout('%sFrame' % self.name, lv=False, bs='out', mw=4, mh=4) as self.frame:
                    self.content()
                formLayout(self.layout, e=True, af=[(self.headFrame, 'top', 0), (self.headFrame, 'left', 0), (self.headFrame, 'right', 0)])
                formLayout(self.layout, e=True, af=[(self.frame, 'left', 0), (self.frame, 'right', 0), (self.frame, 'bottom', 0)])
                formLayout(self.layout, e=True, ac=[(self.frame, 'top', 0, self.headFrame)])
        self.attachViewForm(self.parent, self.layout, 2)
    
    def headContent(self):
        """Create buttons in the view header for access to other views.
        If a custom header is desired this method should be overwritten."""
        btns = []
        path = self.getPath()
        for i in range(0, len(path)):
            name, view = path[i]
            btns.append( button(l=name, c=Callback(self.showView, view), h=18) )
            if i == 0:
                formLayout(self.headForm, e=True, af=[(btns[i], 'left', 0)])
            else:
                formLayout(self.headForm, e=True, ac=[(btns[i], 'left', 2, btns[i-1])]) 
    
    def getPath(self):
        """Return a tuple list of the current view's path.
        ex. [('Main', 'Main'), ('Basic', 'BasicMain')]"""
        return []
    
    def content(self):
        """Create the content of the view"""
        pass
    
    def hide(self):
        """Hide the view"""
        self.layout.setVisible(False)
    
    def show(self):
        """Show the view"""
        self.layout.setVisible(True)
    
    def attachViewForm(self, form, layout, margin):
        formLayout(form, e=True, af=[(layout, 'top', 2), (layout, 'left', 2), (layout, 'right', 2), (layout, 'bottom', 2)])
    
    #special methods for quickly creating common controls/layouts
    def frameItem(self, name, command, description='', bgc=None, enabled=True):
        """Create a small frame with no label and a button with a description"""
        with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
            with formLayout(nd=100) as form:
                btn = button(l=name, c=command, ann=description, w=90)
                if bgc != None:
                    button(btn, e=True, bgc=bgc)
                txt = text(l=description, al='left')
            formLayout(form, e=True, af=[(btn, 'top', 0), (btn, 'left', 0), (btn, 'bottom', 0), (txt, 'top', 0), (txt, 'right', 0), (txt, 'bottom', 0)], ac=[(txt, 'left', 4, btn)])
    
    def showView(self, view):
        """Wraps the showView method of the main GUI"""
        self.gui.showView(view)





class Main(View):
    """The main view of the GUI.
    Contains several large buttons for accessing other
    feature sections.
    
    Currently sections is hard-coded. Should replace
    with a global list and use a loop to generate the buttons.
    """
    
    def getPath(self):
        return [('Main', 'Main')]
    
    def content(self):
        self.frame.setMarginWidth(20)
        self.frame.setMarginHeight(20)
        
        template = uiTemplate( 'MainTemplate', force=True )
        template.define( button, height=34, align='center' )
        
        with template:
            with columnLayout(adj=True, rs=10):
                button( l='Renaming', c=Callback(self.showView, 'RenamingMain'), bgc=[.25, .25, .25])
                button( l='Reload boTools...', c=self.run_reload)
    
    def run_reload(self, *args):
        import boTools
        reload(boTools)
        reload(boTools.gui)
        reload(boTools.views)
        boTools.GUI()


class RenamingMain(View):
    
    def getPath(self):
        return [('Main', 'Main'), ('Renaming', 'RenamingMain')]
    
    def content(self):
        with columnLayout(adj=True, rs=2) as col1:
            self.frameItem('Inherit Name', Callback(self.inheritNamePrompt), 'Name a node after another node and\nadd a suffix. Select the node to copy\nthen the node to rename.')
            self.frameItem('Comet Rename', Callback(mel.eval, 'cometRename'), 'A basic node renamer include prefixing,\nsuffixing, search and replace and batch renaming.')
    
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
            self.showView('RenamingMain')
        else:
            self.showView('RenamingMain')
    
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



