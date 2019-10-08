from pandas import DataFrame as _df
from pandas import read_csv as _r_csv
from tensorflow import read_file as _read
from tensorflow.image import decode_jpeg as _dec_jpeg
from .functions import im_path as _im_path    
from .types import Aug_Original_Im, Aug_Original_Im_Batch




class Input_Data_Formatter():
    '''The class that manages the augmentable input data in order to provide a 
    feedable format for the Augmenter class.'''
    
    
    def __init__(self, 
         sources = ['/augim/_core/data/defaults/default_ims'],
         metadata = [_r_csv('/augim/_core/data/defaults/default_metadata.csv')]):
        self.sources = sources
        self.metadata = metadata
        self.data = []
    
    # Below are the methods related with the adition of input data
    def add_sources(self, newsource):
        if isinstance(newsource, list):
            self.sources.extend(newsource)
        if isinstance(newsource, str):
            self.sources.append(newsource)
        
    def add_metadata(self, newmetadata):
        self.metadata.append(newmetadata)
        
    def add_data(self, newdata):
        self.metadata.append(newdata)
    
    # Below are the methods related with the formatting of input data
    def get_results(self):
        result_batch = Aug_Original_Im_Batch()                  
        if self.metadata != [] and self.sources != []:
            result_batch.add(
                self.format_metadata(self.metadata, self.sources)
            )           
        if self.data != []:
            result_batch.add(self.format_data(self.data))                  
        return result_batch
    
    def format_metadata(self, metadata, sources):
        result_batch = Aug_Original_Im_Batch()
        for i in metadata:
            if isinstance(i, _df):
                result_batch.add(self.format_df(i, sources))
            if isinstance(i, dict):
                result_batch.add(self.format_dict(i, sources))
        return result_batch
    
    def format_df(self, df, sources):
        result_batch = Aug_Original_Im_Batch()
        
        for i in range(df.shape[0]):
            result = Aug_Original_Im()
            row = df.iloc[i]
            image = _dec_jpeg(_read(_im_path(row['Id'], sources)))
            result.add(name = 'im', value = image)
            for var in row.keys().tolist():
                result.add(name = var, value = row[var])
            result_batch.add(result)
        return result_batch
                              
    def format_dict(self, dic, sources):
        result = Aug_Original_Im()
        image = _read(_dec_jpeg(_im_path(row['Id'], sources)))
        result.add(name = 'im', value = image)
        for attrib in dic.keys().tolist():
            result.add(name = attrib, value = dic[attrib])
        return result
                
            