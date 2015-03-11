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

from .Painter import Painter
from .PrimitiveVertexArray import LineStripVertexArray

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PathPainter(Painter):

    __painter_name__ = 'path'

    _logger = _module_logger.getChild('PathPainter')

    ##############################################
    
    def __init__(self, painter_manager):

        super(PathPainter, self).__init__(painter_manager)

        self._glwidget = self._painter_manager.glwidget
        self._shader_program = self._glwidget.shader_manager.wide_line_shader_program
        self.reset()

    ##############################################

    def reset(self):

        self._current_path = None
        self._paths = {} # Fixme: must be extern for pages
        self.disable()

    ##############################################

    def reset_current_path(self):

        self._current_path = None
        
    ##############################################

    def update_current_path(self, path):

        self._logger.debug('Update current path')
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        self._current_path = LineStripVertexArray(path)
        self._current_path.colour = path.colour
        self._current_path.line_width = path.pencil_size
        self._current_path.bind_to_shader(self._shader_program.interface.attributes.position)
        self._glwidget.doneCurrent()

    ##############################################

    def add_path(self, path):

        self._logger.debug('Add path {}'.format(path.id))
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        path_vao = LineStripVertexArray(path)
        path_vao.id = path.id
        path_vao.colour = path.colour
        path_vao.line_width = path.pencil_size
        path_vao.bind_to_shader(self._shader_program.interface.attributes.position)
        self._paths[path_vao.id] = path_vao
        self._glwidget.doneCurrent()

    ##############################################

    def remove_path(self, path):

        del self._paths[path.id]
    
    ##############################################

    def paint(self):

        GL.glEnable(GL.GL_BLEND)
        # Blending: O = Sf*S + Df*D
        # alpha: 0: complete transparency, 1: complete opacity
        # Set (Sf, Df) for transparency: O = Sa*S + (1-Sa)*D 
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self._shader_program.bind()
        self._shader_program.uniforms.antialias_diameter = 1.
        for vao in self._paths.values():
            self._paint_vao(vao)
        if self._current_path is not None:
            self._paint_vao(self._current_path)
            
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
