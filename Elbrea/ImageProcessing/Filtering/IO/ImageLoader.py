####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

from Elbrea.Image import ImageLoader
from Elbrea.ImageProcessing.Core.ImageFilter import ImageFilter

####################################################################################################

class ImageLoaderFilter(ImageFilter):

    __filter_name__ = 'Image Loader Filter'
    __input_names__ = ()
    __output_names__ = ('image',)

    ##############################################

    def __init__(self, path):

        super(ImageLoaderFilter, self).__init__()

        output = self.get_primary_output()
        output.image = ImageLoader.load_image(path)
        output._image_format = output.image.image_format

####################################################################################################
#
# End
#
####################################################################################################
