####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from .Painter import Painter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SwitchPainter(Painter):

    """ Painter acting as a switch between a list of painters. """

    _logger = _module_logger.getChild('SwitchPainter')

    ##############################################

    def __init__(self, *args, **kwargs):

        super(SwitchPainter, self).__init__(*args, **kwargs)

        self._painters = {}
        self._current_painter = None

    ##############################################

    @property
    def current_painter_name(self):
        return self._current_painter

    @property
    def current_painter(self):
        return self._painters[self._current_painter]

    ##############################################

    def add_painter(self, painter, name):

        # name != painter.name
        self._painters[name] = painter
        painter.disable()

    ##############################################

    def select_painter(self, name):

        if name in self._painters:
            self._current_painter = name
            painter = self._painters[name]
            painter.enable()
            # return painter
        else:
            raise KeyError(name)

    ##############################################

    def paint(self):

        if self._current_painter is not None:
            self._logger.info("current painter {}".format(self._current_painter))
            self._painters[self._current_painter].paint()

####################################################################################################
#
# End
#
####################################################################################################
