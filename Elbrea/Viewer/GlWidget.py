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

####################################################################################################

#!# from PyOpenGLng.HighLevelApi.GlOrtho2D import ZoomManagerAbc

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Buffer import GlUniformBuffer
from PyOpenGLng.HighLevelApi.GlWidgetBase import GlWidgetBase
from PyOpenGLng.Tools.Interval import IntervalInt2D

from Elbrea.GraphicEngine.GraphicScene import GraphicScene
from Elbrea.Image.Colour import RgbIntColour

####################################################################################################
 
_module_logger = logging.getLogger(__name__)

####################################################################################################

class GlWidget(GlWidgetBase):

    _logger = _module_logger.getChild('GlWidget')
 
    ##############################################
    
    def __init__(self, parent):

        self._logger.debug('Initialise GlWidget')

        super(GlWidget, self).__init__(parent)

        self._application = QtWidgets.QApplication.instance()

        self._previous_position = None

        self._painter_manager = None

    ##############################################

    def init_tools(self):

        from .Cropper import Cropper
        self.cropper = Cropper(self)

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

    def _set_previous_position(self, position):

        self._previous_position = position

    ##############################################

    def mousePressEvent(self, event):

        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        tool_bar = self._application.main_window.tool_bar
        current_tool = tool_bar.current_tool()
        if current_tool in (tool_bar.crop_tool_action,):
            scene_match = self.scene.mousePressEvent(event)
            if not scene_match:
                if current_tool is tool_bar.crop_tool_action:
                    self.cropper.begin(event) # Fixme: call mousePressEvent
        else:
            if current_tool is tool_bar.position_tool_action:
                position = self.window_to_gl_coordinate(event, round_to_integer=False)
                self.show_coordinate(position)
                self._set_previous_position(position)
            elif current_tool is tool_bar.colour_picker_tool_action:
                if event.modifiers() == (QtCore.Qt.ControlModifier):
                    self.intensity_profile_picker(event)
                else:
                    self.colour_picker(event)

    ##############################################
        
    def mouseReleaseEvent(self, event):

        button = event.button()
        if button & QtCore.Qt.RightButton:
            self.contextual_menu.exec_(event.globalPos())
        elif button & QtCore.Qt.LeftButton:
            tool_bar = self._application.main_window.tool_bar
            current_tool = tool_bar.current_tool()
            # if current_tool is tool_bar.position_tool_action:
            #     position = self.window_to_gl_coordinate(event, round_to_integer=False)
            #     dxy = self._previous_position - position
            #     self.translate_xy(dxy)
            #     self._set_previous_position(position)
            if current_tool is tool_bar.crop_tool_action:
                self.cropper.end(event) # Fixme: call mouseReleaseEvent

    ##############################################

    def wheelEvent(self, event):

        return self.wheel_zoom(event)

    ##############################################

    def mouseMoveEvent(self, event):

        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        tool_bar = self._application.main_window.tool_bar
        current_tool = tool_bar.current_tool()
        if current_tool is tool_bar.position_tool_action:
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            # Fixme: if out of viewer position = -1exxx
            dxy = self._previous_position - position
            self.translate_xy(dxy)
            self._set_previous_position(position)
            self.show_coordinate(position)
        elif current_tool is tool_bar.colour_picker_tool_action:
            self.colour_picker(event)
        elif current_tool is tool_bar.crop_tool_action:
            self.cropper.update(event) # Fixme: call mouseMoveEvent
                
    ##############################################

    def show_coordinate(self, position):

        x, y = position
        self._application.main_window.status_bar.update_coordinate_status(x, y)
        # self._set_previous_position(position)

    ##############################################

    def colour_picker(self, event):

        position = self.window_to_gl_coordinate(event, round_to_integer=True)
        x, y = position
        image = self._current_image()
        rgb_colour = RgbIntColour(image[y,x])
        self._application.main_window.status_bar.update_colour_intensities_status(rgb_colour)
        self.show_coordinate(position)
        # self._set_previous_position(position)

    ##############################################

    def intensity_profile_picker(self, event):

        coordinate = self.window_to_gl_coordinate(event, round_to_integer=True)
        self._show_intensity_profile(coordinate)
        # self._set_previous_position(position)

    ##############################################
        
    def _show_intensity_profile(self, location):
        
        from .IntensityProfileForm import LineIntensityProfileForm
        x_profile, y_profile = self._intensity_line_picker(location, self._current_image())
        self._intensity_profile_form = LineIntensityProfileForm(x_profile, y_profile)
        self._intensity_profile_form.show()

    ##############################################

    def _intensity_line_picker(self, location, image, axis='xy'):

        if axis not in ('x', 'y', 'xy'):
            raise IndexError

        from .IntensityProfile import LineIntensityProfile

        x_profile = None # row
        y_profile = None # column
        
        height, width = image.shape[:2]
        if 'x' in axis:
            x_profile = LineIntensityProfile(location, 'x', 3, width)
        if 'y' in axis:
            y_profile = LineIntensityProfile(location, 'y', 3, height)
        x, y = location
        margin = 5
        for wave in range(3):
            if x_profile is not None:
                x_profile[wave] = np.mean(image[y-margin:y+margin,:,wave], 0)
            if y_profile is not None:
                y_profile[wave] = image[:,x,wave]

        if axis == 'x':
            return x_profile
        elif axis == 'y':
            return y_profile
        elif axis == 'xy':
            return x_profile, y_profile

    ##############################################

    def switch_front_back(self):

        self._logger.info('')

####################################################################################################
#
# End
#
####################################################################################################
