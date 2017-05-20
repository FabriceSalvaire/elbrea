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

class Painter(object):

    """

    Public Attributes:

      :attr:`painter_manager`

      :attr:`status`

    """

    __painter_name__ = None

    _logger = _module_logger.getChild('Painter')

    ##############################################

    def __init__(self, painter_manager, z_value=0, status=True, name=None):

        self._painter_manager = painter_manager
        self._glwidget = painter_manager.glwidget # Fixme: for makeCurrent
        # self._shader_manager = self._glwidget.shader_manager
        
        self._z_value = z_value
        self._status = status
        if name is None:
            self._name = self.__painter_name__ # Fixme: purpose
        else:
            self._name = name

        self._painter_manager.register_painter(self)

    ##############################################

    def __repr__(self):
        return "Painter {} z={} s={}".format(self._name, self._z_value, self._status)

    ##############################################

    def __bool__(self):
        return self._status

    ##############################################

    def __lt__(self, other):

        return self._z_value < other.z_value

    ##############################################

    def _notify_painter_manager(self):
        self._painter_manager.resort()

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def z_value(self):
        return self._z_value

    @z_value.setter
    def z_value(self, value):
        self._z_value = value
        self._notify_painter_manager()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self._notify_painter_manager()

    ##############################################

    def switch(self):
        # Fixme: name, useful ?
        self.status = not self._status

    ##############################################

    def disable(self):
        self.status = False

    ##############################################

    def enable(self):
        self.status = True

    ##############################################

    def paint(self):
        raise NotImplementedError

####################################################################################################

class PainterMetaClass(type):

    """ Metaclass to register all the subclasses. """

    classes = {}

    _logger = _module_logger.getChild('PainterMetaClass')

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        type.__init__(cls, class_name, super_classes, class_attribute_dict)
        if class_name != 'RegisteredPainter':
            # PainterMetaClass._logger.debug("Register painter class %s", cls._name)
            PainterMetaClass.classes[cls.__painter_name__] = cls

####################################################################################################

class RegisteredPainter(Painter, metaclass=PainterMetaClass):
    pass

####################################################################################################
#
# End
#
####################################################################################################
