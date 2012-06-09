"""
    Bo Tools
    
    Copyright (C) 2010 Bohdon Sayre
    All Rights Reserved.
    bo@bohdon.com
    
    Description:
        A suite of tools for use in Maya.
    
    Dependencies:
        pymel
        viewGui
    
    Usage:
        >>> import boTools
        >>> boTools.Gui()
"""

import logging
import os
import files
import gui
import names
import nukeCam
import polyUtils
import utils
import views

__version__ = '0.2.17'
gui.VERSION = __version__

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

def Gui():
    """Wrap gui.GUI as GUI for convenience"""
    import gui
    gui.Gui()



def devReload():
    LOG.info('devReload is deprecated, please use reloadAll')
    reloadAll()

def reloadAll():
    import boTools
    reload(boTools)
    for mod in (files, gui, names, nukeCam, polyUtils, utils, views):
        reload(mod)
    reload(boTools)