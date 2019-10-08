from time import time as _time    
from re import search as _search
from ..scheme.functions import _is_int, _to_int, _is_slice, _to_slice
from secrets import token_hex as _randstr    
import collections as _collections

class Aug_Original_Im():
    '''
    Aug_Original_Im is the basic input data which contains the original
    image and other data needed for certain augmentations.
    '''

    def add(self, name, value):
        self.__dict__[name] = value
        

class Aug_Original_Im_Batch():
    '''
    Output of the augmentable_data_formatter function and input of the Augmenter
    object, contains the Aug_Original_Im's to be augmented.
    
    Attrs:
    ------
        - Id: Composed of the word "batch", and the current time.
        - batch: List of Aug_Original_Im's.
        - batch_info: Relevant information about the batch.
    '''
    
    def __init__(self):
        self.Id = _randstr(6) + '_batch'
        self.batch = []
        self.batch_info = []
        
    def add(self, element):
        if isinstance(element, Aug_Original_Im):
            self.batch.append(element)
        if isinstance(element, Aug_Original_Im_Batch):
            self.batch.extend(element.batch)
                
        
class Aug_Im():
    '''
    Aug_Im is the most basic data type produced in the module execution.
    
    Attrs:
    -----
        - Id: Composed of the original image id and an index.
        - im: The augmented image.
        - im_info: A list of ordered transformations applied
            to obtain the im.
    '''
    def __init__(self, Id, im = None, im_info = []):
        self.Id = Id
        self.im = im
        self.im_info = im_info
        
        
class Aug_Im_Batch():
    from time import time as _time
    '''
    Aug_Im_Batch contains the Aug_Im's produced from a unique Aug_Original. 
    
    Attrs:
    ------
        - Id: Composed of the original image id, the word "_batch_", 
            and the current time.
        - batch: List of Aug_Im.
        - batch_info: Relevant information about the batch.
    '''
    def __init__(self, Id):
        self.Id = Id + '_batch_' + str(_time())
        self.batch = []
        self.batch_info = []

        
class Aug_Im_Batches():
    '''
    Aug_Im_Batches is the output of an Augmenter execution and contains one
    Aug_Batch for each Aug_Original in Aug_Original_Batch. 
    
    Attrs:
    ------
        - Id: Composed of the original image id, the word "_batch_", 
            and the current time.
        - batches: List of Aug_Im_Batch.
        - batches_info: Relevant information about batches.
    '''
    def __init__(self):
        self.Id = _randstr(6) + '_batches'
        self.batches = []
        self.batches_info = []
        

class Aug_Scheme():
    def __init__(self):
        self.ini_deq_components = {}
        self.transitory = []
        self.stable = []
    
        
class List(list):
    def __init__(self, data):
        self.data = data
    def __getitem__(self, indexes):
        result = []
        if isinstance(indexes, tuple):
            for index in indexes:
                if isinstance(index, int):
                    result.append(self.data[index])
                if isinstance(index, slice):
                    result.extend(self.data[index])
        elif isinstance(indexes, str):
            for word in indexes.split(','):
                if _is_int(word):
                    result.append(self.data[_to_int(word)])
                if _is_slice(word):
                    result.extend(self.data[_to_slice(word)])
        else:
            result = self.data[indexes]
        return result

    
class Deque():
    def __init__(self, data = []):
        if isinstance(data, list):
            self.data = _collections.deque(data)
    def append(self, element):
        self.data.append(element)
    def appendleft(self, element):
        self.data.appendleft(element)
    def extend(self, element):
        self.data.extend(element)
    def extendleft(self, element):
        self.data.extendleft(element)
    def pop(self):
        return self.data.pop()
    def popleft(self):
        return self.data.popleft()
    def __repr__(self):
        return 'Deque' + str(self.data)[5:]
    def __getitem__(self, indexes):
        result = []
        deq_cont = list(self.data)
        if isinstance(indexes, tuple):
            for index in indexes:
                if isinstance(index, int):
                    result.append(deq_cont[index])
                if isinstance(index, slice):
                    result.extend(deq_cont[index])
        elif isinstance(indexes, str):
            for word in indexes.split(','):
                if _is_int(word):
                    result.append(deq_cont[_to_int(word)])
                if _is_slice(word):
                    result.extend(deq_cont[_to_slice(word)])
        else:
            result = deq_cont[indexes]
        return Deque(result)
    
    def __iter__(self):
        return iter(self.data)
    def __next__(self):
        return next(self.data)
    def __len__(self):
        return len(self.data)