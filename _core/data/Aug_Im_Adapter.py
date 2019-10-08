import functools as _functools
import inspect as _inspect
import re as _re
from .types import Aug_Im as _Aug_Im
import tensorflow as _tf
import tensorflow.image as _tfi
from tensorflow.contrib.image import rotate as _rotate
import cv2 as _cv2
import collections as _collections
import numpy as _np


class Aug_Im_Adapter:
    #def __call__(self, f):
    def __init__(self, f):
        self.old_f = f
        self.f_code = _inspect.getsource(f)
        self.new_f_code = ''
        self.param_modifier()
        #self.hyperparam_to_attr()
        self.generate_new_f()
    
    def __call__(self):    
        @_functools.wraps(self.new_f)
        def aug_im_compatible_f(augim):
            result = _Aug_Im(Id = augim.Id + '_' + self.new_f.__name__)
            result.im = self.new_f(augim)
            result.im_info = ''
            return result
        
        return aug_im_compatible_f
        
    def param_modifier(self):
        first_line = self.f_code.split('\n')[0]
        params = _re.search('\(.*\)', first_line).group()[1:-1]
        params = _re.split(',[ ]*', params)
        self.new_f_code = ['def ' + self.old_f.__name__ + '(augim):']
        self.new_f_code.extend(['    ' + p + ' = augim.' + p for p in params])
        self.new_f_code.extend(self.f_code.split('\n')[1:])
        pasted_code = ''
        for line in self.new_f_code:
            pasted_code += line + '\n'
        self.new_f_code = pasted_code
    
    def hyperparam_to_attr(self):
        hyp_names = _re.findall(r'\b[A-Z]+[A-Z_0-9]*\b', self.f_code)
        for hyp_name in set(hyp_names):
            self.new_f_code = self.new_f_code.replace(
                hyp_name, self.old_f.__name__ + '.' + hyp_name)
            
    def generate_new_f(self):
        code_to_execute = self.new_f_code + '\nself.new_f = ' + self.old_f.__name__
        exec(code_to_execute)
        
'''class Aug_Im_Compatible_f():
    def __init__(self, f):
        self.__name__ = f.__name__ + 'AugImComp'
        self._f = f
        self.__call__ = 
        
    def __call__(self, augim):
        result = _Aug_Im(Id = augim.Id + '_' + self.__name__)
        result.im = self._f(augim)
        result.im_info = ''
        return result'''
        
        