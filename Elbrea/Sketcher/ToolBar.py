####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

####################################################################################################

from Elbrea.GUI.Base.IconLoader import IconLoader
icon_loader = IconLoader()

####################################################################################################

class ToolBar(object):

    icon_size = 22

    __name__= None
    
    ##############################################
    
    def __init__(self, main_window):

        self._application = QtWidgets.QApplication.instance()
        self._main_window = main_window # self._application.main_window
        self._glwidget  = main_window.glwidget
        self._tool_bar = main_window.addToolBar(self.__name__)

        self._create_actions()
        self._init_tool_bar()

    ##############################################
    
    def _create_actions(self):

        raise NotImplementedError

    ##############################################
    
    def _init_tool_bar(self):

        raise NotImplementedError

    ##############################################

    def _add_items(self, items):

        for item in items:
            if isinstance(item, QtWidgets.QAction):
                self._tool_bar.addAction(item)
            else:
                self._tool_bar.addWidget(item)
    
####################################################################################################

class MainToolBar(ToolBar):

    __name__= 'main'
   
    ##############################################
    
    def _create_actions(self):

        self._save_action = \
                QtWidgets.QAction(icon_loader['document-save'],
                    'Save',
                    self._application,
                    toolTip='Save',
                    triggered=self.save_board,
                    shortcut='Ctrl+S',
                    shortcutContext=Qt.ApplicationShortcut,
                )

        self._zoom_one_action = \
                QtWidgets.QAction(icon_loader['zoom-original'],
                    'Zoom 1:1',
                    self._application,
                    toolTip='Zoom 1:`',
                    triggered=self._main_window.glwidget.zoom_one,
                    # shortcut='Ctrl+',
                    shortcutContext=Qt.ApplicationShortcut,
                )
        
        self._fit_width_action = \
                QtWidgets.QAction(icon_loader['zoom-fit-width'],
                    'Fit width',
                    self._application,
                    toolTip='Fit width',
                    triggered=self._main_window.glwidget.fit_width,
                    shortcut='Ctrl+W',
                    shortcutContext=Qt.ApplicationShortcut,
                )
        
        self._display_all_action = \
                QtWidgets.QAction(icon_loader['zoom-fit-best'],
                    'Display All',
                    self._application,
                    toolTip='Display All',
                    triggered=self._main_window.glwidget.display_all,
                    shortcut='Ctrl+A',
                    shortcutContext=Qt.ApplicationShortcut,
                )

    ##############################################

    def _init_tool_bar(self):
        
        items = (self._save_action,
                 self._zoom_one_action,
                 self._fit_width_action,
                 self._display_all_action,
                )
        self._add_items(items)

    ##############################################

    def save_board(self, checked):

        # triggered -> checked ???
        self._application.save()
                
####################################################################################################

