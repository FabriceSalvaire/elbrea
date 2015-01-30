####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2015 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from Elbrea.ImageProcessing.Filtering.IO.ImageLoader import ImageLoaderFilter
from Elbrea.ImageProcessing.Filtering.DataTypeConverter import NormalisedFloatFilter
from Elbrea.ImageProcessing.Filtering.Colour import HlsFilter

####################################################################################################

class ImageProcessingPipeline(object):

    ##############################################

    def __init__(self, image_path):

        self.input_filter = ImageLoaderFilter(image_path)
        self.float_filter = NormalisedFloatFilter()
        self.hls_filter = HlsFilter()

        self.float_filter.connect_input('input', self.input_filter.get_primary_output())
        self.hls_filter.connect_input('input', self.float_filter.get_primary_output())
        self.hls_filter.update()

####################################################################################################
# 
# End
# 
####################################################################################################
