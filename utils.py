

from pymel.core import *

def filterSelection(filters):
    """Return a list of the selected items that contain the given filter strings"""
    result = []
    for node in selected():
        for filter in filters:    
            if filter in node.nodeName():
                result.append(node)
    return result


def filterSelectionPrompt():
    result = promptDialog(t='Filter Selection', m='filter:', b=['Ok', 'Cancel'], cb='Cancel')
    if result == 'Ok':
        select(filterSelection([promptDialog(q=True)]))


