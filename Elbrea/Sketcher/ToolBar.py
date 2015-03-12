####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

####################################################################################################

from Elbrea.GUI.Base.IconLoader import IconLoader

####################################################################################################

class ToolBar(object):

    icon_size = 22

    ##############################################
    
    def __init__(self, main_window):

        self._application = QtWidgets.QApplication.instance()
        self._main_window = main_window
        self._tool_bar = main_window.addToolBar('Main')

        self._create_actions()
        self._init_tool_bar()

    ##############################################
    
    def _create_actions(self):

        icon_loader = IconLoader()

        self.clear_tool_action = \
            QtWidgets.QAction('Clear',
                          self._application,
                          toolTip='Clear Tool',
                          triggered=self.clear_tool,
                          )

        self.position_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('position-tool', self.icon_size),
                          'Position Tool',
                          self._application,
                          checkable=True,
                          )
        
        self.pen_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('pencil', self.icon_size),
                          'Pen Tool',
                          self._application,
                          checkable=True,
                          )

        self.segment_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('pencil', self.icon_size), # Fixme:
                          'Segment Tool',
                          self._application,
                          checkable=True,
                          )
        
        self.eraser_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('eraser', self.icon_size),
                          'Eraser Tool',
                          self._application,
                          checkable=True,
                          )
        
        self._action_group = QtWidgets.QActionGroup(self._application)
        for action in (self.pen_tool_action,
                       self.segment_tool_action,
                       self.eraser_tool_action,
                       ):
            self._action_group.addAction(action)

    ##############################################

    def _init_tool_bar(self):
                
        self._pencil_size_combobox = QtWidgets.QComboBox(self._main_window)
        for pencil_size in (1, 2, 3, 6, 12):
            self._pencil_size_combobox.addItem(str(pencil_size), pencil_size)
            
        self._pencil_colour_combobox = QtWidgets.QComboBox(self._main_window)
        self._pencil_colours = (Qt.white, Qt.black,
                                Qt.red, Qt.blue, Qt.green,
                                Qt.cyan, Qt.magenta, Qt.yellow,
                            )
        for colour in self._pencil_colours:
            pixmap = QtGui.QPixmap(10, 10)
            pixmap.fill(colour)
            icon = QtGui.QIcon(pixmap)
            self._pencil_colour_combobox.addItem(icon, '')
            
        self._eraser_size_combobox = QtWidgets.QComboBox(self._main_window)
        for eraser_size in (3, 6, 12):
            self._eraser_size_combobox.addItem(str(eraser_size), eraser_size)

        self._pencil_size_combobox.currentIndexChanged.connect(self._on_pencil_size_changed)
        self._eraser_size_combobox.currentIndexChanged.connect(self._on_eraser_size_changed)
        self._pencil_colour_combobox.currentIndexChanged.connect(self._on_pencil_colour_changed)
        # self._eraser_size_combobox.currentIndexChanged.connect(self._on_eraser_size_changed)
        
        self._tool_bar.addAction(self.clear_tool_action)
        items = (self.position_tool_action,
                 self.pen_tool_action,
                 self.segment_tool_action,
                 self._pencil_size_combobox,
                 self._pencil_colour_combobox,
                 self.eraser_tool_action,
                 self._eraser_size_combobox,
        )
        for item in items:
            if isinstance(item, QtWidgets.QAction):
                self._tool_bar.addAction(item)
            else:
                self._tool_bar.addWidget(item)
            
    ##############################################

    def current_tool(self):

        return self._action_group.checkedAction()

    ##############################################

    def clear_tool(self):

        pass

        # current_tool = self.current_tool()

        # if current_tool is self.crop_tool_action:
        #     self._application.main_window.glwidget.cropper.reset()

    ##############################################

    def _on_pencil_size_changed(self, index):

        self._application.sketcher_state.pencil_size = self._pencil_size_combobox.currentData()

    ##############################################

    def _on_eraser_size_changed(self, index):

        self._application.sketcher_state.eraser_size = self._eraser_size_combobox.currentData()
        
    ##############################################

    def _on_pencil_colour_changed(self, index):

        colour = QtGui.QColor(self._pencil_colours[index])
        self._application.sketcher_state.pencil_colour = (colour.red(), colour.green(), colour.blue())
        
####################################################################################################
#
# End
#
####################################################################################################
