####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

import numpy as np

####################################################################################################

from Elbrea.Image.Image import ImageFormat
from Elbrea.ImageProcessing.Core.ImageFilter import ImageFilter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class HlsFilter(ImageFilter):

    __filter_name__ = 'HLS Filter'
    __input_names__ = ('input',)
    __output_names__ = ('hls_image',)

    _logger = _module_logger.getChild('HlsFilter')

    ##############################################

    def generate_image_format(self, output):

        image_format = self.get_primary_input().image_format
        return image_format.clone(data_type=np.float32, normalised=True,
                                  channels=ImageFormat.HLS)

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.get_primary_input()
        output = self.get_primary_output()
        input_.image.convert_colour(ImageFormat.HLS, output.image) # HLS is redundant here 

####################################################################################################
# 
# End
# 
####################################################################################################
