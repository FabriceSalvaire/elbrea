####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

"""
This module provides functions to paint lines, conics, spots and segments.

The *paint_pixel* argument in the followings is a functor that is called for each pixel generated
with the pixel location as argument::

      paint_pixel(x, y)
"""

####################################################################################################

__ALL__ = ['paint_line', 'paint_conic', 'generate_spot_model', 'generate_segment_model']

####################################################################################################

import math

import numpy as np
import scipy.special as sp
import numpy.random as npr

####################################################################################################

from Elbrea.Math.Functions import odd, sign

####################################################################################################

# Digital Line Drawing
# by Paul Heckbert
# from "Graphics Gems", Academic Press, 1990

# digline: draw digital line from (x1,y1) to (x2,y2), calling a user-supplied procedure at each
# pixel.  Does no clipping.  Uses Bresenham's algorithm.

# Paul Heckbert	3 Sep 85

def paint_line(x1, y1, x2, y2, paint_pixel):

    """ Paint a line between (x1, y1) and (x2, y2) using the Bresenham's algorithm.
    """

    dx = x2 - x1
    ax = abs(dx) << 1
    sx = sign(dx)

    dy = y2 - y1
    ay = abs(dy) << 1
    sy = sign(dy)

    x = x1
    y = y1

    if ax > ay: # x dominant
        d = ay - (ax >> 1)
        while True:
            paint_pixel(x, y)
            if x == x2: return
            if d >= 0:
                y += sy
                d -= ax
            x += sx
            d += ay

    else: # y dominant
        d = ax - (ay >> 1)
        while True:
            paint_pixel(x, y)
            if y == y2: return
            if d >= 0:
                x += sx
                d -= ay
            y += sy
            d += ax

####################################################################################################

def paint_simple_ellipse(cx, cy, x_radius, y_radius, paint_pixel):

    """ Paint an ellipse of center (cx, cy) and the axes (x_radius, y_radius) using a naive algorithm.
    """

    def paint_4_ellipse_points(x, y):
        paint_pixel(cx+x, cy+y)
        paint_pixel(cx-x, cy+y)
        paint_pixel(cx-x, cy-y)
        paint_pixel(cx+x, cy-y)

    two_a_square = 2*x_radius**2
    two_b_square = 2*y_radius**2

    x = x_radius
    y = 0

    x_change = y_radius**2*(1 - 2*x_radius)
    y_change = x_radius**2

    ellipse_error = 0

    stopping_x = two_b_square*x_radius
    stopping_y = 0

    while stopping_x >= stopping_y: # 1st set of points, y' > 1

        paint_4_ellipse_points(x, y)

        y += 1
        stopping_y += two_a_square
        ellipse_error += y_change
        y_change += two_a_square

        if (2*ellipse_error + x_change) > 0:
            x -= 1
            stopping_x -= two_b_square
            ellipse_error += x_change
            x_change += two_b_square

    # 1st point set is done start the 2nd set of points

    x = 0
    y = y_radius

    x_change = y_radius**2
    y_change = x_radius**2*(1 - 2*y_radius)

    ellipse_error = 0

    stopping_x = 0
    stopping_y = two_a_square*y_radius

    while stopping_x <= stopping_y: # 2nd set of points, y' < 1

        paint_4_ellipse_points(x, y)

        x += 1
        stopping_x += two_b_square
        ellipse_error += x_change
        x_change += two_b_square

        if (2*ellipse_error + y_change) > 0:
            y -= 1
            stopping_y -= two_a_square
            ellipse_error += y_change
            y_change += two_a_square

####################################################################################################
#
# CONIC 2D Bresenham-like conic drawer.
#
####################################################################################################
#
# Author: Andrew W. Fitzgibbon (andrewfg@ed.ac.uk),
#         Machine Vision Unit,
#         Dept. of Artificial Intelligence,
#         Edinburgh University,
#
# Date: 31-Mar-94
# Version 2: 6-Oct-95
#    Bugfixes from Arne Steinarson <arst@ludd.luth.se>
#
####################################################################################################

# http://research.microsoft.com/en-us/um/people/awf/graphics/bres-ellipse.html
# http://www.cit.gu.edu.au/~anthony/info/graphics/bresenham.procs
# http://www710.univ-lyon1.fr/~bouakaz/OpenCV-0.9.5/docs/ref/OpenCVRef_ImageProcessing.htm#decl_cvEllipse

####################################################################################################

