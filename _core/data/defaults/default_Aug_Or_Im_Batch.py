from ..Input_Data_Formatter import Input_Data_Formatter as _IDF
import pandas as _pd
from re import search as _search

#import ipdb
#ipdb.set_trace()

_curr_dir = _search('.*/', __file__).group()

_idf = _IDF()
_idf.add_sources(_curr_dir + 'default_ims/')
meta = _pd.read_csv(_curr_dir + 'default_metadata.csv')
_idf.add_metadata(meta)

default_aug_original_im_batch = _idf.get_results()