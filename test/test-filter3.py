####################################################################################################

import Elbrea.Logging.Logging as Logging

logger = Logging.setup_logging('elbrea')

####################################################################################################

import numpy as np

####################################################################################################

from Elbrea.ImageProcessing.Filtering.IO.ImageLoader import ImageLoaderFilter
from Elbrea.ImageProcessing.Filtering.DataTypeConverter import NormalisedFloatFilter
from Elbrea.ImageProcessing.Filtering.Colour import HlsFilter

####################################################################################################

image_path = 'image-samples/front.jpg'

input_filter = ImageLoaderFilter(image_path)
float_filter = NormalisedFloatFilter()
hls_filter = HlsFilter()

float_filter.connect_input('input', input_filter.get_primary_output())
hls_filter.connect_input('input', float_filter.get_primary_output())

hls_filter.update()

print(input_filter.get_primary_output().image[0,0])
print(hls_filter.get_primary_output().image[0,0])

####################################################################################################
# 
# End
# 
####################################################################################################
