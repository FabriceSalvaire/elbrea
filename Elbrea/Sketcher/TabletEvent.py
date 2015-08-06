####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

from Elbrea.Tools.EnumFactory import EnumFactory

####################################################################################################

TabletPointerType = EnumFactory('TabletPointerType', ('pen', 'eraser'))
TabletEventType = EnumFactory('TabletEventType', ('press', 'move', 'release'))

class TabletEvent(object):

    ##############################################

    def __init__(self, event_type, pointer_type, position, pressure=0):

        self.type = event_type # subclass ?
        self.pointer_type = pointer_type
        self.position = position
        self.pressure = pressure

    ##############################################

    def __repr__(self):

        return "type {} pointer type {}".format(self.type, self.pointer_type)

####################################################################################################
#
# End
#
####################################################################################################
