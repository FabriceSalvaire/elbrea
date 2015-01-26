####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import numpy as np

from mamba import *

# import cv
import cv2

####################################################################################################

def mamba2cv(image_in, image_out):

    depth = image_in.getDepth()
    if  depth == 1:
        dtype = np.bool
    elif depth == 8:
        dtype = np.uint8
    elif depth == 32:
        dtype = np.uint32
    else:
        raise NotImplementedError

    width, height = image_in.getSize()
    data = image_in.extractRaw()
    array_1d = np.fromstring(data, dtype)
    array_2d = array_1d.reshape((height, width))
    image_out[...] = array_2d[...]

####################################################################################################

def cv2mamba(image_in, image_out):

    data = image_in.tostring()
    image_out.loadRaw(data)

####################################################################################################
# 
# End
# 
####################################################################################################
