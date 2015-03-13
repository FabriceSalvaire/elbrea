####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from Elbrea.GUI.Base.MainWindowBase import MainWindowBase
from Elbrea.GUI.Base.IconLoader import IconLoader
from .GlWidget import GlWidget

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SketcherMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('SketcherMainWindow')

    ##############################################

    def __init__(self, parent=None):

        super(SketcherMainWindow, self).__init__(title='Elbrea Sketcher', parent=parent)

        self._init_ui()
        self._create_actions()
        self._create_toolbars()

        from .StatusBar import StatusBar
        self.status_bar = StatusBar(self)

    ##############################################
    
    def _create_actions(self):

        pass
    
    ##############################################
    
    def _create_toolbars(self):

        from .ToolBar import MainToolBar, SketcherToolBar
        self.main_tool_bar = MainToolBar(self)
        self.sketcher_tool_bar = SketcherToolBar(self)

    ##############################################

    def init_menu(self):

        super(SketcherMainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        # self._central_widget = QtWidgets.QWidget(self)
        # self._horizontal_layout = QtWidgets.QHBoxLayout(self._central_widget)

        self.resize(500, 500)
        
        self.glwidget = GlWidget(self) # ._central_widget
        self.glwidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.glwidget.setMinimumSize(100, 100)
        self._central_widget = self.glwidget

        # self._horizontal_layout.addWidget(self.glwidget)
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
