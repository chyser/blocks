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
            -s | --seed <seed>  : specify a seed for the random number generator
            -t | --test <num>   : specify number of test runs
            -n | --nolog        : do not create log files
            
    """
    args, opts = oss.gopt(argv[1:], [('n', 'nolog')], [('t', 'test'), ('s', 'seed')], __doc__)

    if opts.seed:
        sd = int(opts.seed)
    else:
        ## used for debugging
        sd = int(time.time())

    print(sd, "\n\n")
    random.seed(sd)

    disp = display.DisplayFactory('log')
    
    cnt = int(opts.test) if opts.test else None

    idx = 0
    while 1:
        idx += 1
        p1 = player.PlayerFactory('computer', "Bytes")
        p2 = player.PlayerFactory('computer', "Bits")

        if opts.nolog:
            p1.noLog()
            p2.noLog()
            
        game.Game(disp, p1, p2).play()
        
        if cnt and idx > cnt:
            break

    oss.exit(0)


if __name__ == "__main__":
    main(oss.argv)

