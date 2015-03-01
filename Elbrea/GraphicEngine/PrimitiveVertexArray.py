####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2015 Fabrice Salvaire
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

class LineStripVertexArray(GlVertexArrayObject):

    """ Base class to draw segments primitives as lines. """

    _logger = _module_logger.getChild('LineStripVertexArray')
    
    ##############################################
    
    def __init__(self, path=None):

        super(LineStripVertexArray, self).__init__()

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
        GL.glDrawArrays(GL.GL_LINE_STRIP_ADJACENCY, 0, self._number_of_objects +2)
        self.unbind()

    ##############################################
    
    def set(self, path):

        """ Set the vertex array from an iterable of segments. """

        # points = [[10, 10],
        #           [100, 10], # 1
        #           [200, 200], # 2
        #           [200, 10],
        #           [300, 300],
        #           [100, 300],
        #       ]
        # dx = 2
        # dy = 10
        # for i in xrange(10):
        #     points.append([100 - dx, 300 - 2*i*dy])
        #     points.append([100 + dx, 300 - (2*i+1)*dy])

        points = []
        dx = 50
        dy = 10
        for i in xrange(5):
            points.append([10 + 2*i*dx,     100 + dy])
            points.append([10 + (2*i+1)*dx, 100 - dy])
        print(points)
            
        points = np.array(points)
        self._number_of_objects = points.shape[0]
        # self._number_of_objects = path.number_of_points # Right ?
        vertex = np.zeros((self._number_of_objects + 2, 2), dtype=np.float32)
        vertex[1:-1] = points
        # vertex = np.asarray(path.points, dtype=np.float32)
        # vertex[1:-1] = path.points
        vertex[0] = vertex[1]
        vertex[-1] = vertex[-2]
        vertex += .5
        # vertex = np.zeros((self._number_of_objects, 2), dtype=np.float32)
        # points = path.points
        # for i in range(self._number_of_objects):
        #     vertex[i] = points[i]
        self._vertex_array_buffer.set(vertex)

####################################################################################################
#
# End
#
####################################################################################################
