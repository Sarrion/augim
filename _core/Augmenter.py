from .data.types import *
from .data.Aug_Im_Adapter import Aug_Im_Adapter as _Adapter
from .scheme.Augment_Scheme import Augment_Scheme

from .data.Input_Data_Formatter import Input_Data_Formatter
IDF = Input_Data_Formatter()

import tensorflow as _tf

class Augmenter():
    def __call__(self, originals = IDF.get_results(),
                 scheme = Augment_Scheme(), augment_req = 100):
        '''import ipdb
        ipdb.set_trace()'''
        self.originals = originals
        self.scheme = scheme
        self._parsed_scheme = scheme.parse()
        
        self.augments = {}
        for f in scheme.augments:
            _adapter = _Adapter(f)
            self.augments[f.__name__] =  _adapter()
        self._augment_req = augment_req
        self._aug_im_batches = Aug_Im_Batches()
        self._deque = Deque()
        
        self.augment()
        
        return self._aug_im_batches
    
    def augment(self):
        for original in self.originals.batch:
            self._aug_im_batches.batches.append(self._augment(original))
    
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
                
    def _generate_deque_component(self, sentence):
        for aug_im in self._deque[sentence['take']][sentence['pick']]:
            for augment_name in sentence['apply']:
                new_component = self.augments[augment_name](aug_im)
                self._deque.append(new_component)
                
    def _apply_stable(self, working_im, how_many = 'all'):
        if how_many == 'all':
            augment_names = self._parsed_scheme.stable
        elif isinstance(how_many, int):
            augment_names = self._parsed_scheme.stable[:how_many]
            
        for augment_name in augment_names:
                new_component = self.augments[augment_name](working_im)
                self._deque.append(new_component)