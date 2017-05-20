####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

import numpy as np

import PIL.Image as PIL_Image

try:
    import cv2
except:
    cv2 = None

try:
    import tifffile
except:
    tifffile = None

####################################################################################################

from .Image import ImageFormat, Image

####################################################################################################

def load_image(path):

    if cv2 is not None:
        cv_array = cv2.imread(path)
        # CV uses BGR format
        image = Image(cv_array, share=True, channels=ImageFormat.BGR)
        image = image.swap_channels(ImageFormat.RGB)
    else:
        array = np.array(PIL_Image.open(path))
        image = Image(array, channels=ImageFormat.RGB)

    # array = tifffile.imread(path)
    # image = Image(cv_array, share=True, channels=ImageFormat.RGB)

    return image

####################################################################################################
# 
# End
# 
####################################################################################################
