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

import rtree

from PyQt5 import QtWidgets

####################################################################################################

from Elbrea.Image.Image import Image
from Elbrea.Math.Interval import IntervalInt, IntervalInt2D, Interval2D
from Elbrea.Tools.EnumFactory import EnumFactory
from Elbrea.Tools.TimeStamp import ObjectWithTimeStamp

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SketcherState(object):

    ##############################################

    def __init__(self):

        self.pencil_size = 1
        self.eraser_size = 1
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

    ##############################################

    def __repr__(self):

        return "type {} pointer type {}".format(self.type, self.pointer_type)
    
####################################################################################################

class PathBase(object):

    __path_id__ = 0
    
    ##############################################

    def __init__(self, colour, pencil_size, path_id=None):

        if path_id is None:
            self._path_id = self.__path_id__
            PathBase.__path_id__ += 1
        else:
            self._path_id = path_id
        
        self._colour = colour
        self._pencil_size = pencil_size
        self._interval = None

    ##############################################

    @property
    def id(self):
        return self._path_id
    
    @property
    def colour(self):
        return self._colour

    @property
    def pencil_size(self):
        return self._pencil_size

####################################################################################################

class Path(PathBase):

    _logger = _module_logger.getChild('Path')
    
    ##############################################

    def __init__(self, colour, pencil_size, points, path_id=None, index_interval=None):

        super(Path, self).__init__(colour, pencil_size, path_id)

        if points.shape[1] <= 1:
            raise ValueError("Require at least two points")
        
        self._points = points
        # self._interval = self._compute_interval()

        self.index_interval = None
        # if index_interval is None:
        #     self.index_interval = IntervalInt(0, self.number_of_points -1)
        # else:
        #     self.index_interval = index_interval

    ##############################################

    def _compute_interval(self):

        lower = np.min(self._points, axis=1)
        upper = np.max(self._points, axis=1)
        # Fixme: int or float
        return Interval2D((lower[0], upper[0]), (lower[1], upper[1]))
            
    ##############################################

    @property
    def points(self):
        return self._points

    @property
    def number_of_points(self):
        return self._points.shape[0]
    
    @property
    def indexes(self):
        return np.arange(self.number_of_points)
    
    @property
    def x(self):
        return self.points[:,0]

    @property
    def y(self):
        return self.points[:,1]
    
    @property
    def p0(self):
        return self.points[0]

    @property
    def p1(self):
        return self.points[-1]

    @property
    def p10(self):
        return self.p1 - self.p0
    
    @property
    def u10(self):
        p10 = self.p10
        # print(self.p0, self.p1, str(self.index_interval))
        u10 = p10 / np.sqrt(p10[0]**2 + p10[1]**2) # srqt(x.x) # np.sum(p10**2, axis=1)
        return u10

    @property
    def interval(self):
        return self._interval
    
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

    def farthest_point(self, tolerance=1):

        # distance to chord
        # A x B = sin * |A| * |B|
        # A x u = sin * |A|
        # sin = d / |A|
        # d = (P - P0) x u 
        delta = self.points - self.p0
        distance = np.abs(np.cross(delta, self.u10))
        i_max = np.argmax(distance)
        distance_max = distance[i_max]
        if distance_max > tolerance:
            return i_max
        else:
            return None

    ##############################################

    def nearest_point(self, point):

        p0 = self.points[:-1]
        p1 = self.points[1:]
        p10 = p1 - p0
        u10 = p10 / np.sqrt(np.sum(p10**2, axis=0))

        delta = point - p0
        # projection = np.dot(delta, u10)
        projection = delta[:,0]*u10[:,0] + delta[:,1]*u10[:,1]
        indexes = np.where(np.logical_and(0 <= projection, projection < 1))[0]
        # print(indexes)
        if indexes.shape[0]:
            distance = np.abs(np.cross(delta[indexes], u10[indexes]))
            i_min = np.argmin(distance)
            # print(indexes, projection[indexes], distance)
            # print(i_min, indexes[i_min], distance[i_min])
            return indexes[i_min], distance[i_min]
        else:
            return None, None
        
        # distance = np.sum((self.points - point)**2, axis=1)
        # i_min = np.argmin(distance)
        # return i_min, distance[i_min]
        
    ##############################################
        
    def subpath(self, lower=0, upper=None):

        # global_lower = self.index_interval.inf + lower
        # if upper is None:
        #     stop = None
        #     global_upper = self.index_interval.inf + self.number_of_points -1
        # else:
        #     stop = upper + 1
        #     global_upper = self.index_interval.inf + upper

        # return self.__class__(self._colour, self._pencil_size,
        #                       self.points[lower:stop],
        #                       index_interval=IntervalInt(global_lower, global_upper))

        if upper is None:
            stop = None
        else:
            stop = upper + 1
        points = self.points[lower:stop]
            
        if points.shape[1] > 1:
            return self.__class__(self._colour, self._pencil_size, points)
        else:
            # raise
            return None
        
    ##############################################

    def simplify(self, tolerance=1):

        # Fixme: check interval
        
        queue = [self]
        farthest_points = [0]
        while queue:
            path = queue.pop()
            # print('\nsubpath', str(path.index_interval))
            farthest_point = path.farthest_point(tolerance)
            if farthest_point is not None:
                global_farthest_point = path.index_interval.inf + farthest_point
                # print('farthest point in', str(path.index_interval), global_farthest_point, path.points[farthest_point])
                farthest_points.append(global_farthest_point)
                queue.append(path.subpath(lower=farthest_point))
                queue.append(path.subpath(upper=farthest_point))
        farthest_points.append(self.number_of_points -1)
        farthest_points.sort()
        points = self.points[farthest_points]
        
        return self.__class__(self._colour, self._pencil_size, points)

    ##############################################

    def pair_iterator(self):

        for i in range(self.number_of_points -1):
            yield self.points[i], self.points[i+1]

    ##############################################
            
    @staticmethod
    def segment_intersection(point0, vector10, point2, point3):

        # p + t*r = q + u*s    x s
        #   t * (r x s) = (q - p) x s
        #   t = (q − p) × s / (r × s)
        # p + t*r = q + u*s    x r
        #   u = (q − p) × r / (r × s)
        
        vector32 = point3 - point2
        denominator = np.cross(vector10, vector32)
        if denominator == 0: # parallel
            # if np.cross(vector20, vector10) == 0:
            # check if overlapping
            #  0 ≤ (q − p) · r ≤ r · r or 0 ≤ (p − q) · s ≤ s · s
            return None
        else:
            vector20 = point2 - point0
            t = np.cross(vector20, vector32) / denominator
            u = np.cross(vector20, vector10) / denominator
            if 0 <= t <= 1 and 0 <= u <= 1:
                return point0 + vector10 * t
            else:
                return None

    ##############################################

    def find_self_intersection(self):

        intersections = []
        for i, points01 in enumerate(self.pair_iterator()):
            for j, points23 in enumerate(self.pair_iterator()):
                if i != j and j > i + 1:
                    point0, point1 = points01
                    point2, point3 = points23
                    vector10 = point1 - point0
                    intersection = self.segment_intersection(point0, vector10, point2, point3)
                    if intersection is not None:
                        # print(i, j, intersection)
                        intersections.append((i, j, intersection))
        return intersections

    ##############################################

    def smooth_window(self, radius=2):

        window_size = 2*radius + 1
        if window_size >= self.number_of_points:
            raise ValueError()

        if radius > 0:
            points = np.array(self.points, dtype=np.float) # int64
            view = points[radius:-radius]
            for i in range(1, radius +1):
                upper = -radius + i
                if upper == 0:
                    upper = None
                view += self.points[radius-i:-radius-i]
                view += self.points[radius+i:upper]
            view /= window_size
            # for i in range(1, radius +1):
            #     points[:radius] += self.points[i:radius+i]
            #     points[-radius:] += self.points[-radius-i:-i]
            # points[:radius] /= radius + 1
            # points[-radius:] /= radius + 1
            # points[radius-1] = np.mean(self.points[:radius], axis=0)
            # points[-radius] = np.mean(self.points[-radius:], axis=0)
            # return self.__class__(points[radius-1:-radius+1])
            return self.__class__(self._colour, self._pencil_size, view)
        elif radius < 0:
            raise ValueError()
        else:
            return self

    ##############################################

    def backward_smooth_window(self, radius=2):

        # limite the rate of points: average last N points
        
        window_size = radius + 1
        if window_size >= self.number_of_points:
            raise ValueError()

        if radius > 0:
            points = np.array(self.points, dtype=np.float) # int64
            view = points[radius:]
            for i in range(1, radius +1):
                view += self.points[radius-i:-i]
            view /= window_size
            return self.__class__(self._colour, self._pencil_size, view)
        elif radius < 0:
            raise ValueError()
        else:
            return self

    ##############################################

    def erase(self, point, radius):

        i_min, distance = self.nearest_point(point)
        # print(distance)
        # Fixme: check distance, path removed (only a point)
        if i_min is not None and distance <= radius:
            if i_min == 0:
                return (self.subpath(lower=1),)
            elif i_min == self.number_of_points -1:
                return (self.subpath(upper=i_min -1),)
            else:
                # Fixme: check before
                return [subpath for subpath in (self.subpath(upper=i_min-1),
                                                self.subpath(lower=i_min+1))
                        if subpath is not None]
        else:
            return None
        
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

        # Fixme: self._interval
        return Path(self._colour, self._pencil_size, self.flatten(), self._path_id)

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

