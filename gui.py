"""
Bo Tools - Gui

Dependencies:
    viewGui
"""

from pymel.core import *
import viewGui.gui
import logging
import views

LOG = logging.getLogger(__name__)

VERSION = 0.0
VIEWS = views.VIEWS
WIN_NAME = 'boToolsWin'

def Gui():
    title = 'Bo Tools {0}'.format(VERSION)
    g = viewGui.Gui(title, WIN_NAME, VIEWS, views.DEFAULT_VIEW, 290, 500)
    g.create()

