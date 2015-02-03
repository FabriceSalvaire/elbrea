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

# from .ShaderProgrames import shader_manager
from .Painter import Painter
from Elbrea.Tools.TimeStamp import TimeStamp, ObjectWithTimeStamp
from Elbrea.Image.Image import ImageFormat

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class BackgroundPainter(Painter):

    _logger = _module_logger.getChild('BackgroundPainter')

    ##############################################
    
    def __init__(self, painter_manager):

        super(BackgroundPainter, self).__init__(painter_manager)

        self._texture_painters = {}
        self._current_painter = None

    ##############################################

    @property
    def current_painter_name(self):
        return self._current_painter

    @property
    def current_painter(self):
        return self._texture_painters[self._current_painter]

    ##############################################

    def add_painter(self, name):

        painter = TexturePainter(self._painter_manager, name)
        painter.disable()
        self._texture_painters[name] = painter
        return painter
        
    ##############################################

    def select_painter(self, name):

        if name in self._texture_painters:
            self._current_painter = name
            painter = self._texture_painters[name]
            painter.enable()
            # return painter
        else:
            raise KeyError(name)

    ##############################################

    def paint(self):

        if self._current_painter is not None:
            self._logger.info("current painter {}".format(self._current_painter))
            self._texture_painters[self._current_painter].paint()

####################################################################################################

class TexturePainter(Painter, ObjectWithTimeStamp):

    _logger = _module_logger.getChild('TexturePainter')

    ##############################################
    
    def __init__(self, painter_manager, name):

        ObjectWithTimeStamp.__init__(self)
        Painter.__init__(self, painter_manager)

        self._name = name

        self._glwidget = self._painter_manager.glwidget
        self._source = None
        # self._shader_program = shader_manager.texture_shader_program
        self._shader_program = None
        self._texture_vertex_array = None
        self._uploaded = False
        # self.modified()

    ##############################################

    @property
    def name(self):
        # return self.__painter_name__
        return self._name

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

            self._logger.info("uploaded {}".format(self._uploaded))

            # if self.source > self: # timestamp
            print(self._uploaded, self.source._modified_time, self._modified_time)
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
