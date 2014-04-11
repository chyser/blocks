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
    """ aitest.py [options]
        options:
            -s | --seed <seed>  : specify a seed for the random number generator
            -t | --test <num>   : specify number of test runs
            -n | --nolog        : do not create log files
            -N | --nomove       : play against no move player
            
    """
    args, opts = oss.gopt(argv[1:], [('n', 'nolog'), ('N', 'nomove')], [('t', 'test'), ('s', 'seed')], main.__doc__)

    if opts.seed:
        sd = int(opts.seed)
    else:
        ## used for debugging
        sd = int(time.time())

    print(sd, "\n\n")
    random.seed(sd)

    disp = display.DisplayFactory('log')
    
    cnt = int(opts.test) if opts.test else None

    fn = "%s.data" % oss.DateFileName()
    otf = open(fn, 'w')
    print('Opening data file: %s' % fn)
    
    idx = 0
    while 1:
        idx += 1
        if not opts.nomove:
            p1 = player.PlayerFactory('computer', "Bytes")
            name = 'Bytes'
        else:
            name = 'nom'
            p1 = player.PlayerFactory('nomove', "nom")
            
        p2 = player.PlayerFactory('computer', "Bits")

        if opts.nolog:
            p1.noLog()
            p2.noLog()
            
        s = game.Game(disp, p1, p2).play()
        otf.write('name: %s' % name)
        otf.write('\t' + str(s) + '\n')
        otf.flush()
        
        if cnt and idx > cnt:
            break

    oss.exit(0)


if __name__ == "__main__":
    main(oss.argv)

