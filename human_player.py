#!/usr/bin/env python
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

import player
import board
import pylib.relib as reb

#-------------------------------------------------------------------------------
class HumanPlayer(player.Player):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def move(self, b, lastMove, scd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        sb = b.copy()

        pd = self.getPD(b)
        
        while 1:
            b.display(self, b.blksLeft() == 0)

            cmdstr = self.disp.getInput(self)

            for cmd in cmdstr.split(';'):
                if not cmd:
                    continue

                if cmd == "redo":
                    b.copy(sb)
                    continue

                if cmd == "help":
                    self.info(__doc__)
                    continue

                if cmd == "save":
                    self.game.save()
                    continue

                if cmd == "exit" or cmd == 'qq':
                    raise player.Notification('quit')

                if cmd == '.':
                    if len(pd.blks) >= 10:
                        self.info("cannot keep more than 10 blks");
                        self.info("use 'n' to accept penalty");
                        continue
                    return

                ## an re bug
                if cmd[0] == '.':
                    self.info("## - unknown cmd:", cmd)
                    continue

                if cmd == 'n':
                    if len(pd.blks) >= 10:
                        self.info("cannot keep more than 10 blks");
                        self.info("exiting anyway w/ penalty");
                    return

                elif cmd == '0' or cmd == 's':
                    b.score0(pd)

                elif cmd == 'r':
                    pd.rearrange()

                elif reb.eq(cmd, "[@*-=][0-9xyz][a-es]"):
                    blk = board.Block(cmd[:2])
                    if pd.hasBlk(blk):
                        b.move(pd, blk, cmd[2])
                    else:
                        self.info('## - no such block' + cmd[:2])

                elif reb.eq(cmd, "[0-9xyz][a-es]") or reb.eq(cmd, "[@*-=][a-es]"):
                    blk = pd.findBlk(cmd[0])
                    if blk:
                        b.move(pd, blk, cmd[1])
                    else:
                        self.info("## ambiguous blk description")

                elif reb.eq(cmd, "[@*-=][z][a-e][a-es]"):
                    blk = board.Block(cmd[:2])
                    if pd.hasBlk(blk):
                        b.replace(pd, blk, cmd[2], cmd[3])
                    else:
                        self.info('## - no such block' + cmd[:2])

                elif reb.eq(cmd, "[z][a-e][a-es]"):
                    blk = pd.findBlk(cmd[0])
                    if blk:
                        b.replace(pd, blk, cmd[1], cmd[2])
                    else:
                        self.info("## ambiguous blk description")

                elif reb.eq(cmd, "[a-e][a-es]"):
                    b.moveEnd(pd, cmd[0], cmd[1])

                elif reb.eq(cmd, "[a-e][0-9f-v][a-e]"):
                    b.moveList(pd, cmd[0], cmd[1], cmd[2])

                elif reb.eq(cmd, "[a-e][a-e][a-es]"):
                    b.moveEnd3(pd, cmd[0], cmd[1], cmd[2])

                elif reb.eq(cmd, "[a-e][0-9f-v][a-e][a-es]"):
                    b.moveList4(pd, cmd[0], cmd[1], cmd[2], cmd[3])

                else:
                    self.info("## - unknown cmd:", cmd)

#-------------------------------------------------------------------------------
def ObjectFactory(name):
#-------------------------------------------------------------------------------
    return HumanPlayer(name, 'human')