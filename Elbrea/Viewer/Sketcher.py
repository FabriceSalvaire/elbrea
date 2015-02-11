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

class Sketcher(ObjectWithTimeStamp):

    _logger = _module_logger.getChild('sketcher')
    
    ##############################################
    
    def __init__(self, image_format):

        ObjectWithTimeStamp.__init__(self)

        self._image = Image(image_format)

    ##############################################

    @property
    def image(self):
        return self._image
        
    ##############################################

    def to_cv_point(self, point):

        return (int(point[0]), int(point[1]))
        
    ##############################################

    def draw_line(self, point1, point2, colour, thickness):

        cv2.line(self._image,
                 self.to_cv_point(point1), self.to_cv_point(point2),
                 colour, thickness, 16)
        # thickness, lineType, shift
        self.modified()

####################################################################################################

class FrontBackSketcher(object):

    _logger = _module_logger.getChild('FrontBackSketcher')

    ##############################################
    
    def __init__(self, image_format):

        self.front_sketcher = Sketcher(image_format)
        self.back_sketcher = Sketcher(image_format)
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
