

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
        pd = brd.getPD(self)
        res = self.game.calcScoreAdjustments(pd, brd) + pd.rndScore
        self.info(self.name, "Results = %5.2f" % res)
        self.gameScore += res

        ## total score can't be negative
        if self.gameScore < 0:
            self.gameScore = 0

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def save(self, xn):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
       p = xn.add('<player name="%s"/>' % self.name)
       self.saveState(p)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def saveState(self, p):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restore(self, p):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pn = p.findChild('player')
        self.name = pn['name']
        self.restoreState(pn)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restoreState(self, p):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getPD(self, brd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return brd.getPD(self)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def turn(self, brd, lastMove=False, scd=False):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ handle moves necessary and return True if out of blocks, else false
        """
        self.game.save("stat.blk")

        ## call player move
        self.move(brd, lastMove, scd)

        pd = brd.getPD(self)

        ## can't end turn holding 0 blocks
        brd.score0(pd)

        ## apply any per turn penalties (say too many blocks)
        pd.rndScore -= self.game.checkForTurnPenalties(pd)

        if pd.numBlks() == 0:
            return True

        blk = brd.dd.get()
        if blk:
            pd.setBlk(blk)
        return False

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def move(self, brd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        raise NotImplementedError

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def info(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.disp.printInfo(*args)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getBlks(self, brd, typ='play', order='low') :
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(brd, board.Board)
        return self.getPD(brd).getBlks(typ, order)


#-------------------------------------------------------------------------------
def PlayerFactory(playerType, name):
#-------------------------------------------------------------------------------
    try:
        mod = __import__(playerType + "_player")
    except ImportError:
        return

    return mod.ObjectFactory(name)
