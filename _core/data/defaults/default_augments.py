import tensorflow as _tf
import tensorflow.image as _tfi
from tensorflow.contrib.image import rotate as _rotate
import cv2 as _cv2
import collections as _collections
import numpy as _np
from ...Augments import Augments as _Augments


def crop(im, XMin, XMax, YMin, YMax):
    im_height, im_width = [int(x) for x in im.shape[:2]]

    offset_height = int(YMin * im_height)
    offset_width  = int(XMin * im_width)
    target_height = int((YMax - YMin) * im_height)
    target_width  = int((XMax - XMin) * im_width)
    
    return _tfi.crop_to_bounding_box(im, offset_height, offset_width, target_height, target_width)


def rotation(im):
    ANGLE = _tf.random.uniform([], -0.3, 0.3)
    return _rotate(im, ANGLE)


def homography(im):
    dim2D = im.shape.as_list()[:2]
    
    middleYaxis = [dim2D[0]/4, dim2D[0]*3/4]
    middleXaxis = [dim2D[1]/4, dim2D[1]*3/4]
    
    middleRectangle = [(int(i), int(j)) for i in middleXaxis for j in middleYaxis]
    
    Yvariability = int(dim2D[0] * 0.1)
    Xvariability = int(dim2D[1] * 0.1)

    randomRectangle = [(x + _tf.random.uniform([], -Xvariability, Xvariability),
                        y + _tf.random.uniform([], -Yvariability, Yvariability)) 
                       for x, y in middleRectangle]
   
    M, _ = _cv2.findHomography(_np.float32(middleRectangle), _np.float32(randomRectangle))
    
    shape = im.shape.as_list()[:2]
    shape = tuple(shape.__reversed__())
    return _tf.constant(_cv2.warpPerspective(_np.array(im), M, shape))

def noise(im):
    return _tf.add(
        im.numpy(),
        _tf.cast(
            _tf.random_normal(
                im.shape,
                mean = 0.0,
                stddev = 0.05,
                dtype = _tf.float32) * 255,
            dtype = _tf.uint8
        )
    )

def flip_ud(im):
    return _tfi.flip_up_down(im)

def flip_lr(im):
    return _tfi.flip_left_right(im)
     
    
def hue(im):
    DELTA_HUE = _tf.random.uniform([], 0, 0.1)
    return _tfi.adjust_hue(im, DELTA_HUE)


def saturation(im):
    SATURATION_FACTOR = _tf.random.uniform([], 0.5, 1)
    return _tfi.adjust_saturation(im, SATURATION_FACTOR)


def brightness(im):
    DELTA_BRIGHTNESS = _tf.random.uniform([], -0.2, 0.2)
    return _tfi.adjust_brightness(im, DELTA_BRIGHTNESS)


def contrast(im):
    CONTRAST_FACTOR = _tf.random.uniform([], 0.7, 1.3)
    return _tfi.adjust_contrast(im, CONTRAST_FACTOR)


def blur(im):
    GAUSS_BLUR_FILTER = (3, 3)
    return _tf.constant(_cv2.blur(_np.array(im), GAUSS_BLUR_FILTER))


default_augments_list = [crop, rotation, homography, noise, flip_ud, flip_lr, hue,
                         saturation, brightness, contrast, blur]

default_augments = _Augments()
default_augments.add(default_augments_list)