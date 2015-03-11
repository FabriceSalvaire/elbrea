####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicItem(object):

    ##############################################

    def __init__(self, position):

        self._position = position
        self._scale = 1 # (x, y)
        self._rotation = 0

        self._interval = None
        
    ##############################################

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
    
    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
    
    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    @property
    def interval(self):
        return self._interval

    ##############################################

    def distance(self, point):
        raise NotImplementedError
    
####################################################################################################
#
# End
#
####################################################################################################
