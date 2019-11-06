

#print(__file__)
#print(__path__)
from tensorflow import enable_eager_execution as _eee
_eee()

from ._core.data.Input_Data_Formatter import Input_Data_Formatter

from ._core.Augments import Augments
from ._core.scheme.Augment_Scheme import Augment_Scheme

from ._core.data.defaults.default_Aug_Or_Im_Batch import default_aug_original_im_batch

from ._core.Augmenter import Augmenter





#function based on an answer from: 
#https://stackoverflow.com/questions/36006136/how-to-display-images-in-a-row-with-ipython-display/47334314
def augs_display(augments, original_im_n, range_of_aug_ims, no_of_columns=3, figsize=(10,10)):
    i, f = range_of_aug_ims
    list_of_images = [augments.batches[original_im_n].batch[x].im for x in range(i,f)]
    list_of_titles = [augments.batches[original_im_n].batch[x].Id for x in range(i,f)]
    
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=figsize)
    column = 0
    for i in range(len(list_of_images)):
        column += 1
        #  check for end of column and create a new figure
        if column == no_of_columns+1:
            fig = plt.figure(figsize=figsize)
            column = 1
        fig.add_subplot(1, no_of_columns, column)
        plt.imshow(list_of_images[i])
        plt.axis('off')
        if len(list_of_titles) >= len(list_of_images):
            plt.title(list_of_titles[i])