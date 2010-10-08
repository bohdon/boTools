"""
Bo Tools - Gui

Dependencies:
    boViewGui
"""

from pymel.core import *
import boTools
from boTools import views
import boViewGui.gui


LOG = boTools.getLogger('Gui')


VIEWS = views.VIEWS
WIN_NAME = 'boToolsWin'

def Gui():
    g = boViewGui.gui.Gui()
    g.title = 'Bo Tools {0}'.format(boTools.__version__)
    g.winName = WIN_NAME
    g.metrics['w'] = 290
    g.metrics['h'] = 500
    g.defaultView = views.DEFAULT_VIEW
    g.views = VIEWS
    g.create()
    del g

