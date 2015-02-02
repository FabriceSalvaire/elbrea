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

class PainterMetaClass(type):

    """ Metaclass to register all the subclasses. """

    classes = {}

    _logger = _module_logger.getChild('PainterMetaClass')

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        type.__init__(cls, class_name, super_classes, class_attribute_dict)
        if class_name != 'ForegroundPainter':
            # PainterMetaClass._logger.debug("Register foreground painter %s", cls.__painter_name__)
            PainterMetaClass.classes[cls.__painter_name__] = cls

####################################################################################################

class Painter(object):

    """

    Public Attributes:

      :attr:`painter_manager`

      :attr:`status`

    """

    __painter_name__ = None

    _logger = _module_logger.getChild('Painter')

    ##############################################
    
    def __init__(self, painter_manager):

        self._painter_manager = painter_manager

        self._status = True

    ##############################################

    def __nonzero__(self):
        return self._status

    ##############################################

    @property
    def name(self):
        return self.__painter_name__

    ##############################################

    def switch(self):
        self._status = not self._status

    ##############################################

    def disable(self):
        self._status = False

    ##############################################

    def enable(self):
        self._status = True

    ##############################################

    def paint(self):
        raise NotImplementedError

####################################################################################################

class ForegroundPainter(Painter, metaclass = PainterMetaClass):
    pass

####################################################################################################
#
# End
#
####################################################################################################
