####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Geometry import Point, Offset
from PyOpenGLng.HighLevelApi.TextureVertexArray import GlTextureVertexArray

####################################################################################################

from .Painter import Painter
# from .ShaderProgrames import shader_manager
from Elbrea.Tools.TimeStamp import TimeStamp, ObjectWithTimeStamp

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class TexturePainter(Painter, ObjectWithTimeStamp):

    _logger = _module_logger.getChild('TexturePainter')

    ##############################################
    
    def __init__(self, painter_manager):

        ObjectWithTimeStamp.__init__(self)
        Painter.__init__(self, painter_manager)

        self._glwidget = self._painter_manager.glwidget
        self._source = None
        # self._shader_program = shader_manager.texture_shader_program
        self._shader_program = None
        self._texture_vertex_array = None
        self._uploaded = False
        # self.modified()

    ##############################################

    @property
    def shader_program(self):
        return self._shader_program
    
    @shader_program.setter
    def shader_program(self, shader_program):
        self._shader_program = shader_program

    ##############################################

    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, source):
        # connect_source
        self._source = source
        self._create_texture(self._source.image_format)

    ##############################################

    def _create_texture(self, image_format):

        self._logger.info("")
        self._glwidget.makeCurrent() #?
        dimension = Offset(image_format.width, image_format.height)
        with GL.error_checker():
            self._texture_vertex_array = GlTextureVertexArray(position=Point(0, 0), dimension=dimension)
            # image=self._source.image
            self._texture_vertex_array.bind_to_shader(self._shader_program.interface.attributes)
        self._uploaded = False

    ##############################################

    def upload_data(self):

        # self._glwidget.makeCurrent()
        # self._glwidget.doneCurrent()

        self._logger.info("")
        # should check image_format
        self._texture_vertex_array.set(self._source.image)
        self._uploaded = True
        self.modified()

    ##############################################

    def paint(self):

        if (self._status
            and self._texture_vertex_array is not None
            and self._shader_program is not None):

            self._logger.info("")

            # if self.source > self: # timestamp
            if not self._uploaded:
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