conic_diagonal_move_x = [None, 1, 1, -1, -1, -1, -1,  1,  1]
conic_diagonal_move_y = [None, 1, 1,  1,  1, -1, -1, -1, -1]
conic_square_move_x   = [None, 1, 0,  0, -1, -1,  0,  0,  1]
conic_square_move_y   = [None, 0, 1,  1,  0,  0, -1, -1,  0]

####################################################################################################

def get_conic_octant(gx, gy):

    # Use gradient to identify octant.

    upper = abs(gx) > abs(gy)

    if gx >= 0: # Right-pointing
        if gy >= 0: # Up
            return 4 - upper
        else: # Down
            return 1 + upper

    else: # Left
        if gy > 0: # Up
            return 5 + upper
        else: # Down
            return 8 - upper

####################################################################################################

def paint_conic(xs, ys, xe, ye, conic_parameters, paint_pixel):

    """ Paint a conic using a Bresenham's like algorithm.

    The conic is specified by the equation:

      A x^2 + B x y + C y^2 + D x + E y + F = 0,

    The conic is drawn between the starting point (xs, ys) and the ending (xe,
    ye). *conic_parameters* is a tuple containing the parameters: A, B, C, D, E, F
    """

    A, B, C, D, E, F = conic_parameters

    DEBUG = False

    if DEBUG:
        print(conic_parameters)
        print("paint_conic %i x^2 + %i x y + %i y^2 + %i x + %i y + %i = 0" % (A, B, C, D, E, F))
        print("(%i, %i) (%i, %i)" % (xs, ys, xe, ye))
        print(A*xs**2 + B*xs*ys + C*ys**2 + D*xs + E*ys + F)

    A *= 4
    B *= 4
    C *= 4
    D *= 4
    E *= 4
    F *= 4

    # Translate start point to origin
    F = A*xs**2 + B*xs*ys + C*ys**2 + D*xs + E*ys + F
    D = D + 2*A*xs + B*ys
    E = E + B*xs + 2*C*ys

    # Starting octant number
    octant = get_conic_octant(D, E)

    # Change in (x,y) for square moves
    dx_square = conic_square_move_x[octant]
    dy_square = conic_square_move_y[octant]

    # Change in (x,y) for diagonal moves
    dx_diag = conic_diagonal_move_x[octant]
    dy_diag = conic_diagonal_move_y[octant]

    # Decisions variables and increments

    if octant == 1:
        d = A + B/2 + C/4 + D + E/2 + F
        u = A + B/2 + D
        v = u + E

    elif octant == 2:
        d = A/4 + B/2 + C + D/2 + E + F
        u = B/2 + C + E
        v = u + D

    elif octant == 3:
        d = A/4 - B/2 + C - D/2 + E + F
        u = -B/2 + C + E
        v = u - D

    elif octant == 4:
        d = A - B/2 + C/4 - D + E/2 + F
        u = A - B/2 - D
        v = u + E

    elif octant == 5:
        d = A + B/2 + C/4 - D - E/2 + F
        u = A + B/2 - D
        v = u - E

    elif octant == 6:
        d = A/4 + B/2 + C - D/2 - E + F
        u = B/2 + C - E
        v = u - D

    elif octant == 7:
        d = A/4 - B/2 + C + D/2 - E + F
        u =  -B/2 + C - E
        v = u + D

    elif octant == 8:
        d = A - B/2 + C/4 + D - E/2 + F
        u = A - B/2 + D
        v = u - E

    else:
        raise('funny octant')

    k1_sign = dy_square*dy_diag
    B_sign  = dx_diag*dy_diag

    k1 = 2 * (A + k1_sign * (C - A))
    k2 = k1 + B_sign*B
    k3 = 2 * (A + C + B_sign*B)

    # Translate (xs, ys) to origin
    x = xe - xs
    y = ye - ys

    # Gradient at endpoint
    gx = 2*A*x +   B*y + D
    gy =   B*x + 2*C*y + E

    octant_count = get_conic_octant(gx, gy) - octant

    # if octant_count < 0: octant_count += 8
    # 
    # elif octant_count == 0:
    # 
    #     if ((xs > xe and dx_diag > 0) or (ys > ye and dy_diag > 0) or
    #         (xs < xe and dx_diag < 0) or (ys < ye and dy_diag < 0)):
    #         octant_count += 8

    if octant_count <= 0:
        octant_count += 8

    if DEBUG:
        print('octant_count = %d' % (octant_count))

    # Now we actually draw the curve

    x = xs
    y = ys

    while octant_count > 0:

      if DEBUG:
          print('-- %d -------------------------' % (octant))

      if odd(octant):

          while 2*v <= k2:

              paint_pixel(x,y)

              if DEBUG:
                  print('x = %3d y = %3d d = %4d' % (x, y, d))

              # Are we inside or outside?

              if (d < 0): # Inside
                  x += dx_square
                  y += dy_square
                  u += k1
                  v += k2
                  d += u

              else: # Outside
                  x += dx_diag
                  y += dy_diag
                  u += k2
                  v += k3
                  d += v

          # We now cross the diagonal octant boundary.

          d = d - u + v/2 - k2/2 + 3*k3/8
          # error (^) in Foley and van Dam p 959, "2nd ed, revised 5th printing"
          u = -u + v - k2/2 + k3/2
          v = v - k2 + k3/2
          k1 = k1 - 2*k2 + k3
          k2 = k3 - k2

          dx_square, dy_square = -dy_square, dx_square

      else: # Octant is even

          while 2*u < k2:

              paint_pixel(x, y)

              if DEBUG:
                  print('x = %3d y = %3d d = %4d' % (x, y, d))

              # Are we inside or outside?

              if d > 0: # Outside
                  x += dx_square
                  y += dy_square
                  u += k1
                  v += k2
                  d += u

              else: # Inside
                  x += dx_diag
                  y += dy_diag
                  u += k2
                  v += k3
                  d += v

          # We now cross over square octant boundary.

          k1_minus_k2 = k1 - k2
          d = d + u - v + k1_minus_k2
          # Do v first; it depends on u.
          v = 2*u - v + k1_minus_k2
          u = u + k1_minus_k2
          k3 = k3 + 4*k1_minus_k2
          k2 = k1 + k1_minus_k2

          dx_diag, dy_diag = -dy_diag, dx_diag

      octant = (octant&7) +1
      octant_count -= 1

    # Draw final octant until we reach the endpoint

    if DEBUG:
        print('-- %d (final) -----------------' % (octant))

    if odd(octant):

        while 2*v <= k2:

          paint_pixel(x, y)

          if x == xe and y == ye:
              break

          if DEBUG:
              print('x = %3d y = %3d d = %4d' % (x, y, d))

          # if (DEBUG) fprintf(stderr,"x = %3d y = %3d d = %4d\n", x,y,d)

          # Are we inside or outside?
          if d < 0: # Inside
              x += dx_square
              y += dy_square
              u += k1
              v += k2
              d += u

          else: # outside
              x += dx_diag
              y += dy_diag
              u += k2
              v += k3
              d += v

    else: # Octant is even

        while 2*u < k2:

          paint_pixel(x, y)

          if x == xe and y == ye:
              break

          if DEBUG:
              print('x = %3d y = %3d d = %4d' % (x, y, d))

          # Are we inside or outside?

          if d > 0: # Outside
              x += dx_square
              y += dy_square
              u += k1
              v += k2
              d += u

          else: # Inside
              x += dx_diag
              y += dy_diag
              u += k2
              v += k3
              d += v

    return 1

