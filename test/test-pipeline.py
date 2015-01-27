####################################################################################################

import Elbrea.Logging.Logging as Logging

logger = Logging.setup_logging('elbrea')

####################################################################################################

from Elbrea.Image.ImageLoader import load_image
# from Elbrea.Image.Image import Image, ImageFormat
import Elbrea.ImagePipeline
from Elbrea.ImagePipeline.ImagePipelineManager import ImagePipelineManager

####################################################################################################

class RawData(object):
    def __init__(self, path):
        self.image = load_image(path)

####################################################################################################

raw_data = RawData('image-samples/front.jpg')

image_pipeline_manager = ImagePipelineManager(raw_data=raw_data, shader_program=None)

####################################################################################################
# 
# End
# 
####################################################################################################
