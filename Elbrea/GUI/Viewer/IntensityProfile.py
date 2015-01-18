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

import h5py
import numpy as np

####################################################################################################

class IntensityProfileHdf(object):

    ##############################################
        
    def __init__(self, file_name, update=False):

        """ Open an HDF5 file in append mode
        """

        if update:
            # Fixme: check
            mode = 'a'
        else:
            mode = 'r'

        self._hdf_file = h5py.File(file_name, mode)

    ##############################################

    @property
    def root(self):
        return self._hdf_file['/']

    ##############################################

    def __getitem__(self, path):
        return self._hdf_file[path]

    ##############################################
        
    def create_group(self, name):

        return self._hdf_file.create_group(name)

####################################################################################################

class IntensityProfileBase(object):

    ##############################################

    def __iter__(self):

        for colour in xrange(self.number_of_colours):
            yield self[colour]

    ##############################################

    @staticmethod
    def back_profile(y_input):

        x = 0
        yc = 0
        x_output = [x]
        y_output = [yc]
        for y in y_input:
            if y != yc:
                x_output.append(x)
                y_output.append(yc)
                x_output.append(x)
                y_output.append(y)
                yc = y
            x += 1
        if yc != 0:
            x_output.append(x)
            y_output.append(yc)
        x_output.append(x)
        y_output.append(0)

        return x_output, y_output

    ##############################################

    def create_dataset(self, group, name, comment):

        dataset = group.create_dataset(name, data=self._array, shuffle=True, compression='lzf')

        attributes = dataset.attrs
        if comment is not None:
            attributes['comment'] = unicode(comment)

        return attributes

####################################################################################################

class LineIntensityProfile(IntensityProfileBase):

    ##############################################

    def __init__(self, location, axis, number_of_colours, number_of_points):

        if axis not in ('x', 'y'):
            raise ValueError('Wrong axis')

        self._location = location
        self._axis = axis

        self._array = self._create_array(number_of_colours, number_of_points)

    ##############################################

    def _create_array(self, number_of_colours, number_of_points):

        return np.zeros((number_of_colours, number_of_points), dtype=np.uint16)

    ##############################################

    @property
    def location(self):
        return self._location

    ##############################################

    @property
    def abscissa(self):
        if self._axis == 'x':
            return self._location[0]
        else:
            return self._location[1]

    ##############################################

    @property
    def axis(self):
        return self._axis

    ##############################################

    @property
    def number_of_colours(self):
        return self._array.shape[0]

    ##############################################

    @property
    def number_of_points(self):
        return self._array.shape[1]

    ##############################################

    def __getitem__(self, colour):

        return self._array[colour]

    ##############################################

    def __setitem__(self, colour, value):

        self._array[colour] = value

    ##############################################

    def save(self, group, name=None, comment=None):

        attributes = self.create_dataset(group, name, comment)
        attributes['location'] = self._location
        attributes['axis'] = self._axis

    ##############################################

    @staticmethod
    def from_hdf5(group, name):

        raise NotImplementedError

####################################################################################################
# 
# End
# 
####################################################################################################
