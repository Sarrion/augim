'''
Class whose object instances contains the functions to be used in the augmentation process.
'''



class Augments():
    def __init__(self):
        self._augment_name_list = []
        
    def add(self, element):
        if isinstance(element, list):
            for i in element:
                if i.__class__.__name__ == 'function':
                    self.__dict__[i.__name__] = i
                    self._augment_name_list.append(i.__name__)
                else:
                    raise Exception(str(i) + ' is not a function.')
        elif element.__class__.__name__ == 'function':
            self.__dict__[element.__name__] = element
            self._augment_name_list.append(element.__name__)
        else:
            raise Exception(str(element)+' is not a function or list of functions.')
        
    '''def __getitem__(self, attr_name):
        return getattr(self, attr_name)'''
    
    def __iter__(self):
        self._i = 0
        self._l = len(self._augment_name_list)
        return self
    
    def __next__(self):
        if self._i < self._l:
            self._i += 1
            return getattr(self, self._augment_name_list[self._i - 1])
        else:
            raise StopIteration
    