####################################################################################################

def paint_ellipse(xm, ym, a, b, angle, paint_pixel, fill=False):

    """ Paint an ellipse using the function :func:`paint_conic`. The center is specified by (xm,
    ym), the axes by (a, b) and the major axis angle by *angle*. Set *fill* to :obj:`True` to paint
    the inner pixels.
    """

    angle = math.radians(angle)

    c, s = math.cos(angle), math.sin(angle)

    A = (b*c)**2 + (a*s)**2
    B = 2 * s*c * (b**2 - a**2)
    C = (b*s)**2 + (a*c)**2
    D = 0
    E = 0
    F = -(a*b)**2

    xp, yp = int(a*c), int(a*s)

    conic_parameters = (A, B, C, D, E, F)

    xs = []
    ys = []

    if fill:
        def local_paint_pixel (x, y):
            xs.append(x + xm)
            ys.append(y + ym)
            # paint_pixel(x + xm, y + ym)
    else:
        local_paint_pixel = lambda x, y: paint_pixel(x + xm, y + ym)

    paint_conic(xp, yp, xp, yp, conic_parameters, local_paint_pixel)

    if fill:

        n = len(xs)

        # flag to treat once a points
        v = [False]*n

        # loop over points
        for i in range(n):

            # check it was not treated
            if v[i]:
                continue

            v[i] = True

            x = xs[i]
            y_min = y_max = ys[i]

            # Find the extremas for x
            for k in range(n):
                if k != i and xs[k] == x:

                    v[k] = True

                    y = ys[k]

                    if   y < y_min: y_min = y
                    elif y > y_max: y_max = y

            # print x, y_min, y_max

            # paint the vertical line
            for y in range(y_min, y_max +1):
                paint_pixel(x, y)

