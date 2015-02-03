####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from .Painter import PainterMetaClass
from .TexturePainter import BackgroundPainter

# Load Painters
from . import ForegroundPainter 

####################################################################################################

class PainterManager(object):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, glwidget, background_painter_class=BackgroundPainter):
        
        super(PainterManager, self).__init__()

        self.glwidget = glwidget

        # Fixme: register self
        self.glwidget._painter_manager = self

        self._background_painter = background_painter_class(self)
        self._create_registered_painters()

    ##############################################

    def _create_registered_painters(self):

        self._foreground_painters = {} # enabled/disabled ?
        for painter_name, cls in PainterMetaClass.classes.items():
            self._logger.debug("Add Foreground painter %s", painter_name)
            if painter_name not in self._foreground_painters:
                self._foreground_painters[painter_name] = cls(self)
            else:
                raise NameError("Painter %s already registered" % (painter_name))

    ##############################################

    @property
    def background_painter(self):
        return self._background_painter

    ##############################################

    def foreground_painter(self, name):

        return self._foreground_painters[name]

    ##############################################

    def painter_iterator(self):

        return iter([self._background_painter] + list(self._foreground_painters.values()))

    ##############################################

    def enabled_painter_iterator(self):

        return iter([painter for painter in self.painter_iterator() if painter._status])

    ##############################################

    def paint(self):

        self._logger.info("")
        for painter in self.enabled_painter_iterator():
            painter.paint()

####################################################################################################
#
# End
#
####################################################################################################
