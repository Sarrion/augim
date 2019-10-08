from re import search as _search
from re import sub as _sub


def _is_int(input_str):
    if _search('^[-0-9]+$', input_str) == None:
        return False
    else:
        return True

def _to_int(slice_str):
    return int(slice_str)

def _is_slice(input_str):
    if _search('^[-0-9]*:[-0-9]*$', input_str) == None:
        return False
    else:
        return True

def _to_slice(slice_str):  
    slice_list = slice_str.split(':')
    start = int(slice_list[0]) if _is_int(slice_list[0]) else 0
    stop =  int(slice_list[1]) if _is_int(slice_list[1]) else None
    return slice(start, stop)

def _is_all_except_word(input_str):
    if input_str == 'all_except':
        return True
    else:
        return False

def _is_subst_word(input_str):
    if input_str in ('all', 'all_except'):
        return True
    else:
        return False

def _extract(token, sentence):
    tokens = ('take', 'pick', 'apply', 'name_it', '$')
    token_idx = {'take' : 0, 'pick' : 1, 'apply' : 2, 'name_it' : 3}
    left_token = tokens[token_idx[token]]
    right_token = tokens[token_idx[token] + 1]
    result = _search(left_token + '(.+?)' + right_token, sentence)
    result = _sub('take|pick|apply|name_it', '', result.group())
    result = result.strip()
    return result

