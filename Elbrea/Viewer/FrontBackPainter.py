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

from Elbrea.GraphicEngine.Painter import Painter
from Elbrea.GraphicEngine.PainterManager import BasicPainterManager
from Elbrea.GraphicEngine.SwitchPainter import SwitchPainter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FrontBackPainter(Painter):

    _logger = _module_logger.getChild('FrontBackPainter')

    ##############################################

    def __init__(self, painter_manager, name, painter_class):

        super(FrontBackPainter, self).__init__(painter_manager, name=name)

        self.front_painter = painter_class(painter_manager, name='Front')
        self.back_painter = painter_class(painter_manager, name='Back')
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

class FrontBackPainterManager(BasicPainterManager):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, glwidget):

        super(FrontBackPainterManager, self).__init__(glwidget)

        self._background_painter = FrontBackPainter(self, 'background', SwitchPainter)

    ##############################################

    @property
    def background_painter(self):
        return self._background_painter

    ##############################################

    def switch_face(self):

        for painter in self._painters.values():
            if isinstance(painter, FrontBackPainter):
                painter.switch_face()
        self.glwidget.update()

####################################################################################################
#
# End
#
####################################################################################################
