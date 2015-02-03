####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from Elbrea.GraphicEngine.TexturePainter import BackgroundPainter, Painter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FrontBackPainter(Painter):

    _logger = _module_logger.getChild('FrontBackPainter')

    ##############################################
    
    def __init__(self, painter_manager):

        super(FrontBackPainter, self).__init__(painter_manager)

        self.front_painter = BackgroundPainter(painter_manager)
        self.back_painter = BackgroundPainter(painter_manager)
        self._is_front = True

    ##############################################

    def switch(self):
        self._is_front = not self._is_front

    ##############################################

    @property
    def current_painter(self):

        if self._is_front:
            return self.front_painter
        else:
            return self.back_painter

    ##############################################

    def paint(self):

        self.current_painter.paint()

####################################################################################################
#
# End
#
####################################################################################################
