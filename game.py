#!/usr/bin/env python
"""
Library:
    
"""
    
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import pylib.xmlparse as xp

import board
import display
import player

DEBUG_DISPLAY_PAUSE = True

POINTS_NEEDED_TO_WIN = 100
LIMIT_NUM_BLOCKS = 10

PENALTY_TOO_MANY_BLOCKS = 1
PENALTY_EARLY_BLOCK_HOLD_DIV = 3.1
PENALTY_FINAL_BLOCK_HOLD_DIV = 1.9

BONUS_EARLY_EMPTY_HAND_NO_SCORE = 11
BONUS_EARLY_EMPTY_HAND = 3.5
BONUS_FINAL_EMPTY_HAND = 2.5


__VERSION__ = "1.1"

DEBUG_DISPLAY_PAUSE = False


#-------------------------------------------------------------------------------
class Stats(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        self.numRounds = 0
        
                
#-------------------------------------------------------------------------------
class Game(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, display, p1=None, p2=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        self.score1 = self.score2 = 0
        self.rnd = 0
        self.blockLimit = LIMIT_NUM_BLOCKS
        
        self.state = self.sstate = 0
        self.display = display

        if p1 is not None:
            assert p2 is not None
            self.player1 = p1
            self.player2 = p2
            
            self.allHuman = p1.isHuman() and p2.isHuman()
            self.allComputer = not p1.isHuman() and not p2.isHuman()
            p1.setGame(self)
            p2.setGame(self)
            
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def play(self, brd=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ proceed to play rounds until 1 or both players exceed needed points 
        """
        while 1:
            try:
                self.PlayRound(brd)
            except player.Notification as ex:
                if ex.typ == 'quit':
                    return

            brd = None

            if self.player1.gameScore >= POINTS_NEEDED_TO_WIN and self.player2.gameScore >= POINTS_NEEDED_TO_WIN:
                if self.player1.gameScore == self.player2.gameScore:
                    continue

                if self.player1.gameScore > self.player2.gameScore:
                    self.display.printInfo("Player1 Winner: %4.2f %4.2f" % (self.player1.gameScore, self.player2.gameScore))
                else:
                    self.display.printInfo("Player2 Winner: %4.2f %4.2f" % (self.player2.gameScore, self.player1.gameScore))
                return

            if self.player1.gameScore >= POINTS_NEEDED_TO_WIN:
                self.display.printInfo("Player1 Winner: %4.2f %4.2f" % (self.player1.gameScore, self.player2.gameScore))
                return

            if self.player2.gameScore >= POINTS_NEEDED_TO_WIN:
                self.display.printInfo("Player2 Winner: %4.2f %4.2f" % (self.player2.gameScore, self.player1.gameScore))
                return
                
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def PlayRound(self, brd=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ a round consists of each player playing a subround where they get
            "Last Move" 
        """
        if brd is None:
            self.rnd += 1
            self.state = 0

        if self.state != 2:
            self.state = 1
            self.display.printInfo("\n>>> Round:", self.rnd)
            self.PlaySubRound(self.player1, self.player2, brd)
            brd = None

        ## if both are greater, finish round
        if not (self.player1.gameScore >= POINTS_NEEDED_TO_WIN and self.player2.gameScore >= POINTS_NEEDED_TO_WIN):
            ## else round ends early if someone over
            if self.player1.gameScore >= POINTS_NEEDED_TO_WIN or self.player2.gameScore >= POINTS_NEEDED_TO_WIN:
                return    
            
        self.state = 2
        self.sstate = 0
        self.display.printInfo("\n>>> 2cd SubRound\n")
        self.PlaySubRound(self.player2, self.player1, brd)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def PlaySubRound(self, frst, secd, brd=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ A subround consists of players playing until all blocks are played
            or one player manages to empty their hand 
        """
            
        ## brd not None implies that we are starting in a restored (prior saved) game
        if brd:
            b = self.brd = brd
            
            ## in a saved game, first player may have already played in the subround, so should be skipped
            skip = brd.skip
        else:
            b = self.brd = board.Board(frst, secd, self.display)
            b.startHand()
            skip = False

        playerEmptiedHand = False
        
        while b.blksLeft() > 0:
            
            ## skip only true if in a restored game, first player has already played in this subround
            if not skip:
                ## player one moves
                if frst.turn(b):
                    ## if returns out of blocks, opponent doesn't get to move
                    playerEmptiedHand = True
                    break
            else:
                skip = False

            assert b.validation()

            if self.allHuman:
                self.display.HideAll()
            elif self.allComputer:
                self.display.display(frst, True)

            ## indicates that it is player 2's move next in the event of a saved game at this point
            self.sstate = 1
            
            ## determine if it is the "last move"
            lastMove = b.blksLeft() == 0
            if lastMove:
                self.display.lastMove()

            ## player 2 moves
            if secd.turn(b, lastMove, scd=lastMove):
                ## if returns out of blocks, opponent doesn't get to move
                playerEmptiedHand = True
                break
                
            ## indicates that it is player 1's move next in the event of a saved game at this point
            self.sstate = 0
            assert b.validation()

            if self.allHuman:
                self.display.HideAll()
            elif self.allComputer:
                if DEBUG_DISPLAY_PAUSE:
                    self.display.CompPause(secd)
                else:
                    self.display.display(secd, True)

                
        ## indicates that it is player 1's last move in the event of a saved game at this point
        self.sstate = 3
        
        ## if players still have blocks their hands, first player gets last turn
        if not playerEmptiedHand:
            frst.turn(b, lastMove)

        assert b.validation()
        self.display.display(None, True)

        self.sstate = 4
        p1s = self.player1.getScore()
        p2s = self.player2.getScore()
        if p1s <= 0 and p2s <= 0:
            extra = 20
            self.player1.updateScore(b, extra)
            self.player2.updateScore(b, extra)
        elif p1s <= 0:
            extra = self.player1.updateScore(b)
            self.player2.updateScore(b, extra)
        else:
            extra = self.player2.updateScore(b)
            self.player1.updateScore(b, extra)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def calcScoreAdjustments(self, pd, brd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ calculate score adjustments based on state of board and players hand
        """
        ddiv = PENALTY_EARLY_BLOCK_HOLD_DIV

        ## see if player's hand is empty
        nblks = pd.numBlks()

        if nblks == 0:
            
            ## did the round finish early
            if brd.blksLeft() > 0:
                ## special bonus for going out early with reward for
                ## scoring no points while doing it
                emptyHandBonus = BONUS_EARLY_EMPTY_HAND_NO_SCORE if pd.numScores() == 0 else BONUS_EARLY_EMPTY_HAND
            else:
                ## still value in emptying your hand even if last move
                emptyHandBonus = BONUS_FINAL_EMPTY_HAND

            ## penalty is more severe if holding blocks at the end
            ddiv = PENALTY_FINAL_BLOCK_HOLD_DIV
        else:
            emptyHandBonus = 0

        ## calculate penalty
        penalty = max(nblks, pd.handValue()/ddiv)

        ## get total score
        return emptyHandBonus - penalty

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def checkForTurnPenalties(self, pd):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ there is a penalty for exceeding a maximum amount of blocks in hand 
        """
        return PENALTY_TOO_MANY_BLOCKS if pd.numBlks() >= self.blockLimit else 0
            
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def save(self, fn=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ save the game to a file 
        """
        if fn is None:
            fn = self.display.getFileName("Save Game To:", exists=False)
            if not fn: 
                return

        with open(fn , 'w') as otf:
            xn = xp.xmlNode('<blocks ver="%s" round="%d" state="%d" sstate="%d"/>' % (__VERSION__, self.rnd, self.state, self.sstate))
    
            p1 = xn.add('<player1 type="%s"/>' % (self.player1.typ))
            self.player1.save(p1)
    
            p2 = xn.add('<player2 type="%s"/>' % (self.player2.typ))
            self.player2.save(p2)
    
            self.brd.save(xn)
            xn.writeFile(otf)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restore(self, fn=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ restore the game from the file
        """
        if fn is None:
            fn = self.display.getFileName("Restore Game From:", exists=True)
            if not fn: 
                return

        with open(fn , 'rU') as inf:        
            xn = xp.xmlNode(inf.read())

        if not(xn['ver'] == __VERSION__):
            print('unable to restore file "%s"' % fn, file=oss.stderr)
            return

        self.rnd = int(xn['round'])

        p1 = xn.findChild('player1')
        self.player1 = player.PlayerFactory(self, p1['type'])

        p2 = xn.findChild('player2')
        self.player2 = player.PlayerFactory(self, p2['type'])

        b = xn.findChild('board')
        brd = board.Board(self.player1, self.player2, self.display)

        ## restore game state     
        brd.skip = xn['sstate'] == '1'
        self.state = int(xn['state'])

        brd.restore(b)
        self.player1.restore(p1)
        self.player2.restore(p2)
        self.play(brd)

        