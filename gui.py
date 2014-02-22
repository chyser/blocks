#!/usr/bin/env python
"""
Library:
    
"""
    
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import pylib.osscripts as oss
import display

#-------------------------------------------------------------------------------
def __test__():
#-------------------------------------------------------------------------------
    """
    used for automated module testing. see L{tester}
    """
    import pylib.tester as tester
    return 0
    
#-------------------------------------------------------------------------------
if __name__ == "__main__":
#-------------------------------------------------------------------------------
    import pylib.osscripts as oss
    
    args, opts = oss.gopt(oss.argv[1:], [], [], __test__.__doc__)
    
        
    
    res = not __test__()
    oss.exit(res)
    
