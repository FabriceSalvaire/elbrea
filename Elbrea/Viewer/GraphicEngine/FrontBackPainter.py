####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

# Fixme: place ?

####################################################################################################

import logging

####################################################################################################

from .Painter import Painter
from .PainterManager import PainterManager
from .TexturePainter import BackgroundPainter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FrontBackPainter(Painter):

    _logger = _module_logger.getChild('FrontBackPainter')

    ##############################################
    
    def __init__(self, painter_manager, name, painter_class):

        self.__painter_name__ = name
       
        super(FrontBackPainter, self).__init__(painter_manager)

        self.front_painter = painter_class(painter_manager)
        self.back_painter = painter_class(painter_manager)
        self._is_front = True

    ##############################################

    def switch_face(self):

        self._is_front = not self._is_front

    ##############################################

    @property
    def current_painter(self):

        # current_side ?
        
        if self._is_front:
            return self.front_painter
        else:
            return self.back_painter

    ##############################################

    def paint(self):

        self.current_painter.paint()

####################################################################################################

class FrontBackPainterManager(PainterManager):

    _logger = logging.getLogger(__name__)

    ##############################################

    def create_background_painter(self):

        self._background_painter = FrontBackPainter(self, 'background', BackgroundPainter)

    ##############################################

    def switch_face(self):

        self._background_painter.switch_face()
        # register FrontBackPainter ?
        for painter in self._foreground_painters.values():
            if isinstance(painter, FrontBackPainter):
                painter.switch_face()
        self.glwidget.update()
        
####################################################################################################
#
# End
#
####################################################################################################
