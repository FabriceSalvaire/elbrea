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

class Path(object):

    __path_id__ = 0
    
    ##############################################

    def __init__(self, colour, pencil_size, array_size=500):

        self._path_id = self.__path_id__
        self.__path_id__ += 1
        
        self._colour = colour
        self._pencil_size = pencil_size
        self._arrays = []
        self._array_size = array_size
        self._number_of_points = 0
        self._capacity = 0
        self._index = 0
        self._interval = None
        
    ##############################################

    @property
    def colour(self):
        return self._colour

    @property
    def pencil_size(self):
        return self._pencil_size

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

    def save(self, group, name):

        dataset = group.create_dataset(name, data=self.flatten(),
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
        obj = Path(colour, pencil_size)
        obj._arrays = [np.array(dataset)]
        obj._number_of_points = dataset.shape[0]
        obj._capacity = obj._number_of_points
        obj._index = obj._number_of_points

        return obj

    ##############################################

    def iter_on_segments(self):

        number_of_yielded_points = 0
        for k, points in enumerate(self._arrays):
            number_of_points = min(points.shape[0], self._number_of_points - number_of_yielded_points)
            if k and number_of_points:
                yield self.arrays[k-1][-1], self.arrays[k][0]
            for i in range(number_of_points -1):
                yield points[i], points[i+1]
            number_of_yielded_points += number_of_points
                
    ##############################################

    def erase(self, point, radius):

        radius_square = radius**2
        for points in self._arrays:
            print(np.where((points - point)**2 < radius_square))
            
####################################################################################################

class Sketcher(ObjectWithTimeStamp):

    _logger = _module_logger.getChild('sketcher')
    
    ##############################################
    
    def __init__(self, image_format, sketcher_state):

        ObjectWithTimeStamp.__init__(self)

        self._image = Image(image_format)
        self._image.clear()
        
        self._sketcher_state = sketcher_state

        self._paths = []

        self._window_size = 10
        self._window_points = None
        self._window_counter = 0
        self._window_index = 0
        
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

    def _add_path(self):

        self._paths.append(Path(self._sketcher_state.pencil_colour, self._sketcher_state.pencil_size))

        self._window_points = np.zeros((self._window_size, 2), dtype=np.uint64)
        # self._window_points[0] = tablet_event.position
        self._window_index = 0
        self._window_counter = 0
        
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
            position = tablet_event.position
            self._window_points[self._window_index] = position
            self._window_index = (self._window_index + 1) % self._window_size
            self._window_counter += 1
            if (self._sketcher_state.previous_position is not None and
                self._window_counter >= self._window_size):
                previous_position = self._sketcher_state.previous_position
                position = np.mean(self._window_points, axis=0)
                delta = position - previous_position
                distance = np.sqrt(np.sum(delta**2))
                if distance > 1:
                    if not self._paths[-1].same_sketcher_state(self._sketcher_state):
                        self._add_path()
                    self._paths[-1].add_point(position)
                    self.draw_line(previous_position, position)
                    modified = True # Fixme: modified signal ?
                    self._sketcher_state.previous_position = position
        else:
            if tablet_event.type == TabletEventType.press:
                self._add_path()
            self._sketcher_state.previous_position = tablet_event.position
            
        return modified

    ##############################################

    def on_eraser_event(self, tablet_event):

        self._logger.info("")

        modified = False

        for path in self._paths:
            path.erase(tablet_event.position, radius=self._sketcher_state.pencil_size)
        
        return modified
    
    ##############################################

    def save(self, group):

        for i, path in enumerate(self._paths):
            path.save(group, 'path-{}'.format(i))

    ##############################################

    def from_hdf5(self, group):

        for name in group:
            path = Path.from_hdf5(group, name)
            for point1, point2 in path.iter_on_segments():
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
