####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
        
    def __nonzero__(self):

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

        self._x, self._y = [ConstrainedValue(value=x, constrained=(x is not None))
                            for x in x, y]
        self._number_of_constrains =  bool(self._x) + bool(self._y)

    ##############################################

    def number_of_constrains(self):

        return self._number_of_constrains
        
    ##############################################

    def number_of_free_parameters(self):

        return 2 - self._number_of_constrains

    ##############################################

    def _get_x(self):
        return self._x.value
    
    def _set_x(self, value):
        self._x.value = value

    x = property(_get_x, _set_x)

    ##############################################

    def _get_y(self):
        return self._y.value
    
    def _set_y(self, value):
        self._y.value = value

    y = property(_get_y, _set_y)

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
        self._number_of_constrains = self._p1.number_of_constrains() + self._p2.number_of_constrains()

    ##############################################

    def number_of_constrains(self):

        return self._number_of_constrains

    ##############################################

    def number_of_free_parameters(self):

        return 4 - self._number_of_constrains

    ##############################################

    def set_p1(self, x, y):
        
        self._p1.set_point(x, y)

    ##############################################

    def set_p2(self, x, y):
        
        self._p2.set_point(x, y)

    ##############################################

    def interval(self):

        return IntervalInt2D(sorted((self._p1.x, self._p2.x)),
                             sorted((self._p1.y, self._p2.y)))

####################################################################################################
#
#
#
####################################################################################################
