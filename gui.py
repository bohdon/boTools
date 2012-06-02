"""
Bo Tools - Gui

Dependencies:
    boViewGui
"""

from pymel.core import *
import boViewGui.gui
import logging
import views

LOG = logging.getLogger(__name__)

VERSION = 0.0
VIEWS = views.VIEWS
WIN_NAME = 'boToolsWin'

def Gui():
    g = boViewGui.gui.Gui()
    g.title = 'Bo Tools {0}'.format(VERSION)
    g.winName = WIN_NAME
    g.metrics['w'] = 290
    g.metrics['h'] = 500
    g.defaultView = views.DEFAULT_VIEW
    g.views = VIEWS
    g.create()
    del g

