####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np

import cv2 # Fixme

####################################################################################################

#!# from PyOpenGLng.HighLevelApi.GlOrtho2D import ZoomManagerAbc

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Buffer import GlUniformBuffer
from PyOpenGLng.HighLevelApi.GlWidgetBase import GlWidgetBase
from PyOpenGLng.Math.Interval import IntervalInt2D # duplicated

from .Sketcher import TabletEvent, TabletPointerType, TabletEventType
from Elbrea.GraphicEngine.GraphicScene import GraphicScene

####################################################################################################
 
_module_logger = logging.getLogger(__name__)

####################################################################################################

class GlWidget(GlWidgetBase):

    _logger = _module_logger.getChild('GlWidget')
 
    ##############################################
    
    def __init__(self, parent):

        self._logger.debug('Initialise GlWidget')

        super(GlWidget, self).__init__(parent)
        self.clear_colour = (1, 1, 1, 0)
        
        self._application = QtWidgets.QApplication.instance()

        self._previous_position = None
        self._previous_position_screen = None

        self._painter_manager = None

        # cursor_size = 16
        # # B=1 M=1 black
        # # B=0 M=1 white
        # # B=0 M=0 transparent
        # data = np.zeros((cursor_size, cursor_size), dtype=np.uint8)
        # border = 3
        # data[...] = 1
        # data[:border] = 0
        # data[-border:] = 0
        # data[:,:border] = 0
        # data[:,-border:] = 0
        # bitmap = QtGui.QBitmap.fromData(QtCore.QSize(cursor_size, cursor_size), data.flatten())
        # data = np.zeros((cursor_size, cursor_size), dtype=np.bool)
        # data[...] = 1
        # mask = QtGui.QBitmap.fromData(QtCore.QSize(cursor_size, cursor_size), data.flatten())
        # self._cursor = QtGui.QCursor(bitmap, mask)
        # self.setCursor(self._cursor)
        
    ##############################################

    def init_tools(self):

        pass
        # from .Cropper import Cropper
        # self.cropper = Cropper(self)

    ##############################################

    def init_glortho2d(self):

        # Set max_area so as to correspond to max_binning zoom centered at the origin
        area_size = 10**5
        max_area = IntervalInt2D([-area_size, area_size], [-area_size, area_size])

        super(GlWidget, self).init_glortho2d(max_area, zoom_manager=None)

        self.scene = GraphicScene(self.glortho2d)

    ##############################################

    def initializeGL(self):

        self._logger.debug('Initialise GL')
        super(GlWidget, self).initializeGL()
        self._init_shader()
        self._ready = False

    ##############################################

    def _init_shader(self):

        self._logger.debug('Initialise Shader')

        from Elbrea.GraphicEngine import ShaderProgrames as ShaderProgrames
        self.shader_manager = ShaderProgrames.shader_manager
        self.position_shader_interface = ShaderProgrames.position_shader_program_interface

        # Fixme: share interface
        self._viewport_uniform_buffer = GlUniformBuffer()
        viewport_uniform_block = self.position_shader_interface.uniform_blocks.viewport
        self._viewport_uniform_buffer.bind_buffer_base(viewport_uniform_block.binding_point)

    ##############################################

    def update_model_view_projection_matrix(self):

        viewport_uniform_buffer_data = self.glortho2d.viewport_uniform_buffer_data(self.size())
        self._viewport_uniform_buffer.set(viewport_uniform_buffer_data)

    ##############################################

    def paint(self):

        if self._ready:
            with GL.error_checker():
                self._painter_manager.paint()
                
    ##############################################

    def display_all(self):

        self.glortho2d.zoom_interval(self._image_interval)
        self.update()

    ##############################################

    def event_position(self, event):

        """ Convert mouse coordinate
        """

        self._logger.info("{} {}".format(event.x(), event.y()))
        return np.array((event.x(), event.y()), dtype=np.int) # int for subtraction
        
    ##############################################

    def _set_previous_position(self, position, position_screen):

        self._previous_position = position
        self._previous_position_screen = position_screen

    ##############################################

    def mousePressEvent(self, event):

        self._logger.info("")
       
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        # Fixme: tool triggered -> event receiver
        tool_bar = self._application.main_window.sketcher_tool_bar
        current_tool = tool_bar.current_tool()
        if current_tool in (tool_bar.pen_tool_action,
                            tool_bar.segment_tool_action,
                            tool_bar.eraser_tool_action):
            # Fixme: to func
            if current_tool is tool_bar.pen_tool_action:
                pointer_type = TabletPointerType.pen
                sketcher = self._application.page_manager.path_sketcher
            elif current_tool is tool_bar.segment_tool_action:
                pointer_type = TabletPointerType.pen
                sketcher = self._application.page_manager.segment_sketcher
            else:
                pointer_type = TabletPointerType.eraser
                sketcher = self._application.page_manager.path_sketcher
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            tablet_event = TabletEvent(TabletEventType.press, pointer_type, position)
            if sketcher.on_tablet_event(tablet_event):
                self.update()
                
    ##############################################
        
    def mouseReleaseEvent(self, event):

        self._logger.info("")
        
        button = event.button()
        if button & QtCore.Qt.RightButton:
            self.contextual_menu.exec_(event.globalPos())
        elif button & QtCore.Qt.LeftButton:
            tool_bar = self._application.main_window.sketcher_tool_bar
            current_tool = tool_bar.current_tool()
            if current_tool in (tool_bar.pen_tool_action,
                                tool_bar.segment_tool_action,
                                tool_bar.eraser_tool_action):
                # Fixme: to func
                if current_tool is tool_bar.pen_tool_action:
                    pointer_type = TabletPointerType.pen
                    sketcher = self._application.page_manager.path_sketcher
                elif current_tool is tool_bar.segment_tool_action:
                    pointer_type = TabletPointerType.pen
                    sketcher = self._application.page_manager.segment_sketcher
                else:
                    pointer_type = TabletPointerType.eraser
                    sketcher = self._application.page_manager.path_sketcher
                position = self.window_to_gl_coordinate(event, round_to_integer=False)
                tablet_event = TabletEvent(TabletEventType.release, pointer_type, position)
                if sketcher.on_tablet_event(tablet_event):
                    self.update()
                
    ##############################################

    def wheelEvent(self, event):

        return self.wheel_zoom(event)

    ##############################################

    def mouseMoveEvent(self, event):

        self._logger.info("")
        
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        tool_bar = self._application.main_window.sketcher_tool_bar
        current_tool = tool_bar.current_tool()
        if current_tool is tool_bar.position_tool_action:
            position_screen = self.event_position(event)
            dxy_screen = self._previous_position_screen - position_screen
            # Fixme: if out of viewer position = -1exxx
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            dxy = self._previous_position - position
            # dxy *= [1, -1]
            self._logger.info("{} {} / {} {}".format(dxy_screen[0], dxy_screen[1], int(dxy[0]), int(dxy[0])))
            dxy_screen *= self.glortho2d.parity_display_scale
            self.translate_xy(dxy_screen)
            self._set_previous_position(position, position_screen)
            self.show_coordinate(position)
        # elif current_tool is tool_bar.crop_tool_action:
        #     self.cropper.update(event) # Fixme: call mouseMoveEvent
        elif current_tool in (tool_bar.pen_tool_action,
                              tool_bar.segment_tool_action,
                              tool_bar.eraser_tool_action):
            # Fixme: to func
            if current_tool is tool_bar.pen_tool_action:
                pointer_type = TabletPointerType.pen
                sketcher = self._application.page_manager.path_sketcher
            elif current_tool is tool_bar.segment_tool_action:
                pointer_type = TabletPointerType.pen
                sketcher = self._application.page_manager.segment_sketcher
            else:
                pointer_type = TabletPointerType.eraser
                sketcher = self._application.page_manager.path_sketcher
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            tablet_event = TabletEvent(TabletEventType.move, pointer_type, position)
            if sketcher.on_tablet_event(tablet_event):
                self.update()

    ##############################################

    def tabletEvent(self, event):

        self._logger.info("")

        event.accept()
        # event.ignore()
        
        # pressure = event.pressure()
        # x_tilt = event.xTilt()
        # y_tilt = event.yTilt()
        # self._logger.info("type {} pointer {} pos {} pressure {} tilt {} {}".format(
        #     event_type,
        #     pointer_type,
        #     position,
        #     pressure, x_tilt, y_tilt))

        try:
            tool_bar = self._application.main_window.sketcher_tool_bar
            current_tool = tool_bar.current_tool()
            if current_tool is tool_bar.pen_tool_action:
                event_type = event.type()
                if event_type == QtCore.QEvent.TabletPress:
                    tablet_event_type = TabletEventType.press
                elif event_type == QtCore.QEvent.TabletMove:
                    tablet_event_type = TabletEventType.move
                elif event_type == QtCore.QEvent.TabletRelease:
                    tablet_event_type = TabletEventType.release
                pointer_type = event.pointerType()
                if pointer_type == QtGui.QTabletEvent.Pen:
                    pointer_type = TabletPointerType.pen
                elif pointer_type == QtGui.QTabletEvent.Eraser:
                    pointer_type = TabletPointerType.eraser
                position = self.window_to_gl_coordinate(event, round_to_integer=False)
                tablet_event = TabletEvent(tablet_event_type, pointer_type, position)
                if self._application.page_manager.sketcher.on_tablet_event(tablet_event):
                    self.update()
        except Exception as exception:
            self._logger.error(str(exception))
            
####################################################################################################
#
# End
#
####################################################################################################