class SketcherToolBar(ToolBar):

    __name__= 'sketcher'

    ##############################################
    
    def _create_actions(self):

        self.clear_tool_action = \
            QtWidgets.QAction('Clear',
                          self._application,
                          toolTip='Clear Tool',
                          triggered=self.clear_tool,
                          )

        self.pan_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('position-tool', self.icon_size),
                          'Position Tool',
                          self._application,
                          checkable=True,
                          )

        self.roi_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('crop-tool', self.icon_size),
                          'Roi Tool',
                          self._application,
                          checkable=True,
                          )

        self.select_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('edit-select', self.icon_size),
                          'Selection Tool',
                          self._application,
                          checkable=True,
                          )
        
        self.pen_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('draw-freehand', self.icon_size),
                          'Pen Tool',
                          self._application,
                          checkable=True,
                          )

        self.segment_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('draw-path', self.icon_size),
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

        self.text_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('text-tool', self.icon_size),
                          'Text Tool',
                          self._application,
                          checkable=True,
                          )
        
        self.image_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('insert-image', self.icon_size),
                          'Image Tool',
                          self._application,
                          checkable=True,
                          )
        
        self._sketcher_action_group = QtWidgets.QActionGroup(self._application)
        for action in (self.pan_tool_action,
                       self.roi_tool_action,
                       self.select_tool_action,
                       self.pen_tool_action,
                       self.segment_tool_action,
                       self.eraser_tool_action,
                       self.text_tool_action,
                       self.image_tool_action,
                       ):
            self._sketcher_action_group.addAction(action)
            self._glwidget.register_action(action)
            
    ##############################################

    def _init_tool_bar(self):

        self.pan_tool_action.setChecked(True)
        self._sketcher_action_group.triggered.connect(self._main_window.glwidget.set_current_tool)
        
        self._pencil_size_combobox = QtWidgets.QComboBox(self._main_window)
        for pencil_size in (1, 2, 3, 6, 12):
            self._pencil_size_combobox.addItem(str(pencil_size), pencil_size)
            
        self._pencil_colour_combobox = QtWidgets.QComboBox(self._main_window)
        self._pencil_colours = (Qt.black,
                                Qt.red, Qt.blue, Qt.green,
                                Qt.cyan, Qt.magenta, Qt.yellow,
                                Qt.white)
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
        self._eraser_size_combobox.currentIndexChanged.connect(self._on_eraser_size_changed)
       
        items = (self.clear_tool_action,
                 self.pan_tool_action,
                 self.roi_tool_action,
                 self.select_tool_action,
                 self.pen_tool_action,
                 self.segment_tool_action,
                 self._pencil_size_combobox,
                 self._pencil_colour_combobox,
                 self.eraser_tool_action,
                 self._eraser_size_combobox,
                 self.text_tool_action,
                 self.image_tool_action,
                )
        self._add_items(items)
        
    ##############################################

    def current_tool(self):

        return self._sketcher_action_group.checkedAction()

    ##############################################

    def clear_tool(self):

        current_tool = self.current_tool()

        if current_tool is self.roi_tool_action:
            self._main_window.glwidget.cropper.reset()

    ##############################################

    def _on_pencil_size_changed(self, index):

        page_manager = self._application.page_manager
        page_manager.sketcher_state.pencil_size = self._pencil_size_combobox.currentData()

    ##############################################

    def _on_eraser_size_changed(self, index):

        page_manager = self._application.page_manager
        page_manager.sketcher_state.eraser_size = self._eraser_size_combobox.currentData()
        
    ##############################################

    def _on_pencil_colour_changed(self, index):

        page_manager = self._application.page_manager
        colour = QtGui.QColor(self._pencil_colours[index])
        page_manager.sketcher_state.pencil_colour = (colour.red(), colour.green(), colour.blue())

    ##############################################

    def init_sketcher_state(self):
        
        self._on_pencil_size_changed(0)
        self._on_eraser_size_changed(0)
        self._on_pencil_colour_changed(0)
        self._on_eraser_size_changed(0)

####################################################################################################

class PageToolBar(ToolBar):

    __name__ = 'page'

    ##############################################
    
    def _create_actions(self):

        self.previous_page_action = \
            QtWidgets.QAction('Previous',
                          self._application,
                          toolTip='Previous page',
                          # triggered=self.goto_previous_page,
                          )

        self.next_page_action = \
            QtWidgets.QAction('Next',
                          self._application,
                          toolTip='Next page',
                          # triggered=self.goto_next_page,
                          )

    ##############################################

    def _init_tool_bar(self):

        self._page_spinbox = QtWidgets.QSpinBox(self._main_window)
        self._page_spinbox.setMinimum(1)
        self._number_of_pages_label = QtWidgets.QLabel(self._main_window)
        self.update_number_of_pages(1)
        
        self._page_spinbox.valueChanged.connect(self._on_page_changed)
       
        items = (# self.previous_page_action,
                 # self.next_page_action,
                 self._page_spinbox,
                 self._number_of_pages_label,
                )
        self._add_items(items)

    ##############################################

    def update_number_of_pages(self, number_of_pages):

        self._number_of_pages_label.setText(' / {}'.format(number_of_pages))
        
    ##############################################

    def _on_page_changed(self, index):

        page_index = index -1
        page_manager = self._application.page_manager
        if page_index > page_manager.last_page_index:
            page_manager.add_page()
            self.update_number_of_pages(page_manager.number_of_pages)
        self._application.page_manager.select_page(page_index)
        
####################################################################################################
#
# End
#
####################################################################################################
