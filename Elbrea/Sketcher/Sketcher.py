####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

import cv2
import numpy as np

####################################################################################################

from Elbrea.Image.Image import Image
from Elbrea.Math.Interval import IntervalInt2D, Interval2D
from Elbrea.Tools.EnumFactory import EnumFactory
from Elbrea.Tools.TimeStamp import ObjectWithTimeStamp
from .Path import DynamicPath

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

TabletPointerType = EnumFactory('TabletPointerType', ('pen', 'eraser'))
TabletEventType = EnumFactory('TabletEventType', ('press', 'move', 'release'))

class TabletEvent(object):

    ##############################################

    def __init__(self, event_type, pointer_type, position, pressure=0):

        self.type = event_type # subclass ?
        self.pointer_type = pointer_type
        self.position = position
        self.pressure = pressure

    ##############################################

    def __repr__(self):

        return "type {} pointer type {}".format(self.type, self.pointer_type)

####################################################################################################

class PointFilter(object):

    ##############################################   

    def __init__(self, window_size):
        
        self._window_size = window_size
        self._window_points = np.zeros((self._window_size, 2), dtype=np.float32)
        self._window_counter = 0
        self._window_index = 0

    ##############################################

    def __bool__(self):

        return self._window_counter >= self._window_size
    
    ##############################################

    def reset(self):

        self._window_index = 0
        self._window_counter = 0
        self._window_points[...] = 0 # fixme: required ???

    ##############################################

    def send(self, point):

        self._window_points[self._window_index] = point
        self._window_index = (self._window_index + 1) % self._window_size
        self._window_counter += 1

    ##############################################

    @property
    def value(self):

        if bool(self):
            return np.rint(np.mean(self._window_points, axis=0))
        else:
            return None

####################################################################################################

class SketcherState(object):

    ##############################################

    def __init__(self):

        self.pencil_size = 1
        self.eraser_size = 1
        self.pencil_colour = (255, 255, 255)
        self.previous_position = None
        
####################################################################################################

class PathSketcher(object):

    _logger = _module_logger.getChild('PathSketcher')
    
    ##############################################
    
    def __init__(self, sketcher_state, page, painter):

        self._sketcher_state = sketcher_state

        self._page = page
        self._painter = painter
        
        self._current_path = None
        self._point_filter = PointFilter(window_size=10)
        
    ##############################################

    @property
    def state(self):
        return self._sketcher_state

    ##############################################

    def _start_path(self):

        self._current_path = DynamicPath(self._sketcher_state.pencil_colour,
                                         self._sketcher_state.pencil_size)
        self._point_filter.reset()

    ##############################################

    def _end_path(self):

        path = self._current_path.to_path()
        path = path.backward_smooth_window(radius=3)
        # path = path.simplify(tolerance=1)
        self._page.add_path(path)
        self._current_path = None

        return path
        
    ##############################################

    def on_tablet_event(self, tablet_event):

        if tablet_event.pointer_type == TabletPointerType.pen:
            return self.on_pen_event(tablet_event)
        elif tablet_event.pointer_type == TabletPointerType.eraser:
            return self.on_eraser_event(tablet_event)
        
    ##############################################

    def on_pen_event(self, tablet_event):

        self._logger.info(str(tablet_event))

        modified = False
        if tablet_event.type == TabletEventType.move:
            self._point_filter.send(tablet_event.position)
            position = self._point_filter.value
            # if position is None:
            #     self._logger.warning('Not ready')
            if position is not None and self._sketcher_state.previous_position is not None:
                previous_position = self._sketcher_state.previous_position
                distance = np.sum((position - previous_position)**2) # _square
                if distance > 1:
                    self._current_path.add_point(position)
                    self._painter.update_current_path(self._current_path.to_path())
                    modified = True # Fixme: modified signal ?
                    self._sketcher_state.previous_position = position
        else:
            position = tablet_event.position
            if tablet_event.type == TabletEventType.press:
                self._start_path()
                self._point_filter.send(position)
                self._current_path.add_point(position)
            elif tablet_event.type == TabletEventType.release:
                # add point ?
                path = self._end_path()
                self._painter.reset_current_path()
                self._painter.add_path(path)
                modified = True
            self._sketcher_state.previous_position = position

        self._painter.enable()
            
        return modified

    ##############################################

    def on_eraser_event(self, tablet_event):

        self._logger.info("")

        modified = False

        radius = self._sketcher_state.eraser_size
        position = tablet_event.position
        erased_paths = []
        for path in self._page.paths:
        #for path in hits:
            subpaths = path.erase(position, radius)
            if subpaths is not None:
                self._logger.info("Erase path {}".format(path.id))
                erased_paths.append((path, subpaths))
        for path, subpaths in erased_paths:
            self._page.remove_path(path)
            self._painter.remove_path(path)
            self._page.add_paths(subpaths)
            for subpath in subpaths:
                # subpath._colour = (255, 0, 0)
                self._painter.add_path(subpath)
                
        modified = bool(erased_paths)
            
        return modified

####################################################################################################

class ImageSketcher(ObjectWithTimeStamp):

    _logger = _module_logger.getChild('ImageSketcher')
    
    ##############################################
    
    def __init__(self, image_format, sketcher_state, painter):

        ObjectWithTimeStamp.__init__(self)

        self._image = Image(image_format)
        self._image.clear()
        
    ##############################################

    @property
    def image(self):
        return self._image
    
    ##############################################

    def to_cv_point(self, point):

        return (int(point[0]), int(point[1]))
        
    ##############################################

    def draw_line(self, point1, point2, colour=None, pencil_size=None):

        if colour is None:
            colour = self._sketcher_state.pencil_colour
        if pencil_size is None:
            pencil_size = self._sketcher_state.pencil_size
        
        cv2.line(self._image, self.to_cv_point(point1), self.to_cv_point(point2),
                 colour, pencil_size, 16)
        self.modified()
    
####################################################################################################
#
# End
#
####################################################################################################
