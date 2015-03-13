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
        self._create_toolbar()

        from .StatusBar import StatusBar
        self.status_bar = StatusBar(self)

    ##############################################
    
    def _create_actions(self):

        icon_loader = IconLoader()

        self._save_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Save',
                    self,
                    toolTip='Save',
                    triggered=self.save_board,
                    shortcut='Ctrl+S',
                    shortcutContext=Qt.ApplicationShortcut,
                )
        
        self._display_all_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Display All',
                    self,
                    toolTip='Display All',
                    triggered=self.glwidget.display_all,
                    shortcut='Ctrl+A',
                    shortcutContext=Qt.ApplicationShortcut,
                )

    ##############################################
    
    def _create_toolbar(self):

        self._image_tool_bar = self.addToolBar('Main')
        for item in (self._save_action,
                     self._display_all_action,
                    ):
            if isinstance(item,QtWidgets.QAction):
                self._image_tool_bar.addAction(item)
            else:
                self._image_tool_bar.addWidget(item)

        from .ToolBar import ToolBar
        self.tool_bar = ToolBar(self)

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

    ##############################################

    def save_board(self, checked):

        # triggered -> checked ???
        self._application.save()
    
####################################################################################################
#
# End
#
####################################################################################################
