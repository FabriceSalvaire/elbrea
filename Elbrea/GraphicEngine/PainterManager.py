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

####################################################################################################

class PainterManager(object):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, glwidget):
        
        super(PainterManager, self).__init__()

        self.glwidget = glwidget

        # Fixme: register self
        self.glwidget._painter_manager = self

        self._background_painter = None
        self.create_background_painter()
        
        self._create_registered_painters()

    ##############################################

    def create_background_painter(self):

        raise NotImplementedError

    ##############################################

    def register_foreground_painter(self, painter, painter_name=None):

        # Fixme: useful ?
        if painter_name is None:
            painter_name = painter.name
        
        if painter_name != 'background' and painter_name not in self._foreground_painters:
            self._foreground_painters[painter_name] = painter
        else:
            raise NameError("Painter %s already registered" % (painter_name))

    ##############################################

    def _create_registered_painters(self):

        self._foreground_painters = {} # enabled/disabled ?
        for painter_name, cls in PainterMetaClass.classes.items():
            self._logger.debug("Add Foreground painter %s", painter_name)
            painter = cls(self)
            self.register_foreground_painter(painter)

    ##############################################

    @property
    def background_painter(self):
        return self._background_painter

    ##############################################

    def foreground_painter(self, name):

        return self._foreground_painters[name]

    ##############################################

    def __getitem__(self, name):

        if name == 'background':
            return self._background_painter
        else:
            return self._foreground_painters[name]
    
    ##############################################

    def painter_iterator(self):

        return iter([self._background_painter] + list(self._foreground_painters.values()))

    ##############################################

    def enabled_painter_iterator(self):

        return iter([painter for painter in self.painter_iterator() if bool(painter)])

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
