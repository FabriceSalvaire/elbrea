####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

from atomiclong import AtomicLong

####################################################################################################

class TimeStamp(object):

    _time_stamp = AtomicLong(0)

    ##############################################

    def __init__(self):

        self._modified_time = 0

    ##############################################

    def __repr__(self):
        return 'TS ' + str(self._modified_time)

    ##############################################

    def __lt__(self, other):
        return self._modified_time < other._modified_time

    ##############################################

    def __gt__(self, other):
        return self._modified_time > other._modified_time

    ##############################################

    def __int__(self):
        return self._modified_time

    ##############################################

    def modified(self):

        # Should be atomic
        TimeStamp._time_stamp += 1
        self._modified_time = TimeStamp._time_stamp.value

####################################################################################################

class ObjectWithTimeStamp(object):

     ##############################################

    def __init__(self):

        self._modified_time = TimeStamp()

    ##############################################

    @property
    def modified_time(self):
        return int(self._modified_time)

    ##############################################

    def modified(self):

        self._modified_time.modified()

####################################################################################################
# 
# End
# 
####################################################################################################
