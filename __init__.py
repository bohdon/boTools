"""
    Bo Tools
    
    Copyright (C) 2010 Bohdon Sayre
    All Rights Reserved.
    bo@bohdon.com
    
    Description:
        A suite of tools for use in Maya.
    
    Instructions:
        >>> import boTools
        >>> boTools.GUI()
    
    Version 0.1:
        >
    
    Feel free to email me with any bugs, comments, or requests!
"""

__version__ = '0.1.1'
__author__ = 'Bohdon Sayre'


import gui

def GUI():
    """Wrap gui.GUI as GUI for convenience"""
    gui.GUI()