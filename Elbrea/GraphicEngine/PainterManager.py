####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from .Painter import PainterMetaClass, ForegroundPainter
from .PainterTexture import BackgroundPainter

####################################################################################################

class PainterManager(object):

    """

    Public Attributes:

      :attr:`opengl_viewer`

      :attr:`slide`

    """

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, gl_viewer):
        
        super(PainterManager, self).__init__()

        self.gl_viewer = gl_viewer

        # Fixme: register self
        self.gl_viewer._painter_manager = self

        self._background_painter = BackgroundPainter(self)
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

        return iter([self._background_painter] + self._foreground_painters.values())

    ##############################################

    def enabled_painter_iterator(self):

        return iter([painter for painter in self.painter_iterator() if painter.status])

    ##############################################

    def paint(self):

        for painter in self.enabled_painter_iterator():
            painter.paint()

####################################################################################################
#
# End
#
####################################################################################################
