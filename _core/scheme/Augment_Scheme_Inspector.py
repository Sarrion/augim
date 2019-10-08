class Augment_Scheme_Inspector():
            
    _required_words = set(['take', 'pick', 'apply', 'name_it'])
    _substitution_words = set(['all', 'all_except'])
    
    def __call__(self, attribute, element):
        if attribute == 'stable':
            self._inspect_stable(element)
        elif attribute == 'augments':
            self._inspect_augments(element)
        elif attribute == 'transitory':
            self._inspect_transitory(element)
    
    
    def _inspect_stable(self, stable_scheme):
        allowed_tokens = [x.__name__ for x in self.augments.list]
        for sentence in stable_scheme:
            for token in sentence.split(','):
                if token not in allowed_tokens:
                    raise Exception(token + ' is not an augment name function.')
    
    
    def _inspect_augments(self, element):
        if not isinstance(element, Augments):
            raise Exception(element + ' has to be an Augments data type.')
        
        
    def _inspect_transitory(self, transitory_scheme):
        for sentence in transitory_scheme:
            sentence = sentence.lower()
            self._inspect_transitory_required_words(sentence)
            self._inspect_take_token(sentence)
            self._inspect_pick_token(sentence)
            self._inspect_apply_token(sentence)
            self._inspect_name_it_token(sentence)
            
                        
    def _inspect_transitory_required_words(self, sentence):
        structure = '^take (.+?) pick (.+?) apply (.+?) name_it (.+?)$'
        if _search(structure, sentence) == None:
            raise Exception('The sentence: \n' + sentence +
                        '.\n Doesn´t have the structrure:\n' + structure)
    
    def _inspect_take_token(self, sentence):
        take_token = _extract('take', sentence)
        if take_token not in self._initial_deq_components.keys():
            raise Exception(take_token + ' referenced before creation.')
    
    def _inspect_pick_token(self, sentence):
        pick_token = _extract('pick', sentence)
        pick_token = pick_token.split(' ')
        if _is_all_except_word(pick_token[0]):
            pick_token = pick_token[1:]
        for element in pick_token[0].split(','):
            if not (_is_int(element) or _is_slice(element) or element == 'all'):
                raise Exception(element + ' is a bad token.')
    
    def _inspect_apply_token(self, sentence):
        apply_token = _extract('apply', sentence)
        apply_token = apply_token.split(' ')
        allowed_tokens = [x.__name__ for x in self.augments.list]
        
        if _is_all_except_word(apply_token[0]):
            apply_token = apply_token[1:]
        for element in apply_token[0].split(','):
            if element not in allowed_tokens.append('all'):
                raise Exception(element + ' is not an augment function name')
            
    def _inspect_name_it_token(self, sentence):
        sentence = sentence.split(' ')
        if sentence[-1] == 'name_it':
            raise print('There is not a name for this deque component')
        self._allowed_take_tokens.append(sentence[-1])
                