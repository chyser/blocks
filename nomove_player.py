#!/usr/bin/env python
"""
Library:

"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import random
import time

import player

#-------------------------------------------------------------------------------
class NoMovePlayer(player.Player):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def noLog(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pass
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def move(self, brd, lastMove, second):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pass
                    
#-------------------------------------------------------------------------------
def ObjectFactory(name):
#-------------------------------------------------------------------------------
    return NoMovePlayer(name, 'NoMove')
    
