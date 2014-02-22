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


import pylib.relib as reb
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
    def __init__(self, game, name=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        super(Player, self).__init__()
        self.name = name
        self.score = 0
        self.pd = None
        self.game = game
        self.disp = game.display

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def init(self, name):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.name = name

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def updateScore(self, brd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        res = self.game.calcScore(self.pd, brd)
        self.disp.printInfo(self.name, "Results = %5.2f" % res)
        self.score += res

        ## total score can't be negative
        if self.score < 0:
            self.score = 0

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

        b.score0(self.pd)

        ## apply any per turn penalties (say too many blocks)
        self.game.checkForTurnPenalties(self.pd)

        if len(self.pd.blks) == 0:
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
class HumanPlayer(Player):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def move(self, b, lastMove, scd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        while 1:
            b.display(self, b.blksLeft() == 0)

            cmdstr = self.disp.getInput(self)

            for cmd in cmdstr.split(';'):
                if not cmd:
                    continue

                if cmd == "help":
                    self.info(__doc__)
                    continue

                if cmd == "save":
                    self.game.save()
                    continue

                if cmd == "exit" or cmd == 'qq':
                    raise Notification('quit')

                if cmd == '.':
                    if len(self.pd.blks) >= 10:
                        self.info("cannot keep more than 10 blks");
                        self.info("use 'n' to accept penalty");
                        continue
                    return

                ## an re bug
                if cmd[0] == '.':
                    self.info("## - unknown cmd:", cmd)
                    continue

                if cmd == 'n':
                    if len(self.pd.blks) >= 10:
                        self.info("cannot keep more than 10 blks");
                        self.info("exiting anyway w/ penalty");
                    return

                elif cmd == '0' or cmd == 's':
                    b.score0(self.pd)

                elif cmd == 'r':
                    self.pd.rearrange()

                elif reb.eq(cmd, "[@*-=][0-9xyz][a-es]"):
                    blk = board.Block(cmd[:2])
                    if self.pd.hasBlk(blk):
                        b.move(self.pd, blk, cmd[2])
                    else:
                        self.info('## - no such block' + cmd[:2])

                elif reb.eq(cmd, "[0-9xyz][a-es]") or reb.eq(cmd, "[@*-=][a-es]"):
                    blk = self.pd.findBlk(cmd[0])
                    if blk:
                        b.move(self.pd, blk, cmd[1])
                    else:
                        self.info("## ambiguous blk description")

                elif reb.eq(cmd, "[@*-=][z][a-e][a-es]"):
                    blk = board.Block(cmd[:2])
                    if self.pd.hasBlk(blk):
                        b.replace(self.pd, blk, cmd[2], cmd[3])
                    else:
                        self.info('## - no such block' + cmd[:2])

                elif reb.eq(cmd, "[z][a-e][a-es]"):
                    blk = self.pd.findBlk(cmd[0])
                    if blk:
                        b.replace(self.pd, blk, cmd[1], cmd[2])
                    else:
                        self.info("## ambiguous blk description")

                elif reb.eq(cmd, "[a-e][a-es]"):
                    b.moveEnd(self.pd, cmd[0], cmd[1])

                elif reb.eq(cmd, "[a-e][0-9f-v][a-e]"):
                    b.moveList(self.pd, cmd[0], cmd[1], cmd[2])

                elif reb.eq(cmd, "[a-e][a-e][a-es]"):
                    b.moveEnd3(self.pd, cmd[0], cmd[1], cmd[2])

                elif reb.eq(cmd, "[a-e][0-9f-v][a-e][a-es]"):
                    b.moveList4(self.pd, cmd[0], cmd[1], cmd[2], cmd[3])

                else:
                    self.info("## - unknown cmd:", cmd)


#-------------------------------------------------------------------------------
class TestPlayer(Player):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, game):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Player.__init__(self, game)


import computer_player

#-------------------------------------------------------------------------------
def PlayerFactory(game, player):
#-------------------------------------------------------------------------------
    if player == "human":
        p = HumanPlayer(game)
    elif player == "computer":
        p = computer_player.ComputerPlayer(game)
    elif player == "test":
        p = TestPlayer(game)
    else:
        return

    p.typ = player
    return p

