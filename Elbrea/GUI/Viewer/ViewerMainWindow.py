# -*- coding: utf-8 -*-

####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

import logging

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

####################################################################################################

from Elbrea.GUI.Base.MainWindowBase import MainWindowBase
from Elbrea.GUI.Widgets.IconLoader import IconLoader
from .GlWidget import GlWidget

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ViewerMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('ViewerMainWindow')

    ##############################################

    def __init__(self, parent=None):

        super(ViewerMainWindow, self).__init__(title='Elbrea Viewer', parent=parent)

        self._init_ui()
        self._create_actions()
        self._create_toolbar()

        from .StatusBar import StatusBar
        self.status_bar = StatusBar(self)

    ##############################################
    
    def _create_actions(self):

        icon_loader = IconLoader()

        self._switch_front_back_action = \
            QtGui.QAction(# icon_loader[''],
                          'Switch Front/Back',
                          self,
                          toolTip='Switch Front/Back',
                          triggered=self.glwidget.switch_front_back,
                          shortcut='Ctrl+F',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

    ##############################################
    
    def _create_toolbar(self):

        self._image_tool_bar = self.addToolBar('Main')
        for item in (self._switch_front_back_action,
                    ):
            if isinstance(item,QtGui.QAction):
                self._image_tool_bar.addAction(item)
            else:
                self._image_tool_bar.addWidget(item)

        from ToolBar import ToolBar
        self.tool_bar = ToolBar(self)

    ##############################################

    def init_menu(self):

        super(ViewerMainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        self._central_widget = QtGui.QWidget(self)
        self._horizontal_layout = QtGui.QHBoxLayout(self._central_widget)

        self.glwidget = GlWidget(self._central_widget)
        self.glwidget.setFocusPolicy(QtCore.Qt.ClickFocus)

        self._horizontal_layout.addWidget(self.glwidget)
        self.setCentralWidget(self._central_widget)

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass

####################################################################################################
#
# End
#
####################################################################################################
