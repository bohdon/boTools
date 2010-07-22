"""
The GUI class.
"""

__version__ = '0.1.8'

import logging, inspect
import view, views
from pymel.core import *


logger = logging.getLogger('GUI')
logger.setLevel(logging.DEBUG)

#compile the view dict
classes = inspect.getmembers(views, inspect.isclass)
#get all view classes except for the template
VIEWS = dict( [c for c in classes if issubclass(c[1], views.View) and c[0] != 'View'] )
logger.debug('Views: %s' % (VIEWS.keys()) )


class GUI(object):
    """
    A dynamic GUI class based on pages (views).
    
    The window is designed specially, where the layout rebuilds
    based on the current view.  This eliminates the clutter
    of having tabs while still allowing many sections of features.
    
    The Main view usually provides links to all other
    feature sections.
    """
    
    def __init__(self):
        self.title = 'Bo Tools %s' % __version__
        self.curView = 'Main'
        self.views = VIEWS 
        self.win = None
        self.winName = 'btoolWin'
        self.mainForm = None
        
        self.create()
    
    def create(self):
        logger.debug('Creating GUI...')
        if window(self.winName, ex=True):
            deleteUI(self.winName)
        
        if windowPref(self.winName, ex=True):
            windowPref(self.winName, e=True, w=240)
        with window(self.winName, w=240, title=self.title) as self.win:
            with formLayout('mainForm', nd=100) as self.mainForm:
                #build the current view
                self.createViews()
                #display the current view
                self.showView(self.curView)
                #show the window (end with statement)
    
    def createViews(self):
        """Create all available views of the window.
        This should be run only once per instance of the GUI."""
        for view in self.views.keys():
            #create instance of the view
            self.views[view] = getattr(views, view)( self.mainForm, self )
            #create the views controls/layouts
            self.views[view].create()
            #start the view hidden
            self.views[view].hide()
    
    def showView(self, view):
        if view in self.views:
            self.curView = view
            for loopView in self.views.keys():
                if loopView == view:
                    self.views[loopView].show()
                else:
                    self.views[loopView].hide()

