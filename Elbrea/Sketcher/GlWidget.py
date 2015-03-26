####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

from PyQt5 import QtCore, QtGui, QtWidgets

####################################################################################################

#!# from PyOpenGLng.HighLevelApi.GlOrtho2D import ZoomManagerAbc

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Buffer import GlUniformBuffer
from PyOpenGLng.HighLevelApi.GlWidgetBase import GlWidgetBase, XAXIS
from PyOpenGLng.HighLevelApi.Ortho2D import ZoomManagerAbc
from PyOpenGLng.Math.Geometry import Vector
from PyOpenGLng.Math.Interval import IntervalInt2D # duplicated

from .TabletEvent import TabletEvent, TabletPointerType, TabletEventType
from Elbrea.GraphicEngine.GraphicScene import GraphicScene

####################################################################################################
 
_module_logger = logging.getLogger(__name__)

####################################################################################################

from Elbrea.Tools.EnumFactory import EnumFactory
tool_enum = EnumFactory('ToolEnum', ('pan', 'roi', 'select',
                                     'path', 'segment',
                                     'eraser',
                                     'text', 'image'))

####################################################################################################

class ZoomManager(ZoomManagerAbc):

    _logger = _module_logger.getChild('ZoomManager')

    ##############################################
    
    def __init__(self):

        super(ZoomManager, self).__init__()

        self._fit_zoom_factor = 1

    ##############################################

    def update_fit_zoom_factor(self, zoom_factor):

        self._fit_zoom_factor = zoom_factor * .9
        
    ##############################################
    
    def check_zoom(self, zoom_factor):

        self._logger.info(str(zoom_factor))

        if self._fit_zoom_factor < zoom_factor < 5:
            self.zoom_factor = zoom_factor
            return True, zoom_factor
        else:
            return False, self.zoom_factor

####################################################################################################

