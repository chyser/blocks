"""
"""


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import


import pylib.osscripts as oss
import console_display


#-------------------------------------------------------------------------------
class Log(console_display.Console):
#-------------------------------------------------------------------------------
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        console_display.Console.__init__(self)
        self.otf = open("log.disp", 'w')
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def write(self, *args):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        s = ' '.join([str(a) for a in args])
        oss.write(s)
        self.otf.write(s)
        self.otf.flush()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def border(self):
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self.writeln('-' * 40)
                        
#-------------------------------------------------------------------------------
def ObjectFactory():
#-------------------------------------------------------------------------------
    return Log()
    
