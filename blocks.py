from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import pylib.osscripts as oss
import random
import time

import display
import player
import game


#-------------------------------------------------------------------------------
def main(argv):
#-------------------------------------------------------------------------------
    """ options:
            -s | --seed   : specify a seed for the random number generator
            
    """
    args, opts = oss.gopt(argv[1:], [], [('s', 'seed'), ('r', 'restore')], __doc__)

    if opts.seed:
        sd = int(opts.seed)
    else:
        ## used for debugging
        sd = int(time.time())

    print(sd, "\n\n")
    random.seed(sd)
    
    disp = display.DisplayFactory('console')

    while 1:
        try:
            if opts.restore:
                Game().restore(opts.restore)
                opts.restore = None
            else:
                menu(disp)
                break

        except player.Notification as n:
            if n.typ == 'quit':
                pass
            elif n.typ == 'restore':
                opts.restore = n.val

    oss.exit(0)


#-------------------------------------------------------------------------------
def menu(disp):
#-------------------------------------------------------------------------------
    while 1:
        print("Menu")
        print("     1) New Game: Human -vs- Machine")
        print("     2) New Game: Human -vs- Human")
        print("     3) Restore Game")
        print("     4) Quit")
        print("")
        c = raw_input('> ')

        if c == '1':
            p1 = player.PlayerFactory(self, 'human', disp.getPlayerName('Human Player:'))
            p2 = player.PlayerFactory(self, 'computer', "Bytes")
            
            if random.random() <= 0.5:
                game.Game(disp, p1, p2).play()
            else:
                game.Game(disp, p2, p1).play()
            
        elif c == '2':
            p1 = player.PlayerFactory(self, 'human', disp.getPlayerName('Human Player 1:'))
            p2 = player.PlayerFactory(self, 'human', disp.getPlayerName('Human Player 2:'))
            game.Game(disp, p1, p2).play()

        elif c == '3':
            game.Game(disp).restore()

        elif c == '4':
            return
            

if __name__ == "__main__":
    main(oss.argv)

