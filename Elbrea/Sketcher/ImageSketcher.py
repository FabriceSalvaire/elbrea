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

class ImageSketcher(ObjectWithTimeStamp):

    _logger = _module_logger.getChild('ImageSketcher')
    
    ##############################################
    
    def __init__(self, image_format, sketcher_state, painter):

        ObjectWithTimeStamp.__init__(self)

        self._image = Image(image_format)
        self._image.clear()
        
    ##############################################

    @property
    def image(self):
        return self._image
    
    ##############################################

    def to_cv_point(self, point):

        return (int(point[0]), int(point[1]))
        
    ##############################################

    def draw_line(self, point1, point2, colour=None, pencil_size=None):

        if colour is None:
            colour = self._sketcher_state.pencil_colour
        if pencil_size is None:
            pencil_size = self._sketcher_state.pencil_size
        
        cv2.line(self._image, self.to_cv_point(point1), self.to_cv_point(point2),
                 colour, pencil_size, 16)
        self.modified()
    
####################################################################################################
#
# End
#
####################################################################################################
