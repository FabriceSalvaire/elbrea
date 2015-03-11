####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

import numpy as np

####################################################################################################

from Elbrea.Math.Interval import IntervalInt2D, Interval2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

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

    def __repr__(self):
        return "Path {}".format(self._path_id)    
    
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
# 
# End
# 
####################################################################################################
