####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

from Elbrea.Math.Interval import Interval

####################################################################################################

class MinMaxFilter(object):

    """ Track the minimum and maximum value.

    Usage::

      min_max_filter = MinMaxFilter()
      for x in iterable:
        min_max_filter.filter(x)
      print min_max_filter.min, min_max_filter.max

    """

    ##############################################

    def __init__(self):

        self._min = self._max = None
        self.filter = self._init_filter

    ##############################################

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    ##############################################

    def _init_filter(self, x):

        self._min = self._max = x
        self.filter = self._normal_filter

    ##############################################

    def _normal_filter(self, x):

        self._min = min(self._min, x)
        self._max = max(self._max, x)

####################################################################################################

class IntervalAggregator(object):

    """ Aggregate range

    Usage::

      interval_aggregator = IntervalAggregator()
      for inf, sup in iterable:
        interval_aggregator.union(inf, sup)
      print interval_aggregator()

    """

    ##############################################

    def __init__(self):

        self._interval = None
        self.union = self._init_union

    ##############################################

    def __call__(self):
        return self._interval

    ##############################################

    @property
    def inf(self):
        return self._interval.inf

    @property
    def sup(self):
        return self._interval.sup

    ##############################################

    def _init_union(self, *args):

        self._interval = Interval(*args)
        self.union = self._normal_union

    ##############################################

    def _normal_union(self, *args):

        self._interval |= Interval(*args)

####################################################################################################
#
# End
#
####################################################################################################
