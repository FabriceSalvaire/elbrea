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
from PyOpenGLng.HighLevelApi.TextureVertexArray import GlTextureVertexArray
from PyOpenGLng.Math.Geometry import Point, Offset

####################################################################################################

# from .ShaderProgrames import shader_manager
from .Painter import Painter
from Elbrea.Tools.TimeStamp import ObjectWithTimeStamp
from Elbrea.Image.Image import ImageFormat

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class TexturePainter(Painter):

    __painter_name__ = 'texture'

    _logger = _module_logger.getChild('TexturePainter')

    ##############################################

    def __init__(self, *args, **kwargs):

        super(TexturePainter, self).__init__(*args, **kwargs)

        self._shader_program = self._glwidget.shader_manager.texture_shader_program
        self._texture_vertex_array = None

    ##############################################

    def upload(self, position, dimension, image):

        self._glwidget.makeCurrent() #?
        with GL.error_checker():
            self._texture_vertex_array = GlTextureVertexArray(position, dimension, image)
            shader_program_interface = self._shader_program.interface.attributes
            self._texture_vertex_array.bind_to_shader(shader_program_interface)

    ##############################################

    def paint_texture(self, texture_vertex_array):

        # Fixme: efficiency, design
        shader_program = self._shader_program
        shader_program.bind()
        texture_vertex_array.draw()
        shader_program.unbind()

    ##############################################

    def paint(self):

        # Fixme: status, done in manager ?
        if (self._status and self._texture_vertex_array is not None):
            self.paint_texture(self._texture_vertex_array)

####################################################################################################

class DynamicTexturePainter(Painter, ObjectWithTimeStamp):

    _logger = _module_logger.getChild('DynamicTexturePainter')

    ##############################################

    def __init__(self, *args, **kwargs):

        ObjectWithTimeStamp.__init__(self)
        Painter.__init__(self, *args, **kwargs)

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
            integer_internal_format = image_format.channels == ImageFormat.Label
            self._texture_vertex_array = GlTextureVertexArray(position=Point(0, 0), dimension=dimension,
                                                              integer_internal_format=integer_internal_format)
            # image=self._source.image
            shader_program_interface = self._shader_program.interface.attributes
            self._texture_vertex_array.bind_to_shader(shader_program_interface)
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

            # self._logger.info("uploaded {}".format(self._uploaded))
            
            # if self.source > self: # timestamp
            # print(self._uploaded, self.source._modified_time, self._modified_time)
            if not self._uploaded or self.source._modified_time > self._modified_time:
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
