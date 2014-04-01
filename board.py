#!/usr/bin/env python
"""
Library:

"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import random

silent = 0

USE_11 = True

if __debug__:
    BLK_COUNT = 44 if USE_11 else 52

def getIdx(v, a=0):
    try:
        return int(v) + a
    except:
        return ord(v) - ord('f') + 10 + a

if USE_11:
    def invIdx(idx):
        return '0123456789xyz'[idx]
else:
    def invIdx(idx):
        return '0123456789z'[idx]


def loadBlks(s):
    s = s.strip()
    return [Block(str(c)) for c in s.split(',')] if s else []


def saveBlks(blks):
    return ','.join([str(s) for s in blks]) + '\n' if blks else ''


def printBlks(c, blks):
    print(c + ': ' + ' '.join([str(s) for s in blks]))


#-------------------------------------------------------------------------------
class Block(object):
#-------------------------------------------------------------------------------
    compt = {
        ' ' : (None, '0'),
        '@' : ('-', '='),
        '*' : ('-', '='),
        '-' : ('@', '*'),
        '=' : ('@', '*'),
        '0' : (None, '1'),
        '1' : ('0', '2'),
        '2' : ('1', '3'),
        '3' : ('2', '4'),
        '4' : ('3', '5'),
        '5' : ('4', '6'),
        '6' : ('5', '7'),
        '7' : ('6', '8'),
        '8' : ('7', '9'),
        '9' : ('8', 'z'),
        'z' : ('9', None),
        }

    values = {
        '0' : 1,
        '1' : 1,
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9,
        'z' : 13,
        }
        
    if not USE_11:
        compt = {
            '9' : ('8', 'x'),
            'x' : ('9', 'y'),
            'y' : ('x', 'z'),
            'z' : ('y', None),
            }
    
        values = {
            'x' : 15,
            'y' : 20,
            'z' : 25
            }

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, blockDesc):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        assert blockDesc[0] == '|' or (blockDesc[0] in self.compt and blockDesc[1] in self.compt)
        self.s = blockDesc
        self._lastrow = None

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __getitem__(self, idx):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return self.s[idx]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __setitem__(self, idx, v):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.s[idx] = v

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def next(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ return the next block in the sequence
        """
        v = self.compt[self.s[1]][1]
        return v if v is None else self.s[0] + v

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def prev(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ return the previous block in the sequence
        """
        v = self.compt[self.s[1]][0]
        return v if v is None else self.s[0] + v

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def value(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ return the game's "value" of the block
        """
        return self.values[self.s[1]]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __cmp__(self, b_s):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ enable comparing a block or the blockDesc value which ever is passed
        """
        if isinstance(b_s, Block):
            return cmp(self.s, b_s.s)
        return cmp(self.s, b_s)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def isa(self, b_s):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ return true id blockDesc is the same, the block's suit is same or
            blocks number is the same
        """
        return self.s == b_s or self.s[0] == b_s or self.s[1] == b_s

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def compat1(self, a, b):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return b in self.compt[a]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def compatBlk(self, blk):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return self.compat1(self.s[0], blk[0]) and self.compat1(self.s[1], blk[1])

    compat = compatBlk

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __str__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return self.s


#-------------------------------------------------------------------------------
class PlayerData(object):
#-------------------------------------------------------------------------------
    """ per player data that is accessible from the board structure
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, pd=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        if pd is not None:
            return self.copy(pd)
            
        self.rndScore = 0
        self.score_tray = {'-' : [], '=' : [], '@' : [], '*' : []}
        self.blks = []
        self.numUnique = 0

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def copy(self, pd=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if pd is None:
            return PlayerData(self)

        self.rndScore = pd.rndScore
        self.score_tray = {
            '-' : pd.score_tray['-'][:], 
            '=' : pd.score_tray['='][:], 
            '@' : pd.score_tray['@'][:], 
            '*' : pd.score_tray['*'][:], 
        }
        self.blks = pd.blks[:]
        self.numUnique = pd.numUnique 

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def save(self, xn):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        p = xn.add('<pd rscore="%f"/>' % (self.rndScore))
        p.add('<blks>%s</blks>' % saveBlks(self.blks))
        
        for c, stray in self.getSTrays():
            p.add('<stray name="%s">%s</stray>' % (c, saveBlks(stray)))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restore(self, p):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pdn = p.findChild('pd')
        self.rndScore = float(pdn['rscore'])

        bn = pdn.findChild('blks')
        self.blks = loadBlks(bn.text)

        for sn in pdn.findChildren('stray'):
            self.score_tray[sn['name']].extend(loadBlks(sn.text))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def numBlks(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return len(self.blks)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def setBlk(self, blk):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(blk, Block)
        self.sort()
        self.blks.append(blk)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def rmBlk(self, blk):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(blk, Block)
        self.blks.remove(blk)
        self.sort()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def findBlk(self, b):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        try:
            return self.findBlks(b)[0]
        except IndexError:
            pass

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def findBlks(self, b):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return [blk for blk in self.blks if blk == b or blk[0] == b or blk[1] == b]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getBlks(self, typ, order='low'):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if typ == 'saves':
            self.sort()
            return list(self.blks[:self.numUnique])

        if typ == 'all':
            l = list(self.blks)
        else:
            self.sort()
            l = list(self.blks[self.numUnique:])

        return sorted(l, lambda a, b: cmp(a[1],b[1]), reverse = order == 'high')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def hasBlk(self, blk):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(blk, Block)
        return blk in self.blks

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getNextScore(self, c):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        try:
            return self.getST(c).next()
        except AttributeError:
            pass

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getNextScores(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return [self.getNextScore(c) for c in '-=@*']

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getST(self, c):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        try:
            return self.score_tray[c][-1]
        except IndexError:
            return Block('  ')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getSTrays(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return [('-', self.score_tray['-']), ('=', self.score_tray['=']),
                ('@', self.score_tray['@']),('*', self.score_tray['*'])]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def sort(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.blks.sort()

        ll = list(self.blks)
        l = []
        self.numUnique = 0

        ss = ''
        for blk in self.blks:
            if blk[0] != ss:
                self.numUnique += 1
                l.append(blk)
                ll.remove(blk)
                ss = blk[0]

        l.extend(ll)
        self.blks = l

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def rearrange(self, lst = None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.sort()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def scoreBlk0(self, blk):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(blk, Block)
        return blk.value() + 1

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def handValue(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return sum([self.scoreBlk0(blk) for blk in self.blks])

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def numScores(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        l = 0
        for v in self.score_tray.values():
            l += len(v)
        return l

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def scoreBlk(self, blk):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(blk, Block)
        self.score_tray[blk[0]].append(blk)
        self.rndScore += self.scoreBlk0(blk)


#-------------------------------------------------------------------------------
class Deck(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, shuffle=True, deck=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)

        if deck is not None:
            return self.copy(deck)
            
        self.d = []
        for s in "@*=-":
            for c in "0123456789z" if USE_11 else "0123456789xyz":
                self.d.append(Block(s + c))

        if __debug__:
            global ALL_BLOCKS
            ALL_BLOCKS = set([str(d) for d in self.d])

        if shuffle:
            self.shuffle()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def copy(self, deck=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if deck is None:
            return Deck(deck=self)
        self.d = deck.d[:]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def shuffle(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for i in range(random.randint(23, 42)):
            random.shuffle(self.d)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def get(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ return the next block or None if empty
        """
        try:
            return self.d.pop(0)
        except IndexError:
            return

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def save(self, xn):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        xn.add('<deck>%s</deck>' % saveBlks(self.d))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restore(self, bn):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        dn = bn.findChild('deck')
        self.d = loadBlks(dn.text)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __len__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return len(self.d)


#-------------------------------------------------------------------------------
class Board(object):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self, player1, player2, disp, startHandSize=7, board=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        object.__init__(self)
        
        if board is not None:
            return self.copy(board) 
            
        disp.brd = self
        self.disp = disp
        self.startHandSize = startHandSize
        self.dd = Deck()
        self.a = []
        self.b = []
        self.c = []
        self.d = []
        self.e = []

        self.player1 = player1
        self.player2 = player2

        self.pd1 = PlayerData()
        self.pd2 = PlayerData()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def copy(self, brd=None):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if brd is None:
            return Board(None, None, None, None, self)

        self.startHandSize = brd.startHandSize
        self.dd = brd.dd.copy()
        self.a = brd.a[:]
        self.b = brd.b[:]
        self.c = brd.c[:]
        self.d = brd.d[:]
        self.e = brd.e[:]

        self.player1 = brd.player1
        self.player2 = brd.player2
        self.pd1 = brd.pd1.copy()
        self.pd2 = brd.pd2.copy()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getPD(self, player):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return self.pd1 if player is self.player1 else self.pd2

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getRow(self, rowLetter):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return getattr(self, rowLetter)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getRows(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return [('a', self.a), ('b', self.b), ('c', self.c), ('d', self.d), ('e', self.e)]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def save(self, xn):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        bn = xn.add("<board/>")
        self.dd.save(bn)

        for c, row in self.getRows():
            bn.add('<row name="%s">%s</row>' % (c, saveBlks(row)))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def restore(self, bn):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.dd.restore(bn)
        for rn in bn.findChildren('row'):
            self.getRow(rn['name']).extend(loadBlks(rn.text))

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def blksLeft(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ return num blocks left in draw pile
        """
        return len(self.dd)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def startHand(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        for c, row in self.getRows():
            row.append(self.dd.get())

        for i in range(self.startHandSize):
            self.pd2.setBlk(self.dd.get())
            self.pd1.setBlk(self.dd.get())

        self.pd1.sort()
        self.pd2.sort()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def display(self, player, all):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.disp.display(player, all)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def gs(self, v, c):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        try:
            return self.ll(v).getST(c)
        except IndexError:
            return '  '

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def printErr(self, s, silent):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if not silent:
            self.disp.printInfo(s)
            
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def score(self, p, blk, silent=0):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(blk, Block)

        if self.willScore(blk):
            p.scoreBlk(blk)
            return True
        
        self.printErr("## block will not score", silent)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def willScore(self, blk):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        assert isinstance(blk, Block)
        
        if blk[1] == '0': 
            return True
            
        end2 = self.pd2.getST(blk[0])
        end1 = self.pd1.getST(blk[0])
        return end1.next() == blk or end2.next() == blk

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def ll(self, v):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if isinstance(v, (str, unicode)):
            return self.getRow(v)
        return v

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def score0(self, pp):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ score any zeros
        """
        for blk in pp.findBlks('0'):
            res = self.score(pp, blk)
            assert res
            pp.rmBlk(blk)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def move(self, p, blk, row, silent=0):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ move the blk to end of row (or score)
        """
        assert isinstance(blk, Block)
        if row == 's':
            if self.score(p, blk, silent):
                p.rmBlk(blk)
                return True
            return
            
        rw = self.ll(row)
        end = rw[-1]

        if end.compat(blk):
            rw.append(blk)
            p.rmBlk(blk)
            return True
            
        self.printErr("## cannot put " + str(blk) + " on " + str(end), silent)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def replace(self, p, blk, row0, row1, silent=0):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ blk is a z blk to replace the top element of row0. if row1 is score
            then row0 can only have one element, else see if row0 can be added
            to row1.
        """
        assert isinstance(blk, Block)
        assert(blk[1] == 'z')

        if row0 == row1:
            return self.printErr("## rows not distinct", silent)

        rw0 = self.ll(row0)
        if row1 == 's':
            if len(rw0) != 1:
                return self.printErr("## " + row0 + " len != 1", silent)

            end0 = rw0[-1]

            if self.score(p, end0, silent):
                del rw0[0]
                rw0.append(blk)
                p.rmBlk(blk)
                return True
            return
            
        if self.moveList(p, row0, -1, row1, silent):
            rw0.append(blk)
            p.rmBlk(blk)
            return True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def moveEnd(self, p, row0, row1, check=True, silent=0):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ move blk at end of row0 to end of row1 or score. can't move the
            top most element of a row
        """
        if row0 == row1:
            return self.printErr("## rows not distinct", silent)

        rw0 = self.ll(row0)
        if check and len(rw0) < 2:
            return self.printErr("## " + row0 + " : len < 2", silent)

        end0 = rw0[-1]

        if row1 == 's':
            if self.score(p, end0, silent):
                del rw0[-1]
                return True
            return
            
        rw1 = self.ll(row1)
        end1 = rw1[-1]

        if end1.compat(end0):
            del rw0[-1]
            rw1.append(end0)
            return True
        
        self.printErr("## cannot put " + str(end0) + " with " + str(end1), silent)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def moveEnd3(self, p, row0, row1, row2, silent=0):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ move a z blk at end of row0 to top of row1, moving row1 to end of
            row2 or score
        """
        return self.moveList4(p, row0, -2, row1, row2, silent)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def moveList(self, p, row0, col, row1, silent=0):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ move list starting a [row0,col] to end of row1
        """
        if row0 == row1:
            return self.printErr("## rows not distinct", silent)

        rw0 = self.ll(row0)
        idx = getIdx(col, 1)
        try:
            blk = rw0[idx]
        except IndexError:
            return self.printErr("## - illegal block specified", silent)

        rw1 = self.ll(row1)
        end1 = rw1[-1]

        ## see if it can go on end
        if end1.compat(blk):
            rw1.extend(rw0[idx:])
            del rw0[idx:]
            return True
            
        end0 = rw0[-1]

        ## see if end of this list can move, if so unwind list
        if end1.compat(end0):
            while end0 != blk:
                res = self.moveEnd(p, row0, row1, silent=silent)
                assert res
                end0 = rw0[-1]
                
            return self.moveEnd(p, row0, row1, check=False, silent=silent)
            
        self.printErr("## block " + str(blk) + " not compatible with " + str(end0), silent)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def moveList4(self, p, row0, col, row1, row2, silent=0):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        """ move list [row0,col] (must start w/ a z) to top of row1 moving row1
            to row2 or score
        """
        #print row0, col, row1, row2
        if row0 == row1 or row0 == row2 or row1 == row2:
            return self.printErr("## rows not distinct", silent)

        rw0 = self.ll(row0)
        idx = getIdx(col, 1)

        try:
            blk = rw0[idx]
        except IndexError:
            return self.printErr("## - illegal block specified", silent)

        if blk[1] != 'z':
            return self.printErr("## - list starts w/ blk not z", silent)

        rw1 = self.ll(row1)
        if row2 == 's':
            if len(rw1) != 1:
                return self.printErr("## " + row1 + " len != 1", silent)

            blk1 = rw1[-1]
            if not self.score(p, blk1, silent):
                return
                
            del rw1[-1]
            assert len(rw1) == 0
            rw1.extend(rw0[idx:])
            del rw0[idx:]
            assert len(rw0) > 0
            return True
            
        if self.moveList(p, row1, -1, row2):
            assert len(rw1) == 0
            rw1.extend(rw0[idx:])
            del rw0[idx:]
            assert len(rw0) > 0
            return True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getEndBlks(self, typ='all'):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return [(r[0], r[1][-1]) for r in self.getRows() if typ != 'useable' or len(r[1]) > 1]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getBegBlks(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return [(r[0], r[1][0]) for r in self.getRows()]

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getRandBlk(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        r = self.getRow(random.choice(['a','b','c','d','e']))
        try:
            idx = random.randint(1, len(r)-1)
        except ValueError:
            idx = 0
        return r[idx], r, idx

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getBlks(self, blks, ignCol0=False):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ans = []
        for r, row in self.getRows():
            for col, blk in enumerate(self.row):
                if ignCol0 and col == 0:
                    continue
                if str(blk) in blks:
                    ans.append((row, col, blk))
        return ans

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getIdxInRow(self, blk, row, offset):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        try:
            r = self.getRow(row)
            idx = r.index(blk)
            if offset == 0:
                return idx

            ii = idx + offset
            if ii < 0: return None
            r[ii]
            return ii
        except (ValueError, IndexError):
            pass

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def validation(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        def ps(blk):
            return str(blk)
            
        blks = []
        blks.extend(self.a)
        blks.extend(self.b)
        blks.extend(self.c)
        blks.extend(self.d)
        blks.extend(self.e)
        blks.extend(self.dd.d)

        blks.extend(self.pd1.blks)
        blks.extend(self.pd2.blks)

        for b in self.pd1.score_tray.values():
            blks.extend(b)
        for b in self.pd2.score_tray.values():
            blks.extend(b)

        s = set([str(d) for d in blks])
        if len(blks) != BLK_COUNT:
            print("block count wrong", len(blks), BLK_COUNT)
            
        if s != ALL_BLOCKS:
            print('sets unequal')
            print(s)
            print(ALL_BLOCKS)
            print(s - ALL_BLOCKS)
            print(ALL_BLOCKS - s)
            
        return len(blks) == BLK_COUNT and s == ALL_BLOCKS


def showExec(s, loc, silent=1):
    if not silent:
        print(s)
    exec s in globals(), loc


#-------------------------------------------------------------------------------
def __test__(silent=True):
#-------------------------------------------------------------------------------
    """
    used for automated module testing. see L{tester}
    """
    ###import pylib.tester as tester

    class Display(object):
        def printInfo(self, s):
            if not silent:
                print(s)

        def printBrd(self, brd):
            if not silent:
                print()
                for c, row in brd.getRows():
                    printBlks(c, row)


    class Player(object):
        def printHand(self):
            if not silent:
                printBlks('hand', self.pd.blks)

        def printScore(self):
            if not silent:
                print()
                for c, row in self.pd.getSTrays():
                    printBlks(c, row)

        def show(self):
            if not silent:
                self.printHand()
                self.printScore()

        def get(self, s):
            return self.pd.findBlk(s)

        def set(self, s):
            for blk in loadBlks(s):
                self.pd.setBlk(blk)

    class TestDeck(Deck):
        def __init__(self):
            self.d = loadBlks('=5,-5,@0,*0,=1,||,*6,||,-x,||,=z,||,*y,||,||,||,||,||,||,||')



    disp = Display()
    p1 = Player()
    brd = Board(p1, Player(), disp)
    brd.dd = TestDeck()
    brd.startHand()

    disp.printBrd(brd)
    p1.show()

    showExec("brd.move(p1.pd, p1.get('*6'), 'a')", locals(), silent)

    disp.printBrd(brd)
    p1.show()

    showExec("brd.moveEnd(p1.pd, 'a', 'b')", locals(), silent)
    disp.printBrd(brd)
    p1.show()

    showExec("brd.moveEnd(p1.pd, 'a', 'b')", locals(), silent)
    disp.printBrd(brd)
    p1.show()

    p1.set('-7,@8,=7,@6,@z,-z,=0,*z,-y,=y,-0')

    if not silent:
        printBlks('before', p1.pd.blks)
        printBlks('saves', p1.pd.getBlks('saves'))
        printBlks('all, low', p1.pd.getBlks('all'))
        printBlks('all, high', p1.pd.getBlks('all' 'high'))
        printBlks('!all, low', p1.pd.getBlks('play'))
        printBlks('!all, high', p1.pd.getBlks('play', 'high'))

    showExec("brd.move(p1.pd, p1.get('-7'), 'b')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('@8'), 'b')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('@6'), 'b')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('=7'), 'b')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('@6'), 'b')", locals(), silent)

    disp.printBrd(brd)
    p1.show()

    showExec("brd.moveEnd(p1.pd, 'b', 'a')", locals(), silent)
    showExec("brd.moveList(p1.pd, 'b', 'k', 'a')", locals(), silent)
    showExec("brd.moveList(p1.pd, 'b', '2', 'a')", locals(), silent)
    disp.printBrd(brd)
    p1.show()

    showExec("brd.replace(p1.pd, p1.get('@z'), 'd', 'c')", locals(), silent)
    p1.show()
    showExec("brd.replace(p1.pd, p1.get('@z'), 'e', 'c')", locals(), silent)
    disp.printBrd(brd)
    p1.show()

    showExec("brd.replace(p1.pd, p1.get('-z'), 'd', 's')", locals(), silent)
    showExec("brd.replace(p1.pd, p1.get('=z'), 'c', 's')", locals(), silent)
    disp.printBrd(brd)
    p1.show()

    showExec("brd.move(p1.pd, p1.get('=0'), 's')", locals(), silent)
    p1.show()

    showExec("brd.moveEnd(p1.pd, 'c', 's')", locals(), silent)
    disp.printBrd(brd)
    p1.show()

    showExec("brd.move(p1.pd, p1.get('*y'), 'd')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('=z'), 'd')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('-y'), 'e')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('*z'), 'e')", locals(), silent)
    showExec("brd.move(p1.pd, p1.get('=y'), 'e')", locals(), silent)
    showExec("brd.moveEnd3(p1.pd, 'd', 'b', 'a')", locals(), silent)
    showExec("brd.moveList4(p1.pd, 'e', '1', 'c', 's')", locals(), silent)
    showExec("brd.score0(p1.pd)", locals(), silent)
    disp.printBrd(brd)
    p1.show()
    return 0


#-------------------------------------------------------------------------------
if __name__ == "__main__":
#-------------------------------------------------------------------------------
    import pylib.osscripts as oss

    args, opts = oss.gopt(oss.argv[1:], [], [], __test__.__doc__)

    res = not __test__(silent=False)
    oss.exit(res)

