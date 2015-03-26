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
from .PrimitiveVertexArray import LineVertexArray, LineStripVertexArray, DynamicLineStripVertexArray

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
        self._current_path.z_value = -1
        self._current_path.bind_to_shader(self._shader_program.interface.attributes.position)
        self._glwidget.doneCurrent()

    ##############################################

    def add_item(self, path):

        # Fixme: upload_path ?
        
        self._logger.debug('Add path {}'.format(path.id))
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        vao = self.__primitive_class__(path)
        # Fimme: add attributes
        vao.id = path.id
        vao.colour = path.colour
        vao.line_width = path.pencil_size
        vao.z_value = path.z_value
        vao.bind_to_shader(self._shader_program.interface.attributes.position)
        self._items[vao.id] = vao
        self._glwidget.doneCurrent()

    ##############################################

    def update_item(self, path):

        vao = self._items[path.id]
        vao.colour = path.colour
        vao.line_width = path.pencil_size
        
    ##############################################

    def remove_item(self, path):

        del self._items[path.id]
        
    ##############################################

    def paint(self):

        # GL.glEnable(GL.GL_BLEND)
        # # Blending: O = Sf*S + Df*D
        # # alpha: 0: complete transparency, 1: complete opacity
        # # Set (Sf, Df) for transparency: O = Sa*S + (1-Sa)*D 
        # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self._shader_program.bind()
        # self._shader_program.uniforms.antialias_diameter = 1
        for vao in self._items.values():
            self._paint_vao(vao)
        if self._current_path is not None:
            self._paint_vao(self._current_path)
            
        # GL.glDisable(GL.GL_BLEND)

    ##############################################

    def _paint_vao(self, vao):

        self._shader_program.uniforms.colour = vao.colour
        self._shader_program.uniforms.line_width = vao.line_width
        self._shader_program.uniforms.z_value = vao.z_value
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
    def _items(self,):
        return self._page_provider.page_data.segments
    
####################################################################################################

class PathPainter(PrimitivePainter):

    __painter_name__ = 'path'
    __primitive_class__ = LineStripVertexArray

    ##############################################
    
    def __init__(self, painter_manager, page_provider, **kwargs):

        super(PathPainter, self).__init__(painter_manager, page_provider, **kwargs)
        self._shader_program = self._glwidget.shader_manager.path_shader_program

        self._glwidget.makeCurrent()
        self._current_path = DynamicLineStripVertexArray(size=100, upscale_factor=3)
        self._current_path.bind_to_shader(self._shader_program.interface.attributes.position)
        self._current_path.colour = (1, 1, 1) # Fixme:
        self._current_path.line_width = 1
        self._current_path.z_value = 0
        # self._glwidget.doneCurrent()

    ##############################################

    def reset_current_path(self):

        self._current_path.reset()
        
    ##############################################

    def update_current_item(self, path):

        self._logger.debug('Update current path')

        # Fixme: move to glwidget
        self._glwidget.makeCurrent()

        current_path = self._current_path
        if not current_path.number_of_points:
            self._current_path.colour = path.colour
            self._current_path.line_width = path.pencil_size

        self._current_path.add_vertex(path.p1)
        
        # self._glwidget.doneCurrent()
        
    ##############################################

    @property
    def _items(self,):
        return self._page_provider.page_data.paths

####################################################################################################
#
# End
#
####################################################################################################
