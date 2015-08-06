####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from Elbrea.Sketcher.Sketcher import SketcherState, Sketcher

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FrontBackSketcher(object):

    _logger = _module_logger.getChild('FrontBackSketcher')

    ##############################################

    def __init__(self, image_format, painter):

        self.state = SketcherState()
        self.front_sketcher = Sketcher(image_format, self.state, painter.front_painter)
        self.back_sketcher = Sketcher(image_format, self.state, painter.back_painter)
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

    ##############################################

    def on_tablet_event(self, tablet_event):

        return self.current_face.on_tablet_event(tablet_event)

####################################################################################################
#
# End
#
####################################################################################################
