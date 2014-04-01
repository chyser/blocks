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
class ComputerPlayer(player.Player):
#-------------------------------------------------------------------------------
    plyrNum = 0
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, name, typ):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        player.Player.__init__(self, name, typ)
        ComputerPlayer.plyrNum += 1
        
        self.numMoves = [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.otf = open('comp_log%d.txt' % ComputerPlayer.plyrNum, 'w')
        self.log("Computer Player: %d\n" % ComputerPlayer.plyrNum)
        self.log(time.ctime())

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def log(self, *arg):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.otf.write(' '.join([str(a) for a in arg]) +'\n')
        self.otf.flush()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getNumMoves(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return random.choice(self.numMoves)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def move(self, brd, lastMove, second):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pd = brd.getPD(self)
        
        defense = second
        if lastMove and not second:
            self.info("... have last move")

        pd.moves = moves = []
        if lastMove or pd.numBlks() >= self.game.blockLimit:
            cnt = 2000
        else:
            cnt = random.randint(13, 311)


        ## main loop looking for moves
        for iii in range(cnt):

            ## score covered blocks
            for iiii in range(1000):
                found = False
                for blk in self.getBlks(brd, 'saves'):
                    if brd.willScore(blk):
                        if pd.findBlk(blk.next()):
                            brd.move(pd, blk, 's', silent=1)
                            moves.append('%s scored' % blk)
                            found = True

                if not found: break


            ## attempt to score blocks on the board
            for iiii in range(1000):
                bfound = False

                ## score all that can
                for ii in range(1000):
                    found = False

                    typ = 'all' if lastMove and not defense else 'play'
                    for blk in self.getBlks(brd, typ):
                        if brd.willScore(blk):
                            print('scoring play block', blk)
                            brd.move(pd, blk, 's', silent=1)
                            moves.append('%s scored' % blk)
                            bfound = found = True

                    if not found: break

                ## check board for scores
                for ii in range(1000):
                    found = False

                    for rc, row in brd.getRows():
                        if len(row) >= 2:
                            blk = row[-1]
                            if brd.willScore(blk):
                                brd.moveEnd(pd, rc, 's', silent=1)
                                moves.append('end of row %s scored' % str(rc))
                                bfound = found = True
                        else:
                            ## do I have a top block
                            zblks = pd.findBlks('z')

                            if not zblks:
                                ## is there a usable one on the board
                                for rc, row in brd.getRows():
                                    if len(row) >= 2:
                                        if row[-1].isa('z'):
                                            zblks = [row[-1]]
                                            break

                            ## if so, score
                            if zblks:
                                zblk = zblks[0]
                                blk = row[-1]
                                if brd.willScore(blk):
                                    brd.replace(pd, zblk, rc, 's', silent=1)
                                    moves.append('end of row %s scored' % str(rc))
                                    bfound = found = True

                    if not found: break
                if not bfound: break

            ## do I have any top blocks
            for zblk in pd.findBlks('z'):
                for rcb, bblk in brd.getBegBlks():
                    found = False
                    for rce, eblk in brd.getEndBlks():
                        if rce != rcb and bblk.compat(eblk):
                            brd.replace(pd, zblk, rcb, rce, silent=1)
                            moves.append('%s moved to %s, %s moved to %s' % (rcb, rce, zblk, rcb))
                            found = True
                            break
                    if found: break

                else:
                    last = {}
                    for i in range(100):
                        found = False
                        for rc0, blk0 in brd.getEndBlks('usable'):
                            for rc1, blk1 in brd.getEndBlks():
                                if rc0 != rc1 and blk0.compat(blk1) and last.get(blk0, None) != rc1:
                                    brd.moveEnd(pd, rc0, rc1, silent=1)
                                    moves.append('end of %s moved to %s' % (rc0, rc1))
                                    last[blk0] = rc0
                                    found = True
                                    break
                            if found: break
                        if found: break

            ## look for scoring blocks anywhere on field
            self.log('looking for scoring blocks embedded in rows')

            for blk in pd.getNextScores():
                for row in 'abcde':
                    bidx = brd.getIdxInRow(blk, row, 1)
                    if bidx is None:
                        continue

                    for r1 in 'abcde':
                        if r1 == row or not brd.moveList(pd, row, bidx, r1, silent=1):
                            continue
                        if brd.moveEnd(pd, row, 's', silent=1):
                            break

            ## make simple moves
            if lastMove:
                iidx = 10000
            else:
                iidx = 0
                n = pd.numBlks()
                if n > 9:
                    iidx = n - 9
                iidx += self.getNumMoves()

            self.log('make "%d" simple moves' % iidx)
            for i in xrange(iidx):
                found = False
                for rc, row in brd.getRows():
                    typ = 'all' if lastMove and not defense else 'play'
                    for blk in self.getBlks(brd, typ, 'high'):
                        if not lastMove and pd.numBlks() < 8 and blk.value() < 5:
                            continue

                        if blk.compat(row[-1]):
                            brd.move(pd, blk, rc, silent=1)
                            moves.append('%s moved to %s' % (blk, rc))
                            found = True
                if not found: break

            for i in range(random.randint(7, 311)):
                _, brow, bidx = brd.getRandBlk()
                _, erow, _ = brd.getRandBlk()
                if (brd.moveList(pd, brow, bidx, erow, silent=1)):
                    moves.append('%s/%d moved to %s' % (brow, bidx, erow))

                    
#-------------------------------------------------------------------------------
def ObjectFactory(name):
#-------------------------------------------------------------------------------
    return ComputerPlayer(name, 'computer')
    