class GlWidget(GlWidgetBase):

    _logger = _module_logger.getChild('GlWidget')
 
    ##############################################
    
    def __init__(self, parent):

        self._logger.debug('Initialise GlWidget')

        super(GlWidget, self).__init__(parent)

        self._application = QtWidgets.QApplication.instance()

        # Setup OpenGL 
        self.clear_colour = (1, 1, 1, 0)
        # self.clear_bit = GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT
        
        # Setup navigation
        self.zoom_step = 1.25

        self._painter_manager = None

        self._contextual_menu = QtWidgets.QMenu()

        self._page_manager = None
        self._page_interval = None

        self._previous_position = None
        self._previous_position_screen = None
        
        self._current_tool = None
        self._sketcher = None
        self._pointer_type = None
        
    ##############################################

    def _set_cursor(self):

        pass

        # Don't work as expected 
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

    @property
    def page_manager(self):
        return self._page_manager

    @page_manager.setter
    def page_manager(self, page_manager):
        self._page_manager = page_manager
        
    @property
    def page_interval(self):
        return self._page_interval

    @page_interval.setter
    def page_interval(self, interval):
        self._page_interval = interval
        self._update_zoom_manager() # Fixme: check
        
    ##############################################

    def init_tools(self):

        # Fixme:
        from Elbrea.GraphicEngine.Cropper import Cropper
        self.cropper = Cropper(self)
        self.set_current_tool()

    ##############################################

    def register_menu(self, menu):
        
        """ Register a sub-menu in the contextual menu """
        
        self._contextual_menu.addMenu(menu)

    ##############################################

    def register_action(self, action):
        
        """ Register an action in the contextual menu """

        self._contextual_menu.addAction(action)
        
    ##############################################

    def init_glortho2d(self):

        # Set max_area so as to correspond to max_binning zoom centered at the origin
        area_size = 10**5
        max_area = IntervalInt2D([-area_size, area_size], [-area_size, area_size])

        super(GlWidget, self).init_glortho2d(max_area, zoom_manager=ZoomManager())

        self.scene = GraphicScene(self.glortho2d)

    ##############################################

    def initializeGL(self):

        self._logger.debug('Initialise GL')
        super(GlWidget, self).initializeGL()

        # GL.glEnable(GL.GL_DEPTH_TEST) # Fixme: cf. clear_bit

        GL.glEnable(GL.GL_BLEND)
        # Blending: O = Sf*S + Df*D
        # alpha: 0: complete transparency, 1: complete opacity
        # Set (Sf, Df) for transparency: O = Sa*S + (1-Sa)*D 
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self._init_shader()
        self._ready = False

    ##############################################

    def _update_zoom_manager(self):

        # Fixme:
        #   axis_scale = self.window.size() / np.array(interval.size(), dtype=np.float)
        #   AttributeError: 'NoneType' object has no attribute 'size' 
        if self._page_interval is not None:
            glortho2d = self.glortho2d
            axis, zoom_factor = glortho2d._compute_zoom_to_fit_interval(self._page_interval)
            glortho2d.zoom_manager.update_fit_zoom_factor(zoom_factor)
    
    ##############################################

    def resizeGL(self, width, height):

        super(GlWidget, self).resizeGL(width, height)
        self._update_zoom_manager()
            
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

        self.glortho2d.zoom_interval(self._page_interval)
        self.update()

    ##############################################

    def fit_width(self):

        # self.glortho2d.viewport_area.area.x.length()
        self.glortho2d.fit_axis(self._page_interval.x.length(), XAXIS)
        self.update()

    ##############################################

    def set_current_tool(self):
        
        # Fixme: design, tool_bar.xxx ?
        # implement receiver
        tool_bar = self._application.main_window.sketcher_tool_bar
        current_tool = tool_bar.current_tool()
        page_manager = self._application.page_manager
        self._current_tool = None
        if current_tool is tool_bar.pen_tool_action:
            self._current_tool = tool_enum.path
            self._sketcher = page_manager.path_sketcher
            self._pointer_type = TabletPointerType.pen
        elif current_tool is tool_bar.segment_tool_action:
            self._current_tool = tool_enum.segment
            self._sketcher = page_manager.segment_sketcher
            self._pointer_type = TabletPointerType.pen
        elif current_tool is tool_bar.eraser_tool_action:
            self._current_tool = tool_enum.eraser
            self._sketcher = page_manager.eraser
            self._pointer_type = TabletPointerType.eraser
        else:
            self._sketcher = None
            self._pointer_type = None
            if current_tool is tool_bar.pan_tool_action:
                self._current_tool = tool_enum.pan
            elif current_tool is tool_bar.roi_tool_action:
                self._current_tool = tool_enum.roi
            elif current_tool is tool_bar.select_tool_action:
                self._current_tool = tool_enum.select
            elif current_tool is tool_bar.text_tool_action:
                self._current_tool = tool_enum.text
            elif current_tool is tool_bar.image_tool_action:
                self._current_tool = tool_enum.image
                
    ##############################################

    def event_position(self, event):

        """ Convert mouse coordinate
        """

        # self._logger.info("{} {}".format(event.x(), event.y()))
        return Vector(event.x(), event.y()) # dtype=np.int for subtraction
        
    ##############################################

    def _set_previous_position(self, position, position_screen):

        self._previous_position = position
        self._previous_position_screen = position_screen

    ##############################################

    def _show_coordinate(self, position):

        x, y = self._page_manager.px2mm(position)
        self._application.main_window.status_bar.update_coordinate_status(x, y)
        # self._set_previous_position(position)
        
    ##############################################

    def mousePressEvent(self, event):

        self._logger.info("")

        button = event.button()
        if button & QtCore.Qt.LeftButton:
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            if self._sketcher is not None:
                tablet_event = TabletEvent(TabletEventType.press, self._pointer_type, position)
                if self._sketcher.on_pen_event(tablet_event):
                    self.update()
            elif self._current_tool == tool_enum.pan:
                self._set_previous_position(position, self.event_position(event))
            elif self._current_tool == tool_enum.roi:
                scene_match = self.scene.mousePressEvent(event)
                if not scene_match:
                    # Fixme: call mousePressEvent
                    self.cropper.begin(event)
            elif self._current_tool == tool_enum.image:
                from .ImagePropertiesForm import ImagePropertiesForm
                dialog = ImagePropertiesForm(position)
                dialog.exec_() 
            elif self._current_tool == tool_enum.select:
                self._page_manager.select_around(position)
            self._show_coordinate(position)

    ##############################################
        
    def mouseReleaseEvent(self, event):

        self._logger.info("")
        
        button = event.button()
        if button & QtCore.Qt.RightButton:
            self._contextual_menu.exec_(event.globalPos())
        elif button & QtCore.Qt.LeftButton:
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            if self._sketcher is not None:
                tablet_event = TabletEvent(TabletEventType.release, self._pointer_type, position)
                if self._sketcher.on_pen_event(tablet_event):
                    self.update()
            elif self._current_tool == tool_enum.roi:
                 # Fixme: call mouseReleaseEvent
                self.cropper.end(event)
            self._show_coordinate(position)

    ##############################################

    def mouseMoveEvent(self, event):

        # self._logger.info("")

        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        position = self.window_to_gl_coordinate(event, round_to_integer=False)
        if self._sketcher is not None:
            tablet_event = TabletEvent(TabletEventType.move, self._pointer_type, position)
            if self._sketcher.on_pen_event(tablet_event):
                self.update()
        elif self._current_tool == tool_enum.pan:
            position_screen = self.event_position(event)
            dxy_screen = self._previous_position_screen - position_screen
            # Fixme: if out of viewer position = -1exxx
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            dxy = self._previous_position - position
            # dxy *= [1, -1]
            # self._logger.info("{} {} / {} {}".format(dxy_screen[0], dxy_screen[1], int(dxy[0]), int(dxy[0])))
            dxy_screen *= self.glortho2d.parity_display_scale
            self.translate_xy(dxy_screen)
            self._set_previous_position(position, position_screen)
            self._show_coordinate(position)
        elif self._current_tool == tool_enum.roi:
            # Fixme: call mouseMoveEvent
            self.cropper.update(event)
        self._show_coordinate(position)

    ##############################################

    def wheelEvent(self, event):

        return self.wheel_zoom(event)
                
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
            if self._sketcher is not None:
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
                if self._sketcher.on_pen_event(tablet_event):
                    self.update()
        except Exception as exception:
            self._logger.error(str(exception))
            
####################################################################################################
#
# End
#
####################################################################################################
