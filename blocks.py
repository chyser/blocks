"""
usage: blocks

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


import pylib.osscripts as oss
import pylib.xmlparse as xp
import random
import time

import board
import display
import player

__VERSION__ = "1.1"

DEBUG_DISPLAY_PAUSE = True

POINTS_NEEDED_TO_WIN = 100

PENALTY_TOO_MANY_BLOCKS = 1
PENALTY_EARLY_BLOCK_HOLD_DIV = 3.1
PENALTY_FINAL_BLOCK_HOLD_DIV = 1.9

BONUS_EARLY_EMPTY_HAND_NO_SCORE = 11
BONUS_EARLY_EMPTY_HAND = 3.5
BONUS_FINAL_EMPTY_HAND = 2.5

#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ options:
            -s | --seed   : specify a seed for the random number generator
            
    """
    args, opts = oss.gopt(argv[1:], [('t', 'test')], [('s', 'seed'), ('r', 'restore')], __doc__ + main.__doc__)

    if opts.seed:
        sd = int(opts.seed)
    else:
        ## used for debugging
        sd = int(time.time())

    print(sd, "\n\n")
    random.seed(sd)
    
    global DEBUG_DISPLAY_PAUSE
    DEBUG_DISPLAY_PAUSE = not opts.test

    cmd = '3' if opts.test else None
    
    while 1:
        try:
            if opts.restore:
                Game().restore(opts.restore)
                opts.restore = None
            else:
                menu(cmd)
                break

        except player.Notification as n:
            if n.typ == 'quit':
                pass
            elif n.typ == 'restore':
                opts.restore = n.val


    oss.exit(0)



#-------------------------------------------------------------------------------
class Game(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, p1=None, p2=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        self.score1 = self.score2 = 0
        self.rnd = 0
        self.blockLimit = 10
        self.state = self.sstate = 0

        self.display = display.DisplayFactory('console')

        if p1:
            self.player1 = player.PlayerFactory(self, 'human')
            self.player1.init(p1)
        else:
            self.player1 = player.PlayerFactory(self, 'computer')
            self.player1.init('bytes')

        if p2:
            self.player2 = player.PlayerFactory(self, 'human')
            self.player2.init(p2)
            self.allHuman = p1 is not None
            self.allComp = None
        else:
            self.allComp = p1 is None
            self.allHuman = None
            self.player2 = player.PlayerFactory(self, 'computer')
            self.player2.init('bits')

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

            assert b.validation(frst.pd, secd.pd)

            if self.allHuman:
                self.display.HideAll()
            elif self.allComp:
                self.display.display(frst, True)

            ## indicates that it is player 2's move next in the event of a saved game at this point
            self.sstate = 1
            
            ## determine if it is the "last move"
            lastMove = b.blksLeft() == 0
            if lastMove:
                self.display.printInfo("\n>>> LAST MOVE\n")

            ## player 2 moves
            if secd.turn(b, lastMove, scd=lastMove):
                ## if returns out of blocks, opponent doesn't get to move
                playerEmptiedHand = True
                break
                
            ## indicates that it is player 1's move next in the event of a saved game at this point
            self.sstate = 0
            assert b.validation(frst.pd, secd.pd)

            if self.allHuman:
                self.display.HideAll()
            elif self.allComp:
                if DEBUG_DISPLAY_PAUSE:
                    self.display.CompPause(secd)
                else:
                    self.display.display(secd, True)

                
        ## indicates that it is player 1's last move in the event of a saved game at this point
        self.sstate = 3
        
        ## if players still have blocks their hands, first player gets last turn
        if not playerEmptiedHand:
            frst.turn(b, lastMove)

        assert b.validation(frst.pd, secd.pd)
        self.display.display(None, True)

        self.sstate = 4
        self.player1.updateScore(b)
        self.player2.updateScore(b)

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


#-------------------------------------------------------------------------------
def menu(c=None):
#-------------------------------------------------------------------------------
    while 1:
        if c is None:
            print("Menu")
            print("     1) New Game: Human -vs- Machine")
            print("     2) New Game: Human -vs- Human")
            print("     3) New Game: Machine -vs- Machine")
            print("     4) Restore Game")
            print("     5) Quit")
            print("")
            c = raw_input('> ')
        else:
            print('testing:', c)
            
        if c == '1':
            if random.random() <= 0.5:
                name = display.DisplayFactory('console').getPlayerName('Player 1:')
                Game(p1=name).play()
            else:
                name = display.DisplayFactory('console').getPlayerName('Player 2:')
                Game(p2=name).play()

        elif c == '2':
            p1 = display.DisplayFactory('console').getPlayerName('Player 1:')
            p2 = display.DisplayFactory('console').getPlayerName('Player 2:')
            Game(p1, p2).play()

        elif c == '3':
            Game().play()

        elif c == '4':
            Game().restore()

        elif c == '5':
            return


if __name__ == "__main__":
    main(oss.argv)

