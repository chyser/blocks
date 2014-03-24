"""
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

#-------------------------------------------------------------------------------
class Display(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        self.brd = None
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getInput(self, player):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def display(self, p, all):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def printInfo(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def lastMove(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.printInfo("\n>>> LAST MOVE\n")
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getFileName(self, msg, exists):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def CompPause(self, plyr):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def HideAll(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getPlayerName(self, msg):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def clear(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError()
    
        
#-------------------------------------------------------------------------------
def DisplayFactory(dtype):
#-------------------------------------------------------------------------------
    try:
        mod = __import__(dtype + '_display')
    except ImportError:
        return
    return mod.ObjectFactory()
    
    
