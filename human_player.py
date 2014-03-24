#!/usr/bin/env python
"""
Library:
    
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
def ObjectFactory(name):
#-------------------------------------------------------------------------------
    return HumanPlayer(name, 'human')