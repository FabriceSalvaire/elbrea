####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2015 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging

from importlib import reload

####################################################################################################

from Elbrea.ImageProcessing.Filtering.IO.ImageLoader import ImageLoaderFilter
from Elbrea.ImageProcessing.Filtering.DataTypeConverter import NormalisedFloatFilter
from Elbrea.ImageProcessing.Filtering.Colour import HlsFilter

from Elbrea.ImageProcessing.Core.ImageFilter import ImageFilter

from . import UserFilterFunctions

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class UserFilter(ImageFilter):

    __filter_name__ = 'User Filter'
    __input_names__ = ('input',)
    __output_names__ = ('user_image',)

    _logger = _module_logger.getChild('UserFilter')

    ##############################################

    def generate_image_format(self, output):

        image_format = self.get_primary_input().image_format
        return image_format.clone()

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.get_primary_input()
        output = self.get_primary_output()

        reload(UserFilterFunctions)
        UserFilterFunctions.user_filter(input_.image, output.image)

####################################################################################################

class ImageProcessingPipeline(object):

    ##############################################

    def __init__(self, image_path):

        self.input_filter = ImageLoaderFilter(image_path)
        self.float_filter = NormalisedFloatFilter()
        self.hls_filter = HlsFilter()
        self.user_filter = UserFilter()

        self.float_filter.connect_input('input', self.input_filter.get_primary_output())
        self.hls_filter.connect_input('input', self.float_filter.get_primary_output())
        # self.hls_filter.update()
        self.user_filter.connect_input('input', self.hls_filter.get_primary_output())
        self.user_filter.update()

####################################################################################################
# 
# End
# 
####################################################################################################