class Sketcher(ObjectWithTimeStamp):

    _logger = _module_logger.getChild('sketcher')
    
    ##############################################
    
    def __init__(self, image_format, sketcher_state, painter):

        ObjectWithTimeStamp.__init__(self)

        # Fixme:
        if image_format is not None:
            self._image = Image(image_format)
            self._image.clear()
        else:
            self._iamge = None
        
        self._sketcher_state = sketcher_state

        self._painter = painter
        
        self._current_path = None
        self._paths = {}
        self._rtree = rtree.index.Index()
        
        self._point_filter = PointFilter(window_size=10)
        
    ##############################################

    @property
    def image(self):
        return self._image

    @property
    def state(self):
        return self._sketcher_state
    
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
        path = path.backward_smooth_window(radius=3)
        # path = path.simplify(tolerance=1)
        self._paths[path.id] = path
        # self._rtree.add(path.id, path.interval.bounding_box(), obj=path)
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
                    # self.draw_line(previous_position, position)
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
        # Fixme: cost ?
        # lower_position = position - radius
        # upper_position = position + radius
        erased_paths = []
        # hits = self._rtree.intersection((position[0] - radius, position[1] - radius,
        #                                  position[0] + radius, position[1] + radius),
        #                                 objects='raw')
        for path in self._paths.values():
        #for path in hits:
            subpaths = path.erase(position, radius)
            if subpaths is not None:
                self._logger.info("Erase path {}".format(path.id))
                erased_paths.append((path, subpaths))
        for path, subpaths in erased_paths:
            del self._paths[path.id]
            # self._rtree.delete(path.id, path.interval.bounding_box())
            self._painter.remove_path(path)
            self._paths.update({subpath.id:subpath for subpath in subpaths})
            for subpath in subpaths:
                # subpath._colour = (255, 0, 0)
                self._painter.add_path(subpath)
                # self._rtree.add(subpath.id, subpath.interval.bounding_box(), obj=subpath)
                
        modified = bool(erased_paths)
            
        return modified
    
    ##############################################

    def save(self, group):

        for i, path in enumerate(self._paths.values()):
            path.save(group, 'path-{}'.format(i))

    ##############################################

    def from_hdf5(self, group):

        for name in group:
            path = Path.from_hdf5(group, name)
            # for point1, point2 in path.pair_iterator():
            #     self.draw_line(point1, point2, path.colour, path.pencil_size)
            self._paths[path.id] = path
            self._painter.add_path(path)
            
####################################################################################################
#
# End
#
####################################################################################################
