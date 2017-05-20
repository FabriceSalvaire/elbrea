####################################################################################################

import h5py
import matplotlib.pylab as plt
import numpy as np

####################################################################################################

from Elbrea.Math.Interval import IntervalInt

####################################################################################################

class Path(object):

    ##############################################

    def __init__(self, points, interval=None):

        self.points = points
        if interval is None:
            self.interval = IntervalInt(0, self.number_of_points -1)
        else:
            self.interval = interval

    ##############################################

    @property
    def number_of_points(self):
        return self.points.shape[0]

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
        # print(self.p0, self.p1, str(self.interval))
        u10 = p10 / np.sqrt(p10[0]**2 + p10[1]**2) # srqt(x.x) # np.sum(p10**2, axis=1)
        return u10

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
        print(indexes)
        if indexes.shape[0]:
            distance = np.abs(np.cross(delta[indexes], u10[indexes]))
            i_min = np.argmin(distance)
            print(indexes, projection[indexes], distance)
            print(i_min, indexes[i_min], distance[i_min])
            return indexes[i_min], distance[i_min]
        else:
            return None, None

        # distance = np.sum((self.points - point)**2, axis=1)
        # i_min = np.argmin(distance)
        # return i_min, distance[i_min]
        
    ##############################################
        
    def subpath(self, lower=0, upper=None):

        global_lower = self.interval.inf + lower
        if upper is None:
            stop = None
            global_upper = self.interval.inf + self.number_of_points -1
        else:
            stop = upper + 1
            global_upper = self.interval.inf + upper

        return self.__class__(self.points[lower:stop],
                              interval=IntervalInt(global_lower, global_upper))

    ##############################################

    def simplify(self, tolerance=1):

        queue = [self]
        farthest_points = [0]
        while queue:
            path = queue.pop()
            # print('\nsubpath', str(path.interval))
            farthest_point = path.farthest_point(tolerance)
            if farthest_point is not None:
                global_farthest_point = path.interval.inf + farthest_point
                # print('farthest point in', str(path.interval), global_farthest_point, path.points[farthest_point])
                farthest_points.append(global_farthest_point)
                queue.append(path.subpath(lower=farthest_point))
                queue.append(path.subpath(upper=farthest_point))
        farthest_points.append(self.number_of_points -1)
        farthest_points.sort()
        points = self.points[farthest_points]

        return self.__class__(points)

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
                        print(i, j, intersection)
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
            return self.__class__(view)
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
            return self.__class__(view)
        elif radius < 0:
            raise ValueError()
        else:
            return self

####################################################################################################

# filename = 'curve-sample-loop.hdf5'
filename = 'curve-sample-erase.hdf5'
f = h5py.File(filename)

g = f['front']

p = np.array(g['path-0'].value, dtype=np.int64)
path0 = Path(p)
# plt.plot(path0.x, path0.y, 'o-')

p = np.array(g['path-1'].value, dtype=np.int64)
path1 = Path(p)
plt.plot(path1.x, path1.y, 'o-')
paths = [path0]
for point in path1.points:
    # i_min = path0.nearest_point(point)
    # nearest_point = path0.points[i_min]
    # plt.plot((point[0], nearest_point[0]), (point[1], nearest_point[1]), 'o-')
    new_paths = []
    for path in paths:
        i_min, distance = path.nearest_point(point)
        print(i_min, distance)
        if i_min is not None and distance <= 2:
            if i_min == 0:
                new_paths.append(path.subpath(lower=1))
            elif i_min == path.number_of_points -1:
                new_paths.append(path.subpath(upper=i_min -1))
            else:
                new_paths.append(path.subpath(upper=i_min-1))
                new_paths.append(path.subpath(lower=i_min+1))
        else:
            new_paths.append(path)
    paths = new_paths
for path in paths:
    plt.plot(path.x, path.y, '-')

####################################################################################################

# path0.points = np.arange(1, 11)
# path0_smooth = path0.smooth_window(radius=2)
# path0_smooth = path0.backward_smooth_window(radius=3)
# path0_smooth = path0_smooth.smooth_window(radius=1)
# plt.plot(path0.x, path0.y, 'o-')
# plt.plot(path0_smooth.x, path0_smooth.y, 'o-')

# simplified_path0 = path0.simplify()
# plt.plot(path0.x, path0.y, 'o-')
# plt.plot(simplified_path0.x, simplified_path0.y, 'o-')

# intersections = path0.find_self_intersection()
# plt.plot(path0.x, path0.y, 'o-')
# plt.plot([p[2][0] for p in intersections], [p[2][1] for p in intersections], 'o')

# if intersections:
#     lower = 0
#     for i, j, intersection in intersections:
#         path = path0.subpath(lower=lower, upper=i)
#         plt.plot(path.x, path.y, 'o-')
#         path = path0.subpath(lower=i, upper=j)
#         plt.plot(path.x, path.y, 'o-')
#         path = path0.subpath(lower=lower)
#         lower = j
#     path = path0.subpath(lower=lower)
#     plt.plot(path.x, path.y, 'o-')

####################################################################################################

plt.show()

####################################################################################################
# 
# End
# 
####################################################################################################
