####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

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

    cv_array = cv2.imread(path)
    # CV uses BGR format
    image = Image(cv_array, share=True, channels=ImageFormat.BGR)
    image = image.swap_channels(ImageFormat.RGB)

    # array = tifffile.imread(path)
    # image = Image(cv_array, share=True, channels=ImageFormat.RGB)

    return image

####################################################################################################
# 
# End
# 
####################################################################################################
