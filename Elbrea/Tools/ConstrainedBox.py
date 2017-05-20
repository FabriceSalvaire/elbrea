####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

from Elbrea.Math.Interval import IntervalInt2D

####################################################################################################

class ConstrainedValue(object):

    ##############################################
    
    def __init__(self, value=None, constrained=False):

        self._value = value
        self.constrained = constrained

    ##############################################
        
    def __bool__(self):

        return self.constrained

    ##############################################
        
    def _get_value(self):

        return self._value

    ##############################################
    
    def _set_value(self, value):

        if self.constrained:
            raise NameError("Value is constrained")
        else:
            self._value = value

    value = property(_get_value, _set_value)

####################################################################################################

class ConstrainedPoint(object):

    ##############################################

    def __init__(self, x=None, y=None):

        self._x, self._y = [ConstrainedValue(value=z, constrained=(z is not None))
                            for z in (x, y)]
        self._number_of_constrains =  bool(self._x) + bool(self._y)

    ##############################################

    @property
    def number_of_constrains(self):

        return self._number_of_constrains

    ##############################################

    @property
    def number_of_free_parameters(self):

        return 2 - self._number_of_constrains

    ##############################################

    @property
    def x(self):
        return self._x.value

    @x.setter
    def x(self, value):
        self._x.value = value

    ##############################################

    @property
    def y(self):
        return self._y.value

    @y.setter
    def y(self, value):
        self._y.value = value

    ##############################################

    def set_point(self, x, y):

        if not self._x:
            self._x.value = x
        if not self._y:
            self._y.value = y

####################################################################################################

class ConstrainedBox(object):

    ##############################################

    def __init__(self, x1=None, y1=None, x2=None, y2=None):

        self._p1 = ConstrainedPoint(x1, y1)
        self._p2 = ConstrainedPoint(x2, y2)
        self._number_of_constrains = self._p1.number_of_constrains + self._p2.number_of_constrains

    ##############################################

    @property
    def number_of_constrains(self):

        return self._number_of_constrains

    ##############################################

    @property
    def number_of_free_parameters(self):

        return 4 - self._number_of_constrains

    ##############################################

    def set_p1(self, x, y):

        self._p1.set_point(x, y)

    ##############################################

    def set_p2(self, x, y):

        self._p2.set_point(x, y)

    ##############################################

    @property
    def interval(self):

        return IntervalInt2D(sorted((self._p1.x, self._p2.x)),
                             sorted((self._p1.y, self._p2.y)))

    ##############################################

    @property
    def size(self):

        return self.interval.size()

####################################################################################################
#
#
#
####################################################################################################
