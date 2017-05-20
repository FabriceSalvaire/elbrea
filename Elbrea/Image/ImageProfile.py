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

from Elbrea.Math.Functions import sign

####################################################################################################

class ImageProfile(object):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, image):

        self._image = image
        self._slope_sign = None

    ##############################################

    @property
    def slope_sign(self):
        return self._slope_sign

    ##############################################

    def profile(self, location1, location2, radius):

        c1, r1 = location1
        c2, r2 = location2

        delta_r = r2 - r1
        delta_c = c2 - c1

        if not (abs(delta_r) <= abs(delta_c)): # /!\
            return None

        self._slope_sign = sign(delta_r) 
        if self._slope_sign == 0:
            r_slices = self._r_slices_for_null_slope(c1, c2, r1, radius)
            self._slope_sign = 0
        elif self._slope_sign > 0:
            r_slices = self._r_slices_for_positive_slope(c1, c2, r1, r2, radius)
        else:
            r_slices = self._r_slices_for_negative_slope(c1, c2, r1, r2, radius)

        number_of_points = abs(delta_c) +1
        # data_type = self._image.dtype()
        data_type = np.float
        means = np.zeros(number_of_points, dtype=data_type)
        squares = np.zeros(number_of_points, dtype=data_type)
        counts = np.zeros(number_of_points, dtype=data_type)
        for r_slice in r_slices:
            r, cs1, cs2 = r_slice
            cm1 = cs1 - c1
            cm2 = cs2 - c1
            values = self._image.buffer[r,cs1:cs2 +1]
            means[cm1:cm2 +1] += values
            squares[cm1:cm2 +1] += values**2
            counts[cm1:cm2 +1] += 1
        means /= counts
        # generate nan !
        sigmas = np.sqrt(squares/counts - means*means)

        return means, sigmas

    ##############################################

    def bresenham(self, c1, r1, c2, r2):

        dc = c2 - c1
        ac = abs(dc) << 1
        sc = sign(dc)

        dr = r2 - r1
        ar = abs(dr) << 1
        sr = sign(dr)

        c = c1
        r = r1
        cs = []
        rs = []

        if ac > ar: # c dominant
            d = ar - (ac >> 1)
            while True:
                cs.append(c)
                rs.append(r)
                if c == c2: break
                if d >= 0:
                    r += sr
                    d -= ac
                c += sc
                d += ar

        else: # r dominant
            d = ac - (ar >> 1)
            while True:
                cs.append(c)
                rs.append(r)
                if r == r2: break
                if d >= 0:
                    c += sc
                    d -= ar
                r += sr
                d += ac

        return cs, rs

    ##############################################

    def _r_slices_for_null_slope(self, c1, c2, r, radius):

        # horizontal line

        r_slices = []
        r_start = max(0, r - radius)
        r_stop = min(self._image.height, r + radius +1)
        for r in range(r_start, r_stop):
            r_slices.append((r, c1, c2))

        return r_slices

    ##############################################

    def _bresenham_width(self, c1, c2, r1, r2, radius):

        cs, rs = self.bresenham(c1, r1, c2, r2)
        # rs_min = [max(0, r - radius )for r in rs]
        # rs_max = [min(self.height -1, r + radius) for r in rs]
        rs_min = [r - radius for r in rs]
        rs_max = [r + radius for r in rs]

        # for i in xrange(len(cs)):
        #     print "%u [ %u - %u - %u ]" % (cs[i], rs_min[i], rs[i], rs_max[i])

        return cs, rs, rs_min, rs_max

    ##############################################

    def _r_slices_for_positive_slope(self, c1, c2, r1, r2, radius):

        # r1 < r2
        cs, rs, rs_min, rs_max = self._bresenham_width(c1, c2, r1, r2, radius)

        r_slices = []
        i_start = 0
        i_stop = len(cs) -1
        r_start = max(0, r1 - radius)
        r_stop = min(self._image.height, r2 + radius +1)
        for r in range(r_start, r_stop):
            i = i_start
            cs1 = cs[i]
            while i <= i_stop and rs_min[i] <= r:
                if r == rs_max[i]:
                    i_start = i + 1
                i += 1
            cs2 = cs[i -1]
            r_slices.append((r, cs1, cs2))

        return r_slices

    ##############################################

    def _r_slices_for_negative_slope(self, c1, c2, r1, r2, radius):

        # r1 > r2

        cs, rs, rs_min, rs_max = self._bresenham_width(c1, c2, r1, r2, radius)

        r_slices = []
        i_start = len(cs) -1
        i_stop = 0
        r_start = max(0, r2 - radius)
        r_stop = min(self._image.height, r1 + radius +1)
        for r in range(r_start, r_stop):
            i = i_start
            cs2 = cs[i]
            while i >= i_stop and rs_min[i] <= r:
                if r == rs_max[i]:
                    i_start = i - 1
                i -= 1
            cs1 = cs[i +1]
            r_slices.append((r, cs1, cs2))

        return r_slices

####################################################################################################
#
#
#
####################################################################################################
