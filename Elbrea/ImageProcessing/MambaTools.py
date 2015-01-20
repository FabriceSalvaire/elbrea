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

import numpy as np

from mamba import *

import cv
import cv2

####################################################################################################

def mamba2cv(image_in, image_out):

    depth = image_in.getDepth()
    if  depth == 1:
        dtype = np.bool
    elif depth == 8:
        dtype = np.uint8
    elif depth == 32:
        dtype = np.uint32
    else:
        raise NotImplementedError

    width, height = image_in.getSize()
    data = image_in.extractRaw()
    array_1d = np.fromstring(data, dtype)
    array_2d = array_1d.reshape((height, width))
    image_out[...] = array_2d[...]

####################################################################################################

def cv2mamba(image_in, image_out):

    data = image_in.tostring()
    image_out.loadRaw(data)

####################################################################################################
# 
# End
# 
####################################################################################################
