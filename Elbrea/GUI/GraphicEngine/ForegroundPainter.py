####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from PyOpenGLng.HighLevelApi.Geometry import Point, Segment
from PyOpenGLng.HighLevelApi.PrimitiveVertexArray import GlSegmentVertexArray

from .ShaderProgrames import shader_manager

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class RoiPainter(object):

    _logger = _module_logger.getChild('RoiPainter')

    ##############################################
    
    def __init__(self, glwidget):

        self._glwidget = glwidget
        self._shader_program = shader_manager.roi_shader_program
        self.reset()

    ##############################################

    @property
    def paint_box(self):
        return self._paint_box

    @paint_box.setter
    def paint_box(self, paint_box):
        self._paint_box = paint_box

    @property
    def paint_grips(self):
        return self._paint_grips

    @paint_grips.setter
    def paint_grips(self, paint_grips):
        self._paint_grips = paint_grips

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, margin):
        self._margin = margin

    ##############################################

    def reset(self):

        self._logger.debug('Reset ROI Box Painter')
        self._bounding_box = None
        self._segment_vertex_array = None
        self._margin = 0
        self.disable()

    ##############################################

    def disable(self):

        self._logger.debug('Disable ROI Box Painting')
        # super(RoiPainter, self).disable()
        self._paint_box = False
        self._paint_grips = False

    ##############################################

    def enable(self, paint_grips=False):

        self._logger.debug('Enable ROI Box Painting')
        self._paint_box = True
        self._paint_grips = paint_grips
        # super(RoiPainter, self).enable()

    ##############################################

    def update_bounding_box(self, interval):

        self._logger.debug('Update ROI Box')
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        if interval is not None:
            segments = []
            x_min, y_min, x_max, y_max = interval.bounding_box()
            segment = Segment(Point(x_min, y_min), Point(x_max, y_max))
            segments.append(segment)
            self._segment_vertex_array = GlSegmentVertexArray(segments)
            self._segment_vertex_array.bind_to_shader(self._shader_program.interface.attributes.position)
        self._glwidget.doneCurrent()

    ##############################################

    def paint(self):

        if self._paint_box and self._segment_vertex_array is not None:
            self._logger.debug('Paint ROI Box')
            self._shader_program.bind()
            #!# self._shader_program.uniforms.colour = (1., 1., 1.)
            self._shader_program.uniforms.margin = self._margin
            #!# Fixme: self._shader_program.uniforms.paint_grips = self._paint_grips # Fixme: always on, check Cropper
            self._segment_vertex_array.draw()

####################################################################################################
#
# End
#
####################################################################################################
