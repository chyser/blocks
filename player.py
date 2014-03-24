"""
    cmds:
        'r'         - rearrange the blocks
        '.'         - end turn, but check for > 10
        'n'         - end turn, take penalty for > 10
        'qq'| exit  - leave game

        - movements
        [0-9][a-e]  - move block <num1> to end of row <letter2>
        [a-e][a-e]  - move end block of row <letter1> to end of row <letter2>
        [a-e][0-..][a-e] - move list specified by [a-e][0-] to end of row <letter3>

        - score
        '0'|'s'     - score the zero blocks in hand
        [0-9]s      - score block <num> from hand
        [a-e]s      - score end block from row

        - head replacements
        [0-9][a-e][a-e]  - move block <num> to head of row <letter2> and moving
                           that row to end of specified row <letter3>
        [a-e][a-e][a-e]  - move end block of row <letter1> to head of row <letter2>
                           moving that row to end of row <letter3>
        [0-9][a-e]s      - move block <num> to head of row <letter2> and scoring
                           that block
        [a-e][a-e]s      - move end block of row <letter1> to head of row <letter2>
                           and scoring that block
        [a-e][0-..][a-e][a-e] - move list specified by [a-e][0-] to head of row
                                <letter3>, moving that row to end of row <letter4>
        [a-e][0-..][a-e]s     - move list specified by [a-e][0-] to head of row
                                <letter3>, scoring that block

        *Note, the block moving to the head must be a 'z' block

"""


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import


#import pylib.relib as reb
###import pylib.xmlparse as xp
import random

import board


#-------------------------------------------------------------------------------
class Notification(Exception):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, typ, val=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Exception.__init__(self, "Notification")
        self.typ = typ
        self.val = val


#-------------------------------------------------------------------------------
class Player(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, name, typ):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        self.name = name
        self.gameScore = 0
        self.pd = None
        self.game = None
        self.disp = None
        self.typ = typ
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def setGame(self, game):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.game = game
        self.disp = game.display

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def isHuman(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return self.typ == 'human'

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def setName(self, name):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.name = name

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def updateScore(self, brd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        res = self.game.calcScoreAdjustments(self.pd, brd) + self.pd.rndScore
        self.info(self.name, "Results = %5.2f" % res)
        self.gameScore += res

        ## total score can't be negative
        if self.gameScore < 0:
            self.gameScore = 0

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def save(self, xn):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
       p = xn.add('<player name="%s"/>' % self.name)
       self.pd.save(p)
       self.saveState(p)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def saveState(self, p):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restore(self, p):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pn = p.findChild('player')
        self.pd.restore(pn)
        self.name = pn['name']
        self.restoreState(pn)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restoreState(self, p):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def turn(self, b, lastMove=False, scd=False):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ handle moves necessary and return True if out of blocks, else false
        """
        self.game.save("stat.blk")

        ## call player move
        self.move(b, lastMove, scd)

        ## can't end turn holding 0 blocks
        b.score0(self.pd)

        ## apply any per turn penalties (say too many blocks)
        self.pd.rndScore -= self.game.checkForTurnPenalties(self.pd)

        if self.pd.numBlks() == 0:
            return True

        blk = b.dd.get()
        if blk:
            self.pd.setBlk(blk)
        return False

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def move(self, b):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def info(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.disp.printInfo(*args)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getBlks(self, typ='play', order='low') :
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return self.pd.getBlks(typ, order)


#-------------------------------------------------------------------------------
def PlayerFactory(playerType, name):
#-------------------------------------------------------------------------------
    try:
        mod = __import__(playerType + "_player")
    except ImportError:
        return

    return mod.ObjectFactory(name)
