####################################################################################################
# 
# PyOpenGLng - An OpenGL Python Wrapper with a High Level API.
# Copyright (C) 2014 Fabrice Salvaire
# 
####################################################################################################

# Note: we use functions (e.g. sin) from math module because they are faster

####################################################################################################

import math
import numpy as np

####################################################################################################

def identity():
    return np.identity(3, dtype=np.float32)

####################################################################################################

def translate(matrix, x, y):

    """ in-place translation """

    T = np.array([[1, 0, x],
                  [0, 1, y],
                  [0, 0, 1]],
                 dtype=matrix.dtype)

    matrix[...] = np.dot(T, matrix)
    return matrix

####################################################################################################

def scale(matrix, x, y):

    S = np.array([[x, 0, 0],
                  [0, y, 0],
                  [0, 0, 1]],
                 dtype=matrix.dtype)

    matrix[...] = np.dot(S, matrix)
    return matrix

####################################################################################################

def rotate(matrix, angle):

    t = math.radians(angle)
    c = math.cos(t)
    s = math.sin(t)
    R = np.array([[c, -s, 0],
                  [s,  c, 0],
                  [0,  0, 1]],
                 dtype=matrix.dtype)

    matrix[...] = np.dot(R, matrix)
    return matrix

####################################################################################################
# 
# End
# 
####################################################################################################
