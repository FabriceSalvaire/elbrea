####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

# Fixme: should check dirty

####################################################################################################

import logging

####################################################################################################

from .DependencyGraph import DependencyGraphNode
from Elbrea.Image.Image import Image
from Elbrea.Tools.EnumFactory import EnumFactory

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

# purpose ? vs image_format, label ?
IntensityType = EnumFactory('IntensityType', ('raw', 'full_scale'))

####################################################################################################

class ImagePipelineBase(DependencyGraphNode):

    # Number of bits to compute key
    #  2**16 = 65536
    PIPELINE_NUMBER_OF_BITS = 16

    __pipeline_name__ = None
    __input_pipelines__ = ()
    __ouput_pipelines__ = []
    __intensity_type__ = None
    __intensity_default_range__ = None
    _last_pipeline_id = 0
    _generation_number_max = 2**32 -1

    _logger = _module_logger.getChild('ImagePipelineBase')

    ##############################################

    @staticmethod
    def _new_pipeline_id():

        ImagePipeline._last_pipeline_id += 1

        return ImagePipeline._last_pipeline_id

    ##############################################

    def __init__(self,
                 image_format=None,
                 shader_program=None,
                 ):

        super(ImagePipelineBase, self).__init__()

        self._image_format = image_format
        self._shader_program = shader_program

        self._pipeline_id = self._new_pipeline_id()
        self._generation_number = 0

    ##############################################

    def __repr__(self):

        return self.__pipeline_name__

    ##############################################

    # def __hash__(self):
    #     return self._pipeline_id

    ##############################################

    @property
    def name(self):
        return self.__pipeline_name__

    @property
    def intensity_default_range(self):
        return self.__intensity_default_range__

    @property
    def pipeline_id(self):
        return self._pipeline_id

    @property
    def generation_number(self):
        return self._generation_number

    @property
    def image_format(self):
        return self._image_format

    @property
    def shader_program(self):
        return self._shader_program

    @shader_program.setter
    def shader_program(self, shader_program):
        self._shader_program = shader_program

    ##############################################

    def increment_generation_number(self):

        # self._logger.debug('Increment Generation Number for {}'.format(self.name))

        if self._generation_number < self._generation_number_max:
            self._generation_number += 1
        else:
            raise RuntimeError('Generation Number Overflow')

    ##############################################

    def make_empty_output_image(self):

        return Image(self._image_format)

    ##############################################

    def generate_output_image(self):

        return self.make_empty_output_image()

####################################################################################################

class RawImagePipeline(ImagePipelineBase):

    __pipeline_name__ = 'raw'
    __intensity_type__ = IntensityType.raw

    _logger = _module_logger.getChild('RawImagePipeline')

    ##############################################

    def __init__(self, raw_data, shader_program=None):

        image_format = raw_data.image.image_format
        super(RawImagePipeline, self).__init__(image_format, shader_program)
        self._raw_data = raw_data

        self.increment_generation_number()

    ##############################################

    def generate_output_image(self):

        return self._raw_data.image

####################################################################################################

class ImagePipelineMetaClass(type):

    classes = {}

    _logger = _module_logger.getChild('ImagePipelineMetaClass')

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        type.__init__(cls, class_name, super_classes, class_attribute_dict)
        if class_name != 'ImagePipeline':
            ImagePipelineMetaClass._logger.info("Register image pipeline {}".format(cls.__pipeline_name__))
            ImagePipelineMetaClass.classes[cls.__pipeline_name__] = cls

####################################################################################################

class ImagePipeline(ImagePipelineBase, metaclass = ImagePipelineMetaClass):

    _logger = _module_logger.getChild('ImagePipeline')

    ##############################################

    def __init__(self, **kwargs):

        _kwargs = dict(kwargs)
        # for key in ('image_format', 'shader_program'):
        #     if key not in kwargs:
        #         # Fixme: bad use property
        #         _kwargs[key] = getattr(image_pipeline, '_' + key)

        super(ImagePipeline, self).__init__(**_kwargs)

    ##############################################

    def get_input_image(self):

        return self._image_pipeline.get_output_image()

####################################################################################################
# 
# End
# 
####################################################################################################
