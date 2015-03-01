# -*- coding: utf-8 -*-

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

from PyQt5 import QtWidgets

####################################################################################################

from Elbrea.Image.Image import Image
from Elbrea.Math.Interval import IntervalInt2D
from Elbrea.Tools.EnumFactory import EnumFactory
from Elbrea.Tools.TimeStamp import ObjectWithTimeStamp

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SketcherState(object):

    ##############################################

    def __init__(self):

        self.pencil_size = 1
        self.pencil_colour = (255, 255, 255)
        self.previous_position = None

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

####################################################################################################

class PathBase(object):

    __path_id__ = 0
    
    ##############################################

    def __init__(self, colour, pencil_size, path_id=None):

        if path_id is None:
            self._path_id = self.__path_id__
            self.__path_id__ += 1
        else:
            self._path_id = path_id
        
        self._colour = colour
        self._pencil_size = pencil_size
        self._interval = None

    ##############################################

    @property
    def colour(self):
        return self._colour

    @property
    def pencil_size(self):
        return self._pencil_size

####################################################################################################

class Path(PathBase):

    ##############################################

    def __init__(self, colour, pencil_size, points, path_id=None):

        super(Path, self).__init__(colour, pencil_size, path_id)

        self._points = points

    ##############################################

    @property
    def points(self):
        return self._points

    @property
    def number_of_points(self):
        return self._points.shape[0]
    
    ##############################################

    def save(self, group, name):

        dataset = group.create_dataset(name, data=self._points,
                                       shuffle=True, compression='lzf')
        attributes = dataset.attrs
        attributes['colour'] = self._colour
        attributes['pencil_size'] = self._pencil_size

    ##############################################

    @staticmethod
    def from_hdf5(group, name):

        dataset = group[name]
        attributes = dataset.attrs

        colour = [int(x) for x in attributes['colour']]
        pencil_size = int(attributes['pencil_size'])
        points = np.array(dataset)

        return Path(colour, pencil_size, points)

    ##############################################

    def pair_iterator(self):

        for i in range(self.number_of_points -1):
            yield self.points[i], self.points[i+1]
            
####################################################################################################

class DynamicPath(PathBase):

    ##############################################

    def __init__(self, colour, pencil_size, array_size=500):

        super(DynamicPath, self).__init__(colour, pencil_size)
        
        self._arrays = []
        self._array_size = array_size
        self._number_of_points = 0
        self._capacity = 0
        self._index = 0
        
    ##############################################

    def same_sketcher_state(self, sketcher_state):

        return (self._colour == sketcher_state.pencil_colour
                and self._pencil_size == sketcher_state.pencil_size)
    
    ##############################################    

    def _make_array(self, size):

        return np.zeros((size, 2), dtype=np.uint16)
        
    ##############################################    

    def _extend(self):

        self._arrays.append(self._make_array(self._array_size))
        self._capacity += self._array_size
        self._index = 0

    ##############################################    

    def flatten(self):

        points = self._make_array(self._number_of_points)
        lower_index = 0
        for array in self._arrays[:-1]:
            array_size = array.shape[0]
            upper_index = lower_index + array_size
            points[lower_index:upper_index] = array
            lower_index = upper_index
        last_array = self._arrays[-1]
        points[lower_index:self._number_of_points] = last_array[:self._number_of_points-lower_index]
        return points
        
    ##############################################

    def add_point(self, point):

        self._number_of_points += 1
        if self._number_of_points > self._capacity:
            self._extend()
        current_array = self._arrays[-1]
        current_array[self._index] = point
        self._index += 1
        point_interval = IntervalInt2D([point[0], point[0]], [point[1], point[1]])
        if self._interval is None:
            self._interval = point_interval
        else:
            self._interval |= point_interval

    ##############################################

    def to_path(self):

        return Path(self._colour, self._pencil_size, self.flatten(), self._path_id)


####################################################################################################

class PointFilter(object):

    ##############################################   

    def __init__(self, window_size):
        
        self._window_size = window_size
        self._window_points = np.zeros((self._window_size, 2), dtype=np.uint64)
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
            return np.mean(self._window_points, axis=0)
        else:
            return None
    
####################################################################################################

class Sketcher(ObjectWithTimeStamp):

    _logger = _module_logger.getChild('sketcher')
    
    ##############################################
    
    def __init__(self, image_format, sketcher_state):

        ObjectWithTimeStamp.__init__(self)

        self._image = Image(image_format)
        self._image.clear()
        
        self._sketcher_state = sketcher_state

        self._current_path = None
        self._paths = []

        self._point_filter = PointFilter(window_size=10)
        
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

    ##############################################

    def _start_path(self):

        self._current_path = DynamicPath(self._sketcher_state.pencil_colour,
                                         self._sketcher_state.pencil_size)
        self._point_filter.reset()

    ##############################################

    def _end_path(self):

        path = self._current_path.to_path()
        self._paths.append(path)
        self._current_path = None
    
    ##############################################

    def on_tablet_event(self, tablet_event):

        if tablet_event.pointer_type == TabletPointerType.pen:
            return self.on_pen_event(tablet_event)
        elif tablet_event.pointer_type == TabletPointerType.eraser:
            return self.on_eraser_event(tablet_event)
        
    ##############################################

    def on_pen_event(self, tablet_event):

        self._logger.info("")

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
                    # path = self._current_path
                    # if not path.same_sketcher_state(self._sketcher_state):
                    #     self._end_path()
                    #     self._start_path()
                    self._current_path.add_point(position)
                    self.draw_line(previous_position, position)
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
                self._end_path()
                application = QtWidgets.QApplication.instance()
                path_painter = application.painter_manager['path']
                path_painter.update_path(self._paths[-1])
                path_painter.enable()
                modified = True
            self._sketcher_state.previous_position = position
            
        return modified

    ##############################################

    def on_eraser_event(self, tablet_event):

        self._logger.info("")

        modified = False

        # for path in self._paths:
        #     path.erase(tablet_event.position, radius=self._sketcher_state.pencil_size)
        
        return modified
    
    ##############################################

    def save(self, group):

        for i, path in enumerate(self._paths):
            path.save(group, 'path-{}'.format(i))

    ##############################################

    def from_hdf5(self, group):

        for name in group:
            path = Path.from_hdf5(group, name)
            for point1, point2 in path.pair_iterator():
                self.draw_line(point1, point2, path.colour, path.pencil_size)
            self._paths.append(path)
            
####################################################################################################

class FrontBackSketcher(object):

    _logger = _module_logger.getChild('FrontBackSketcher')

    ##############################################
    
    def __init__(self, image_format):

        self.state = SketcherState()
        self.front_sketcher = Sketcher(image_format, self.state)
        self.back_sketcher = Sketcher(image_format, self.state)
        self._is_front = True

    ##############################################

    def switch_face(self):

        self._is_front = not self._is_front

    ##############################################

    @property
    def current_face(self):

        if self._is_front:
            return self.front_sketcher
        else:
            return self.back_sketcher

    ##############################################

    def on_tablet_event(self, tablet_event):

        return self.current_face.on_tablet_event(tablet_event)
        
####################################################################################################
#
# End
#
####################################################################################################
