####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from PyOpenGLng.HighLevelApi.Geometry import Point, Offset
from PyOpenGLng.HighLevelApi.TextureVertexArray import GlTextureVertexArray

####################################################################################################

from .Painter import Painter
from .ShaderProgrames import shader_manager
from Elbrea.Tools.TimeStamp import TimeStamp, ObjectWithTimeStamp

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class TexturePainter(Painter, ObjectWithTimeStamp):

    _logger = _module_logger.getChild('TexturePainter')

    ##############################################
    
    def __init__(self, gl_widget):

        ObjectWithTimeStamp.__init__(self)
        Painter.__init__(self)

        self._gl_widget = gl_widget # ?

        self._source = None
        self._shader_program = shader_manager.roi_shader_program
        self._texture_vertex_array = None
        self._shader_program = None
        # self.modified()

    ##############################################

    @property
    def shader_program(self):
        return self._shader_program
    
    @shader_program.setter
    def shader_program(self, shader_program):

        self._shader_program = shader_program
        self._texture_vertex_array.bind_to_shader(self._shader_program.interface.attributes)

    ##############################################

    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, source):
        # connect_source
        self._source = source

    ##############################################

    def _create_texture(self, image_format):

        dimension = Offset(image_format.width, image_format.height)
        self._texture_vertex_array = GlTextureVertexArray(position=Point(0, 0), dimension=dimension)

    ##############################################

    def upload_data(self):

        # should check image_format
        self._texture_vertex_array.set(self._source.image)
        self.modified()

    ##############################################

    def paint(self):

        if (self._status
            and self._texture_vertex_array is not None
            and self._shader_program is not None):
            if self.source > self: # timestamp
                self.upload_data()
            shader_program = self._shader_program
            shader_program.bind()
            self._texture_vertex_array.draw()
            shader_program.unbind()

####################################################################################################
#
# End
#
####################################################################################################
