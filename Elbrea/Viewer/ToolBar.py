# -*- coding: utf-8 -*-

####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from Elbrea.GUI.Base.IconLoader import IconLoader

####################################################################################################

class ToolBar(object):

    icon_size = 22

    ##############################################
    
    def __init__(self, main_window):

        self._tool_bar = main_window.addToolBar('Main')

        self._create_actions()
        self._init_tool_bar()

    ##############################################
    
    def _create_actions(self):

        application = QtWidgets.QApplication.instance()
        icon_loader = IconLoader()

        self.clear_tool_action = \
            QtWidgets.QAction('Clear',
                          application,
                          toolTip='Clear Tool',
                          triggered=self.clear_tool,
                          )

        self.position_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('position-tool', self.icon_size),
                          'Position Tool',
                          application,
                          checkable=True,
                          )

        self.colour_picker_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('colour-picker-tool', self.icon_size),
                          'Colour Picker Tool',
                          application,
                          checkable=True,
                          )

        self.crop_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('crop-tool', self.icon_size),
                          'Crop Tool',
                          application,
                          checkable=True,
                          )

        self._action_group = QtWidgets.QActionGroup(application)
        for action in (self.position_tool_action,
                       self.colour_picker_tool_action,
                       self.crop_tool_action,
                       ):
            self._action_group.addAction(action)

    ##############################################

    def _init_tool_bar(self):
                
        application = QtWidgets.QApplication.instance()

        self.position_tool_action.setChecked(True)
        
        self._tool_bar.addAction(self.clear_tool_action)
        standard_actions = (self.position_tool_action,
                            self.colour_picker_tool_action,
                            self.crop_tool_action,
                            )
        for action in standard_actions:
            self._tool_bar.addAction(action)

    ##############################################

    def current_tool(self):

        return self._action_group.checkedAction()

    ##############################################

    def clear_tool(self):

        application = QtWidgets.QApplication.instance()
        current_tool = self.current_tool()

        if current_tool is self.crop_tool_action:
            application.main_window.glwidget.cropper.reset()

####################################################################################################
#
# End
#
####################################################################################################
