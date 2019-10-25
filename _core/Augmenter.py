#from memory_profiler import profile
import gc
#import time

from .data.types import *
from .data.Aug_Im_Adapter import Aug_Im_Adapter as _Adapter
from .scheme.Augment_Scheme import Augment_Scheme

from .data.Input_Data_Formatter import Input_Data_Formatter
IDF = Input_Data_Formatter()

import tensorflow as _tf


class Augmenter():
    #@profile
    def __init__(self, originals = IDF.get_results(),
                 scheme = 'default', augment_req = 100):
        self.originals = originals
        if scheme == 'default':
            self.scheme = Augment_Scheme()
        else:
            self.scheme = scheme
        
        self.augments = {}
        for f in self.scheme.augments:
            _adapter = _Adapter(f)
            self.augments[f.__name__] =  _adapter()
        self._augment_req = augment_req
        self._deque = Deque()
        
   #@profile
    def augment(self):
        result = Aug_Im_Batches()
        self._parsed_scheme = self.scheme.parse()
        for original in self.originals.batch:
            result.batches.append(self._augment(original))
        gc.collect()
        return result
    
    #@profile
    def _augment(self, original):
        result = Aug_Im_Batch(original.Id)
        self._deque.append(original)
        for sentence in self._parsed_scheme.transitory:
            self._generate_deque_component(sentence)
        if self._augment_req <= len(self._deque):
            for _ in range(self._augment_req):
                result.batch.append(self._deque.popleft())
        else:
            remaining_n_augments = (self._augment_req - len(self._deque))
            stable_len = len(self._parsed_scheme.stable)
            stable_n_iters =  remaining_n_augments // stable_len
            residual_n = remaining_n_augments % stable_len
            for _ in range(stable_n_iters):
                working_im = self._deque.popleft()
                result.batch.append(working_im)
                self._apply_stable(working_im)

            working_im = self._deque.popleft()
            result.batch.append(working_im)
            self._apply_stable(working_im, residual_n)
            for _ in range(len(self._deque)):
                result.batch.append(self._deque.popleft())
        return result
    #@profile            
    def _generate_deque_component(self, sentence):
        for aug_im in self._deque[sentence['take']][sentence['pick']]:
            for augment_name in sentence['apply']:
                new_component = self.augments[augment_name](aug_im)
                self._deque.append(new_component)
    #@profile            
    def _apply_stable(self, working_im, how_many = 'all'):
        if how_many == 'all':
            augment_names = self._parsed_scheme.stable
        elif isinstance(how_many, int):
            augment_names = self._parsed_scheme.stable[:how_many]
            
        for augment_name in augment_names:
            new_component = self.augments[augment_name](working_im)
            self._deque.append(new_component)
        #gc.collect()