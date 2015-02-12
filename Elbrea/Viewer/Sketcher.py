# -*- coding: utf-8 -*-

####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

import cv2

####################################################################################################

from Elbrea.Image.Image import Image
from Elbrea.Tools.TimeStamp import ObjectWithTimeStamp

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SketcherState(object):

    ##############################################

    def __init__(self):

        self.pencil_size = 1
        self.pencil_colour = (255, 255, 255)
    
####################################################################################################

class Sketcher(ObjectWithTimeStamp):

    _logger = _module_logger.getChild('sketcher')
    
    ##############################################
    
    def __init__(self, image_format, sketcher_state):

        ObjectWithTimeStamp.__init__(self)

        self._image = Image(image_format)
        
        self._sketcher_state = sketcher_state
        
    ##############################################

    @property
    def image(self):
        return self._image
        
    ##############################################

    def to_cv_point(self, point):

        return (int(point[0]), int(point[1]))
        
    ##############################################

    def draw_line(self, point1, point2):

        cv2.line(self._image,
                 self.to_cv_point(point1), self.to_cv_point(point2),
                 self._sketcher_state.pencil_colour, self._sketcher_state.pencil_size, 16)
        # thickness, lineType, shift
        self.modified()

    ##############################################

    # def tabletEvent(self, event):

    #     pointer_type = event.pointerType()
    #     # QtGui.QTabletEvent.UnknownPointer
    #     # QtGui.QTabletEvent.Pen
    #     # QtGui.QTabletEvent.Eraser

    #     position = event.pos()
    #     pressure = event.pressure()
    #     x_tilt = event.xTilt()
    #     y_tilt = event.yTilt()

    #     event_type = event.type()
    #     # QtCore.QEvent.TabletPress
    #     # QtCore.QEvent.TabletRelease

    #     self._logger.info("type {} pointer {} pos {} pressure {} tilt {} {}".format(
    #         event_type,
    #         pointer_type,
    #         position,
    #         pressure, x_tilt, y_tilt))

    #     if event_type == QtCore.QEvent.TabletMove:
    #         position = self.window_to_gl_coordinate(event, round_to_integer=False)
    #         if self._previous_position is not None:
    #             sketcher = self._application.sketcher.current_face
    #             sketcher.draw_line(self._previous_position, position,
    #                                self.pencil_colour,
    #                                self.pencil_size)
    #             self.update()
    #         self._set_previous_position(position, self.event_position(event))

    #         event.accept()
    #     # event.ignore()
        
####################################################################################################

class FrontBackSketcher(object):

    _logger = _module_logger.getChild('FrontBackSketcher')

    ##############################################
    
    def __init__(self, image_format):

        self.state = SketcherState()
        self.front_sketcher = Sketcher(image_format, self.state)
        self.back_sketcher = Sketcher(image_format, self.state)
        self._is_front = True

    ##############################################

    def switch_face(self):

        self._is_front = not self._is_front

    ##############################################

    @property
    def current_face(self):

        if self._is_front:
            return self.front_sketcher
        else:
            return self.back_sketcher
    
####################################################################################################
#
# End
#
####################################################################################################
