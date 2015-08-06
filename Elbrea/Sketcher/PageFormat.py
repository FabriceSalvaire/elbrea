####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

from .Unit import mm2in

####################################################################################################

class PageFormat(object):

    ##############################################

    def __init__(self, name, largest_length, smallest_length, portrait=True):

        self._name = name
        self._largest_length = max(smallest_length, largest_length)
        self._smallest_length = min(smallest_length, largest_length)
        self._portrait = portrait

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def largest_length(self):
        return self._largest_length

    @property
    def smallest_length(self):
        return self._smallest_length

    @property
    def height(self):
        if self._portrait:
            return self._largest_length
        else:
            return self._smallest_length

    @property
    def width(self):
        if self._portrait:
            return self._smallest_length
        else:
            return self._largest_length

    @property
    def is_portrait(self):
        return self._portrait

    @property
    def is_landscape(self):
        return not self._portrait

    ##############################################

    def height_px(self, dpi):
        return mm2in(self.height)*dpi

    ##############################################

    def width_px(self, dpi):
        return mm2in(self.width)*dpi

####################################################################################################

def page_format_database(name, portrait=True):

    if name == 'a4':
        return PageFormat('a4', 297, 210, portrait)
    else:
        raise ValueError('Unknown page format {}'.format(name))

####################################################################################################
#
# End
#
####################################################################################################
