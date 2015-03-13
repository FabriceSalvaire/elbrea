####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

import numpy as np

####################################################################################################

from PyOpenGLng.HighLevelApi import GL

from .Path import Segment 
from Elbrea.GraphicEngine.Painter import Painter
from Elbrea.GraphicEngine.PrimitiveVertexArray import LineVertexArray
from Elbrea.Image.Colour import RgbIntColour

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PagePainter(Painter):

    __painter_name__ = 'page'

    _logger = _module_logger.getChild('PagePainter')

    ##############################################
    
    def __init__(self, painter_manager, step=10):

        super(PagePainter, self).__init__(painter_manager)

        self._glwidget = self._painter_manager.glwidget
        self._shader_program = self._glwidget.shader_manager.segment_shader_program
        self.reset()

        self.set_page(step)
        
    ##############################################


    def set_page(self, step=10):

        self._glwidget.makeCurrent()

        interval =  self._glwidget._image_interval
        colour = RgbIntColour(64, 160, 255).normalise() # xournal
        pencil_size = 1. # > 1
        for y in range(interval.y.inf, interval.y.sup, step):
            points = np.array(((interval.x.inf, y),
                               (interval.x.sup, y)),
                              dtype=np.uint16)
            path = Segment(colour, pencil_size, points=points)
            self.add_path(path)
        for x in range(interval.x.inf, interval.x.sup, step):
            points = np.array(((x, interval.y.inf),
                               (x, interval.y.sup)),
                              dtype=np.uint16)
            path = Segment(colour, pencil_size, points=points)
            self.add_path(path)
            
        self._glwidget.doneCurrent()

    ##############################################

    def add_path(self, path):

        path_vao = LineVertexArray(path)
        path_vao.id = path.id
        path_vao.colour = path.colour
        path_vao.line_width = path.pencil_size
        path_vao.bind_to_shader(self._shader_program.interface.attributes.position)
        self._paths.append(path_vao)
        
    ##############################################

    def reset(self):

        self._paths = []
        self.disable()
    
    ##############################################

    def paint(self):

        GL.glEnable(GL.GL_BLEND)
        # Blending: O = Sf*S + Df*D
        # alpha: 0: complete transparency, 1: complete opacity
        # Set (Sf, Df) for transparency: O = Sa*S + (1-Sa)*D 
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self._shader_program.bind()
        self._shader_program.uniforms.antialias_diameter = 1.
        for vao in self._paths:
            self._paint_vao(vao)
            
        GL.glDisable(GL.GL_BLEND)

    ##############################################

    def _paint_vao(self, vao):

        self._shader_program.uniforms.colour = vao.colour
        self._shader_program.uniforms.line_width = vao.line_width
        vao.draw()
               
####################################################################################################
#
# End
#
####################################################################################################
