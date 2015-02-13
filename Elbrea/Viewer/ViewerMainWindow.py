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

        self._save_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Save',
                    self,
                    toolTip='Save',
                    triggered=self._application.save,
                    shortcut='Ctrl+S',
                    shortcutContext=Qt.ApplicationShortcut,
                )
        
        self._switch_face_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Switch Front/Back',
                    self,
                    toolTip='Switch Front/Back',
                    triggered=self._application.switch_face,
                    shortcut='Ctrl+F',
                    shortcutContext=Qt.ApplicationShortcut,
                )

        self._refresh_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Refresh',
                    self,
                    toolTip='Refresh',
                    triggered=self.glwidget.update,
                    shortcut='Ctrl+R',
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

        self._reload_user_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Reload User',
                    self,
                    toolTip='Reload User',
                    triggered=self._application.reload_user,
                    shortcut='Ctrl+U',
                    shortcutContext=Qt.ApplicationShortcut,
                )

    ##############################################
    
    def _create_toolbar(self):

        self._image_tool_bar = self.addToolBar('Main')
        for item in (self._save_action,
                     self._switch_face_action,
                     self._refresh_action,
                     self._display_all_action,
                     self._reload_user_action,
                    ):
            if isinstance(item,QtWidgets.QAction):
                self._image_tool_bar.addAction(item)
            else:
                self._image_tool_bar.addWidget(item)

        filter_combo_box = QtWidgets.QComboBox(self)
        filter_combo_box.addItem('raw')
        filter_combo_box.addItem('hls')
        filter_combo_box.addItem('user')
        filter_combo_box.currentIndexChanged[str].connect(self._application.on_filter_changed)
        self._image_tool_bar.addWidget(filter_combo_box)

        from .ToolBar import ToolBar
        self.tool_bar = ToolBar(self)

    ##############################################

    def init_menu(self):

        super(ViewerMainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        # self._central_widget = QtWidgets.QWidget(self)
        # self._horizontal_layout = QtWidgets.QHBoxLayout(self._central_widget)

        self.glwidget = GlWidget(self) # ._central_widget
        self.glwidget.setFocusPolicy(QtCore.Qt.ClickFocus)
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
