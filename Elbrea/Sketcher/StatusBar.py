####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from PyQt5 import QtWidgets, QtCore

####################################################################################################

class StatusBar(object):

    _logger = logging.getLogger(__name__)

    ##############################################
    
    def __init__(self, main_window):

        self._main_window = main_window
        self._status_bar = self._main_window.statusBar()

        self._application = QtWidgets.QApplication.instance()

        label_definitions = (('message_label', 'Message'),
                             ('coordinate_label', 'Coordinate of the pointer'),
                             )

        for attribute_name, tool_tip in label_definitions:
            widget = QtWidgets.QLabel(toolTip=tool_tip)
            setattr(self, attribute_name, widget)

        self.update_status_message('W'*30)
        coordinate_max = 10**5
        self.update_coordinate_status(coordinate_max, coordinate_max)

        for widget in (self.message_label,
                       self.coordinate_label,
                       ):
            # Permanently means that the widget may not be obscured by temporary messages. It is is
            # located at the far right of the status bar.
            self._status_bar.addPermanentWidget(widget)
            widget.setMinimumSize(widget.sizeHint())
            widget.clear()
           
        self.update_coordinate_status(0, 0)

    ##############################################

    def update_status_message(self, message):

        self.message_label.setText(message)

    ##############################################

    def update_coordinate_status(self, x, y):

        text = '(%6u, %6u) mm' % (x, y)
        self.coordinate_label.setText(text)
        
####################################################################################################
#
# End
#
####################################################################################################
