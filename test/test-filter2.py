####################################################################################################

import Elbrea.Logging.Logging as Logging

logger = Logging.setup_logging('elbrea')

####################################################################################################

import numpy as np

####################################################################################################

from Elbrea.Image import ImageLoader
from Elbrea.Image.Image import Image, ImageFormat
from Elbrea.ImagePipeline.ImageFilter import ImageFilter

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

class FloatFilter(ImageFilter):

    __filter_name__ = 'Float Filter'
    __input_names__ = ('input',)
    __output_names__ = ('float_image',)

    ##############################################

    def generate_output_information(self):

       if self._inputs:
           input_ = self.get_primary_input()
           output = self.get_primary_output()
           image_format = input_.image_format.clone(data_type=np.float32, normalised=True)
           self._logger.info("Make output for {} with shape \n{}".format(output.name,
                                                                         str(image_format)))
           output.image = Image(image_format)

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.get_primary_input()
        output = self.get_primary_output()
        input_.image.to_normalised_float(output.image)

####################################################################################################

class HlsFilter(ImageFilter):

    __filter_name__ = 'HLS Filter'
    __input_names__ = ('input',)
    __output_names__ = ('hls_image',)

    ##############################################

    def generate_output_information(self):

       if self._inputs:
           input_ = self.get_primary_input()
           output = self.get_primary_output()
           image_format = input_.image_format.clone(data_type=np.float32, normalised=True,
                                                    channels=ImageFormat.HLS)
           self._logger.info("Make output for {} with shape \n{}".format(output.name,
                                                                         str(image_format)))
           output.image = Image(image_format)

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)

        input_ = self.get_primary_input()
        output = self.get_primary_output()
        input_.image.convert_colour(ImageFormat.HLS, output.image) # HLS is redundant here 

####################################################################################################

image_path = 'image-samples/front.jpg'

input_filter = ImageLoaderFilter(image_path)
float_filter = FloatFilter()
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
