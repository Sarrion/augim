'''
Submodule containing functions related with input output formats of the augim application.

Functions:
----------
    im_path()
    
    
'''

import os as _os



def im_path(im_name, sources, extension = '.jpg'):
    for source in sources:
        potential_path = source + '/' + im_name + extension
        if _os.path.exists(potential_path):
            return potential_path