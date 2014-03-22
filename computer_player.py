#!/usr/bin/env python
"""
Library:

"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import random
import player

#-------------------------------------------------------------------------------
class ComputerPlayer(player.Player):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, game):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        player.Player.__init__(self, game)
        self.numMoves = [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.otf = open('comp_log.txt', 'w')

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
    def move(self, b, lastMove, second):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        defense = second
        if lastMove and not second:
            self.info("... have last move")

        self.pd.moves = moves = []
        if lastMove or self.pd.numBlks() >= self.game.blockLimit:
            cnt = 2000
        else:
            cnt = random.randint(13, 311)


        ## main loop looking for moves
        for iii in range(cnt):

            ## score covered blocks
            for iiii in range(1000):
                found = False
                for blk in self.getBlks('saves'):
                    if b.willScore(blk):
                        if self.pd.findBlk(blk.next()):
                            b.move(self.pd, blk, 's', silent=1)
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
                    for blk in self.getBlks(typ):
                        if b.willScore(blk):
                            print('scoring play block', blk)
                            b.move(self.pd, blk, 's', silent=1)
                            moves.append('%s scored' % blk)
                            bfound = found = True

                    if not found: break

                ## check board for scores
                for ii in range(1000):
                    found = False

                    for rc, row in b.getRows():
                        if len(row) >= 2:
                            blk = row[-1]
                            if b.willScore(blk):
                                b.moveEnd(self.pd, rc, 's', silent=1)
                                moves.append('end of row %s scored' % str(rc))
                                bfound = found = True
                        else:
                            ## do I have a top block
                            zblks = self.pd.findBlks('z')

                            if not zblks:
                                ## is there a usable one on the board
                                for rc, row in b.getRows():
                                    if len(row) >= 2:
                                        if row[-1].isa('z'):
                                            zblks = [row[-1]]
                                            break

                            ## if so, score
                            if zblks:
                                zblk = zblks[0]
                                blk = row[-1]
                                if b.willScore(blk):
                                    b.replace(self.pd, zblk, rc, 's', silent=1)
                                    moves.append('end of row %s scored' % str(rc))
                                    bfound = found = True

                    if not found: break
                if not bfound: break

            ## do I have any top blocks
            for zblk in self.pd.findBlks('z'):
                for rcb, bblk in b.getBegBlks():
                    found = False
                    for rce, eblk in b.getEndBlks():
                        if rce != rcb and bblk.compat(eblk):
                            b.replace(self.pd, zblk, rcb, rce, silent=1)
                            moves.append('%s moved to %s, %s moved to %s' % (rcb, rce, zblk, rcb))
                            found = True
                            break
                    if found: break

                else:
                    last = {}
                    for i in range(100):
                        found = False
                        for rc0, blk0 in b.getEndBlks('usable'):
                            for rc1, blk1 in b.getEndBlks():
                                if rc0 != rc1 and blk0.compat(blk1) and last.get(blk0, None) != rc1:
                                    b.moveEnd(self.pd, rc0, rc1, silent=1)
                                    moves.append('end of %s moved to %s' % (rc0, rc1))
                                    last[blk0] = rc0
                                    found = True
                                    break
                            if found: break
                        if found: break

            ## look for scoring blocks anywhere on field
            self.log('looking for scoring blocks embedded in rows')

            for blk in self.pd.getNextScores():
                for row in 'abcde':
                    bidx = b.getIdxInRow(blk, row, 1)
                    if bidx is None:
                        continue

                    for r1 in 'abcde':
                        if r1 == row or not b.moveList(self.pd, row, bidx, r1, silent=1):
                            continue
                        if b.moveEnd(self.pd, row, 's', silent=1):
                            break

            ## make simple moves
            if lastMove:
                iidx = 10000
            else:
                iidx = 0
                n = self.pd.numBlks()
                if n > 9:
                    iidx = n - 9
                iidx += self.getNumMoves()

            self.log('make "%d" simple moves' % iidx)
            for i in xrange(iidx):
                found = False
                for rc, row in b.getRows():
                    typ = 'all' if lastMove and not defense else 'play'
                    for blk in self.getBlks(typ, 'high'):
                        if not lastMove and self.pd.numBlks() < 8 and blk.value() < 5:
                            continue

                        if blk.compat(row[-1]):
                            b.move(self.pd, blk, rc, silent=1)
                            moves.append('%s moved to %s' % (blk, rc))
                            found = True
                if not found: break

            for i in range(random.randint(7, 311)):
                _, brow, bidx = b.getRandBlk()
                _, erow, _ = b.getRandBlk()
                if (b.moveList(self.pd, brow, bidx, erow, silent=1)):
                    moves.append('%s/%d moved to %s' % (brow, bidx, erow))


#-------------------------------------------------------------------------------
def __test__():
#-------------------------------------------------------------------------------
    """
    used for automated module testing. see L{tester}
    """
    #import pylib.tester as tester
    return 0


#-------------------------------------------------------------------------------
if __name__ == "__main__":
#-------------------------------------------------------------------------------
    import pylib.osscripts as oss

    args, opts = oss.gopt(oss.argv[1:], [], [], __test__.__doc__)


    res = not __test__()
    oss.exit(res)