####################################################################################################
#
# This code is wrong since P is not on the conic
#
# def paint_ellipse(a, b, angle, paint_pixel):
# 
#     angle = math.radians(angle)
# 
#     xp, yp =  a*math.cos(angle), a*math.sin(angle)
# 
#     xq, yq = -b*math.sin(angle), b*math.cos(angle)
# 
#     x_prod = xp*yq - xq*yp
# 
#     if x_prod != 0: # if it is zero, the points are colinear!
# 
#         if x_prod < 0:
# 
#             xp, xq = xq, xp
#             yp, yq = yq, yp
# 
#             x_prod = -x_prod
# 
#         A = yp**2 + yq**2
#         B = -2 * (xp*yp + xq*yq)
#         C = xp**2 + xq**2
#         D =  2 * yq * x_prod
#         E = -2 * xq * x_prod
#         F = 0
# 
#         conic_parameters = (A, B, C, D, E, F)
# 
#         print conic_parameters
# 
#         paint_conic(xp, yp, xp, yp, conic_parameters, paint_pixel)

####################################################################################################

def generate_spot_model(cx, cy, radius, sigma, paint_pixel):

    """ Generate a point convoluted with a Gaussian resolution.

    The center is specified by (cx, cy), the radial extension by *radius* and the Gaussian width by
    *sigma*.
    """

    model_image, cr, cc = generate_spot_model_image(radius, sigma)

    height, width = model_image.shape

    for r in range(height):
        for c in range(width):
            paint_pixel(cx - cc + c, cy - cr + r, model_image[r, c])

def generate_spot_model_image(radius, sigma):

    inverse_sigma_square = 1./sigma**2

    ymax = xmax = radius

    image = np.zeros((2*ymax +1, 2*xmax +1))

    # Fixme : Use mirroring to be faster
   
    for y in range(-ymax, ymax +1):
        for x in range(-xmax, xmax +1):

            r = x**2 + y**2

            image[ymax - y, xmax + x] = math.exp(- inverse_sigma_square * r)

    return image, ymax, xmax

####################################################################################################

def generate_segment_model(cx, cy, length, sigma, angle, paint_pixel):

    """ Generate a segment convoluted with a Gaussian resolution.

    The barycentre is specified by (cx, cy), the length by *length*, the angle to the abscissa axis
    by *angle* and the Gaussian width by *sigma*.
    """

    model_image, cr, cc = generate_segment_model_image(length, sigma, angle)

    height, width = model_image.shape

    for r in range(height):
        for c in range(width):
            paint_pixel(cx - cc + c, cy - cr + r, model_image[r, c])

def generate_segment_model_image(length, sigma, angle):

    l2 = .5 * length

    rad = math.radians(angle)

    ct = cos(rad)
    st = sin(rad)

    sqrt2_sigma = math.sqrt(2.) * sigma
    inv_sqrt2_sigma = 1. / sqrt2_sigma

    # Constant to have center = 1
    cst = .5 / sp.erf(inv_sqrt2_sigma * l2)

    number_of_sigma = 5.
    margin = round(number_of_sigma * sigma)

    xmax = int(max(round(ct      * (l2 + margin)), margin))
    ymax = int(max(round(abs(st) * (l2 + margin)), margin))

    image = np.zeros((2*ymax +1, 2*xmax +1))

    # Fixme : Use mirroring to be faster
   
    for y in range(-ymax, ymax +1):
        for x in range(-xmax, xmax +1):

            # Rotate(theta)
	    
            dxr = ct * x - st * y
            dyr = st * x + ct * y

            # On x axis : Segment * Gaussian
            
            sgx =   sp.erf(inv_sqrt2_sigma *(l2 + dxr)) \
                  + sp.erf(inv_sqrt2_sigma *(l2 - dxr))

            # On y axis : Dirac   * Gaussian
	    
            gy = math.exp(-(inv_sqrt2_sigma * dyr)**2)

            sgxy = cst * sgx * gy

            image[ymax - y, xmax + x] += sgxy

    return image, ymax, xmax

####################################################################################################
#
# End
# 
####################################################################################################
