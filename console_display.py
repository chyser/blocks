"""
"""


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import


import pylib.osscripts as oss
import display


#-------------------------------------------------------------------------------
class Console(display.Display):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        display.Display.__init__(self)
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def write(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        s = ' '.join([str(a) for a in args])
        oss.write(s)
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def writeln(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        s = ' '.join([str(a) for a in args])
        self.write(s + '\n')
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getInput(self, player):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        while 1:
            ch = raw_input(">> ")
            try:
                if ch[0] in "0123456789":
                    return str(player.pd.blks[int(ch[0])]) + ch[1:]
                    
                if ch[0] == ',':
                    return str(player.pd.blks[10]) + ch[1:]
                    
                return ch
            except IndexError:
                pass
                
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def border(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        pass

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def display(self, p, all=False):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.border()
        self.write("[%2d]   "  % self.brd.blksLeft())
        self.writeln("0  1  2  3  4  5  6  7  8  9  f  g  h  i  j  k  l  m  n  o  p  q  r  s  t  u  v"[:(self.dl()-1)*3])
        self.writeln("a: " + ' '.join([str(s) for s in self.brd.a]))
        self.writeln("b: " + ' '.join([str(s) for s in self.brd.b]))
        self.writeln("c: " + ' '.join([str(s) for s in self.brd.c]))
        self.writeln("d: " + ' '.join([str(s) for s in self.brd.d]))
        self.writeln("e: " + ' '.join([str(s) for s in self.brd.e]))
        
        self.writeln()
        self.writeln("[%s] [%s] [%s] [%s] - %3d/%6.2f  -- %s" % (
            self.brd.gs(self.brd.player2.pd, '-'),
            self.brd.gs(self.brd.player2.pd, '='),
            self.brd.gs(self.brd.player2.pd, '*'),
            self.brd.gs(self.brd.player2.pd, '@'),
            self.brd.player2.pd.rndScore,
            self.brd.player2.gameScore,
            self.brd.player2.name))
            
        self.writeln("[%s] [%s] [%s] [%s] - %3d/%6.2f  -- %s ***" % (
            self.brd.gs(self.brd.player1.pd, '-'),
            self.brd.gs(self.brd.player1.pd, '='),
            self.brd.gs(self.brd.player1.pd, '*'),
            self.brd.gs(self.brd.player1.pd, '@'),
            self.brd.player1.pd.rndScore,
            self.brd.player1.gameScore,
            self.brd.player1.name))
            
        self.writeln("")
        if p is None:
            if all:
                self.writeln((' '.join([str(s) for s in self.brd.player2.pd.blks])) + ("  -- %s" % self.brd.player2.name))
                self.writeln((' '.join([str(s) for s in self.brd.player1.pd.blks])) + ("  -- %s" % self.brd.player1.name))
            else:
                self.writeln(('## '*(self.brd.player2.pd.numBlks())) + (" -- %s"  % self.brd.player2.name))
                self.writeln(('## '*(self.brd.player1.pd.numBlks())) + (" -- %s"  % self.brd.player1.name))
            s = max(self.brd.player1.pd.numBlks(), self.brd.player2.pd.numBlks())
            self.writeln(" 0  1  2  3  4  5  6  7  8  9  ,"[:s*3])
            
        elif p == self.brd.player1:
            if all:
                self.writeln((' '.join([str(s) for s in self.brd.player2.pd.blks])) + ("  -- %s" % self.brd.player2.name))
            else:
                self.writeln(('## '*(self.brd.player2.pd.numBlks())) + (" -- %s"  % self.brd.player2.name))
            self.writeln((' '.join([str(s) for s in self.brd.player1.pd.blks])) + ("  -- %s" % self.brd.player1.name))
            self.writeln(" 0  1  2  3  4  5  6  7  8  9  ,"[:(self.brd.player1.pd.numBlks())*3])
                        
        elif p == self.brd.player2:
            if all:
                self.writeln((' '.join([str(s) for s in self.brd.player1.pd.blks])) + ("  -- %s" % self.brd.player1.name))
            else:
                self.writeln(('## '*(self.brd.player1.pd.numBlks())) + (" -- %s"  % self.brd.player1.name))
            self.writeln((' '.join([str(s) for s in self.brd.player2.pd.blks])) + ("  -- %s" % self.brd.player2.name))
            self.writeln(" 0  1  2  3  4  5  6  7  8  9  ,"[:(self.brd.player2.pd.numBlks())*3])
        self.writeln()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def printInfo(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if args:
            self.write('\n')
            for a in args:
                self.write(str(a), ' ')
        self.write('\n')
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getFileName(self, msg, exists):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        while 1:
            fn = raw_input(msg + ' ')
                        
            if fn == 'CANCEL':
                return None
                
            if exists:
                if oss.exists(fn):
                    return fn
                print("no such file")
                
            else:
                if oss.exists(fn):
                    print("file exists")
                    c = raw_input("overwrite? (y/n)")
                    if c in "Yy":
                        return fn
                else:
                    return fn
                    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def getPlayerName(self, msg):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        while 1:
            name = raw_input(msg + ' ')
            if name:
                return name
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def HideAll(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.clear()
        self.display(None)
        raw_input('press any key to begin')
                
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def CompPause(self, plyr):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.display(plyr, True)
        raw_input('\nany key to continue\n\n')
                        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def clear(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        print(((' '*200) + '\n')*100)
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dl(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        return max(len(self.brd.a), len(self.brd.b), len(self.brd.c), len(self.brd.d), len(self.brd.e))
        
                            
#-------------------------------------------------------------------------------
def ObjectFactory():
#-------------------------------------------------------------------------------
    return Console()
    
