####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################


""" This modules provides tools to draw segments and rectangles primitives.

The aim of these classes has to be used by a Geometry Shader.
"""

####################################################################################################

from six.moves import xrange

####################################################################################################

import logging
import numpy as np

####################################################################################################

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Buffer import GlArrayBuffer
from PyOpenGLng.HighLevelApi.VertexArrayObject import GlVertexArrayObject

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class LineVertexArray(GlVertexArrayObject):

    """ Base class to draw segments primitives as lines. """

    _logger = _module_logger.getChild('LineVertexArray')
    
    ##############################################
    
    def __init__(self, path=None):

        super(LineVertexArray, self).__init__()

        self._number_of_objects = 0
        self._vertex_array_buffer = GlArrayBuffer()

        if path is not None:
            self.set(path)

    ##############################################
    
    def bind_to_shader(self, shader_program_interface_attribute):

        """ Bind the vertex array to the shader program interface attribute.
        """

        self.bind()
        shader_program_interface_attribute.bind_to_buffer(self._vertex_array_buffer)
        self.unbind()

    ##############################################
    
    def draw(self):

        """ Draw the vertex array as lines. """

        self.bind()
        GL.glDrawArrays(GL.GL_LINES, 0, self._number_of_objects)
        self.unbind()

    ##############################################
    
    def set(self, path):

        """ Set the vertex array from an iterable of segments. """

        self._number_of_objects = path.number_of_points # Right ?
        vertex = np.zeros((self._number_of_objects, 2), dtype=np.float32)
        vertex[...] = path.points
        vertex += .5
        self._vertex_array_buffer.set(vertex)

####################################################################################################

class LineStripVertexArray(LineVertexArray):

    """ Base class to draw segments primitives as line strips. """

    _logger = _module_logger.getChild('LineStripVertexArray')

    ##############################################
    
    def draw(self):

        """ Draw the vertex array as lines. """

        self.bind()
        GL.glDrawArrays(GL.GL_LINE_STRIP_ADJACENCY, 0, self._number_of_objects +2)
        self.unbind()

    ##############################################
    
    def set(self, path):

        """ Set the vertex array from an iterable of segments. """

        self._number_of_objects = path.number_of_points # Right ?
        vertex = np.zeros((self._number_of_objects + 2, 2), dtype=np.float32)
        vertex[1:-1] = path.points
        vertex[0] = vertex[1]
        vertex[-1] = vertex[-2]
        vertex += .5
        self._vertex_array_buffer.set(vertex)

####################################################################################################
#
# End
#
####################################################################################################
