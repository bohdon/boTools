"""
The template View class.
"""

__version__ = '0.2.0'

import logging
from pymel.core import *

logger = logging.getLogger('View')
logger.setLevel(logging.DEBUG)


class View(object):
    """Template class for a View object of the GUI.
    
    Views mainly consist of a frameLayout containing any controls
    and their corresponding methods.
    
    showView wraps the gui's showView so that views can change views.
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
        self.viewItemHeight = 34
        self.frameItemWidth = 90
    
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
            if view == self.name:
                button(btns[i], e=True, bgc=[.86, .86, .86])
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
    def viewItem(self, l, view, ann='', bgc=[.25, .25, .25], en=True):
        """Create a button used to link to another view"""
        btn = button(l=l, c=Callback(self.showView, view), ann=ann, h=self.viewItemHeight, bgc=bgc, en=en)
    
    def frameItem(self, l, c, ann='', bgc=None, en=True):
        """Create a small frame with no label and a button with a description"""
        with frameLayout(lv=False, mw=4, mh=4, bs='etchedIn'):
            with formLayout(nd=100, en=en) as form:
                btn = button(l=l, c=c, ann=ann, w=self.frameItemWidth)
                if bgc != None:
                    button(btn, e=True, bgc=bgc)
                txt = text(l=ann, al='center')
            formLayout(form, e=True, af=[(btn, 'top', 0), (btn, 'left', 0), (btn, 'right', 0), (txt, 'left', 0), (txt, 'right', 0), (txt, 'bottom', 0)], ac=[(txt, 'top', 4, btn)])
    
    def showView(self, view):
        """Wraps the showView method of the gui"""
        self.gui.showView(view)



