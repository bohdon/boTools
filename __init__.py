"""
    Bo Tools
    
    Copyright (C) 2010 Bohdon Sayre
    All Rights Reserved.
    bo@bohdon.com
    
    Description:
        A suite of tools for use in Maya.
    
    Dependencies:
        pymel
        boViewGui
    
    Usage:
        >>> import boTools
        >>> boTools.Gui()
"""

import os, logging
__version__ = '0.2.12'
__author__ = 'Bohdon Sayre'

__LOG_LEVEL__ = logging.DEBUG

def getLogger(name=''):
    logname = '{0} : {1}'.format('Bo Tools', name)
    log = logging.getLogger(logname)
    log.setLevel(__LOG_LEVEL__)
    return log


def Gui():
    """Wrap gui.GUI as GUI for convenience"""
    import gui
    gui.Gui()



def devReload():
    import boTools
    reload(boTools)
    import boTools.gui
    reload(boTools.gui)
    import boTools.views
    reload(boTools.views)
    import boTools.names
    reload(boTools.names)
    import boTools.utils
    reload(boTools.utils)
    import boTools.nukeCam
    reload(boTools.nukeCam)
    import boTools.polyUtils
    reload(boTools.polyUtils)