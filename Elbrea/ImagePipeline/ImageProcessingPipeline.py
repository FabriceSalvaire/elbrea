####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

import numpy as np
import cv2

####################################################################################################

from Elbrea.Image.Image import ImageFormat
from .ImagePipeline import ImagePipeline, IntensityType

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class HlsImagePipeline(ImagePipeline):

    __pipeline_name__ = 'hls'
    __input_pipelines__ = ('raw',)

    _logger = _module_logger.getChild('HslImageProcessing')

    __intensity_type__ = IntensityType.raw # ?

    ##############################################

    def generate_output_image(self):

        input_image = self.get_input_image()
        output_image = input_image.convert_colour(ImageFormat.HLS)

        return output_image

####################################################################################################

# import UserImageProcessing

class UserImagePipeline(ImagePipeline):

    __pipeline_name__ = 'user'
    __input_pipelines__ = ('raw',)

    _logger = _module_logger.getChild('UserImageProcessing')

    __intensity_type__ = IntensityType.raw

    ##############################################

    def reload(self):

        self._logger.info('Reload UserImageProcessing')
        reload(UserImageProcessing)
        self.increment_generation_number()

    ##############################################

    def generate_output_image(self):

        import UserImageProcessing
        return UserImageProcessing.process_image(self.get_input_image())

####################################################################################################

class FooPipeline(ImagePipeline):

    __pipeline_name__ = 'foo'
    __input_pipelines__ = ('hls', 'user')

####################################################################################################
# 
# End
# 
####################################################################################################
