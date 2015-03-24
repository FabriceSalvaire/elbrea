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
from .PrimitiveVertexArray import LineVertexArray, LineStripVertexArray

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PrimitivePainter(Painter):

    __primitive_class__ = None

    _logger = _module_logger.getChild('PrimitivePainter')
    
    ##############################################
    
    def __init__(self, painter_manager, page_provider, **kwargs):

        super(PrimitivePainter, self).__init__(painter_manager, **kwargs)

        self._page_provider = page_provider
        self._glwidget = self._painter_manager.glwidget
        # self._path_vaos = {}
        self.reset()

    ##############################################

    def reset(self):

        self._current_path = None
        # self.disable()

    ##############################################

    def reset_current_path(self):

        self._current_path = None
        
    ##############################################

    def update_current_item(self, path):

        self._logger.debug('Update current path')
        # Fixme: move to glwidget
        # Fixme: try to update vbo, allocate a larger buufer
        self._glwidget.makeCurrent()
        self._current_path = self.__primitive_class__(path)
        self._current_path.colour = path.colour
        self._current_path.line_width = path.pencil_size
        self._current_path.bind_to_shader(self._shader_program.interface.attributes.position)
        self._glwidget.doneCurrent()

    ##############################################

    def add_item(self, path):

        # Fixme: upload_path ?
        
        self._logger.debug('Add path {}'.format(path.id))
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        path_vao = self.__primitive_class__(path)
        path_vao.id = path.id
        path_vao.colour = path.colour
        path_vao.line_width = path.pencil_size
        path_vao.bind_to_shader(self._shader_program.interface.attributes.position)
        self._paths[path_vao.id] = path_vao
        # self._path_vaos[path_vao.id] = path_vao
        # self._paths.append(path_vao.id)
        self._glwidget.doneCurrent()

    ##############################################

    def remove_item(self, path):

        del self._paths[path.id]
        # del self._path_vaos[path_vao.id]
        # self._paths.remove(path_vao.id)
        
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
        # for vao_id in self._paths:
        #     vao = self._path_vaos[vao_id]
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

class SegmentPainter(PrimitivePainter):

    __painter_name__ = 'segment'
    __primitive_class__ = LineVertexArray

    ##############################################
    
    def __init__(self, painter_manager, page_provider, **kwargs):

        super(SegmentPainter, self).__init__(painter_manager, page_provider, **kwargs)
        self._shader_program = self._glwidget.shader_manager.segment_shader_program

    ##############################################

    @property
    def _paths(self,):
        return self._page_provider.page_data.segments

####################################################################################################

class PathPainter(PrimitivePainter):

    __painter_name__ = 'path'
    __primitive_class__ = LineStripVertexArray

    ##############################################
    
    def __init__(self, painter_manager, page_provider, **kwargs):

        super(PathPainter, self).__init__(painter_manager, page_provider, **kwargs)
        self._shader_program = self._glwidget.shader_manager.path_shader_program

    ##############################################

    @property
    def _paths(self,):
        return self._page_provider.page_data.paths

####################################################################################################
#
# End
#
####################################################################################################
