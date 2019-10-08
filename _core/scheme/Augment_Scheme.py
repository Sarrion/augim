'''
Class whose object instances contains the application schemme of augments.
'''
from re import search as _search
from secrets import token_hex as _randstr
from ..data.types import Aug_Scheme
from ..data.defaults.default_augments import default_augments
from ..data.defaults.default_scheme import default_transitory, default_stable
from .functions import _extract, _is_int, _to_int, _is_slice, _to_slice
from .Augment_Scheme_Inspector import Augment_Scheme_Inspector as _ASI 

class Augment_Scheme():
    def __init__(self, 
                 augments_list = default_augments,
                 transitory = default_transitory,
                 stable = default_stable):
        self.Id = _randstr(6) + '_augment_schemme'
        self.augments = augments_list
        self.transitory = transitory
        self.stable = stable
        self._ini_deq_components = {'original' : slice(0,1)}
        self._ini_deq_idx = 1
        
    _required_words = set(['take', 'pick', 'apply', 'name_it'])
    _substitution_words = set(['all', 'all_except'])
    _inspect = _ASI()
        
    def add(self, attribute, element):
        if attribute in ('transitory', 'stable', 'augments'):
            self._inspect(attribute, element)
            self.__dict__[attribute] = element
            
    def parse(self):
        result = Aug_Scheme()
        result.transitory = self._parse_transitory()
        result.stable = self._parse_stable()
        result.ini_deq_components = self._ini_deq_components
        return result
    
    def _parse_transitory(self):
        transitory_scheme = []
        for sentence in self.transitory:
            parsed_sentence = {}
            parsed_sentence['take'], n_im = self._take(sentence)
            parsed_sentence['pick'], n_im = self._pick(sentence, n_im)
            parsed_sentence['apply'], n_aug = self._apply(sentence)
            parsed_sentence['name_it'] = self._name_it(sentence)
            
            new_comp = slice(self._ini_deq_idx, self._ini_deq_idx + n_im * n_aug)
            self._ini_deq_components[parsed_sentence['name_it']] = new_comp
            self._ini_deq_idx += n_im * n_aug
            
            transitory_scheme.append(parsed_sentence)
        return transitory_scheme
    
    def _parse_stable(self):
        return self.stable.split(',')
    
    def _take(self, sentence):
        take_token = _extract('take', sentence)
        component = self._ini_deq_components[take_token]
        n_im = component.stop + component.start
        return component, n_im
        
    def _pick(self, sentence, n_im):
        pick_token = _extract('pick', sentence)
        if pick_token == 'all':
            pick_token = ':'
        elif _search('all_except', pick_token) != None:
            pick_token = pick_token.split(' ')[1]
            reverse_pick_token = ':'
            for n in pick_token.split(','):
                if _is_int(n):
                    reverse_pick_token += n + ',' + str(_to_int(n)+1) + ':'
                    n_im -= 1
                elif _is_slice(n):
                    n = _to_slice(n)
                    reverse_pick_token += str(n.start) + ',' + str(n.stop+1) + ':'
                    n_im -= n.stop - n.start
            pick_token = reverse_pick_token
        else:
            n_im = 0
            for n in pick_token.split(','):
                if _is_int(n): 
                    n_im += 1
                elif _is_slice(n):
                    n = _to_slice(n)
                    n_im += n.stop - n.start
        return pick_token, n_im
    
    def _apply(self, sentence):
        apply_token = _extract('apply', sentence)
        augment_names = [x for x in self.augments.__dict__.keys() if x[0] != '_']
        if apply_token == 'all':
            applied_augments = augment_names
        elif _search('all_except', apply_token) != None:
            not_applied_augments = apply_token.split(' ')[1].split(',')
            applied_augments = [x for x in augment_names if x not in not_applied_augments]
        else:
            applied_augments = apply_token.split(',')
        return applied_augments, len(applied_augments)
    
    def _name_it(self, sentence):
        name_it_token = _extract('name_it', sentence)
        return name_it_token
    