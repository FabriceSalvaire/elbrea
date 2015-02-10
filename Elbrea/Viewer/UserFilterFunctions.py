####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2015 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging
import math

####################################################################################################

import numpy as np

import cv2

from mambaIm import mamba as mb
import mambaIm.mambaComposed as mc
import mambaIm.mambaExtra as me

####################################################################################################

from Elbrea.Math.Functions import rint
import Elbrea.ImageProcessing.Core.CvTools as CvTools

####################################################################################################

_module_logger = logging.getLogger(__name__)

_module_logger.info("Load " + __name__)

####################################################################################################

def user_filter_via(image_hls_float, output_image):

    _module_logger.info("")

    height, width = image_hls_float.shape[:2]

    hue_image_float, lightness_image_float, saturation_image_float = cv2.split(image_hls_float)

    track_inf = 80. / 360
    track_sup = 170. / 360
    mask = ((hue_image_float >= track_inf) &
            (hue_image_float <= track_sup))
    mask = mask == False # cv

    mask = np.array(mask, dtype=np.uint8)
    mask *= 255
    # radius = 2
    # CvTools.morphology_erode(output_image, output_image, CvTools.ball_structuring_element(radius, radius))
    CvTools.alternate_sequential_filter(mask, mask,
                                        2,
                                        lambda radius: CvTools.ball_structuring_element(radius, radius),
                                        # lambda radius: CvTools.circular_structuring_element(radius),
                                        open_first=False)

    image8_np = mb.NumpyWrapper(height, width, 8)
    output_image_np = mb.NumpyWrapper(height, width, 8)
    image8_mb = mb.imageMb(image8_np)
    output_image_mb = mb.imageMb(output_image_np)

    binary_image_mb = mb.imageMb(width, height, 1)
    marker_mb = mb.imageMb(width, height, 1)
    distance_image32_mb = mb.imageMb(width, height, 32)
    distance_image8_mb = mb.imageMb(width, height, 8)
    watershed_image32_mb = mb.imageMb(width, height, 32)
    watershed_image8_mb = mb.imageMb(width, height, 8)

    image8_np.view[...] = mask

    # Segmentation grains with the distance function. Firstly, we compute the distance function
    # (note the edge programming)
    mb.copyBitPlane(image8_mb, 0, binary_image_mb)
    mb.computeDistance(binary_image_mb, distance_image32_mb, edge=mb.FILLED)
    
    # We verify (with computeRange) that the distance image is lower than 256
    range = mb.computeRange(distance_image32_mb)
    mb.copyBytePlane(distance_image32_mb, 0, distance_image8_mb)

    # The distance function is inverted and its valued watershed is computed
    mb.negate(distance_image8_mb, distance_image8_mb)

    # Computing a marker image
    mc.minima(distance_image8_mb, marker_mb)
    mc.dilate(marker_mb, marker_mb, 2)
    
    # Then, we compute the watershed of the inverted distance function controlled by this marker
    # set (note the number of connected components given by the labelling operator; they should
    # correspond to the number of grains)
    number_of_labels = mb.label(marker_mb, watershed_image32_mb)
    mb.watershedSegment(distance_image8_mb, watershed_image32_mb) # (grayscale, marker -> output)
    # The three first byte planes contain the actual segmentation (each region has a specific
    # label according to the original marker). The last plane represents the actual watershed
    # line (pixels set to 255).

    # We build the labelled catchment basins
    mb.copyBytePlane(watershed_image32_mb, 3, watershed_image8_mb) # copy watershed lines
    mb.negate(watershed_image8_mb, watershed_image8_mb) # black watershed lines
    mb.copyBytePlane(watershed_image32_mb, 0, output_image_mb) # copy labels
    mb.logic(output_image_mb, watershed_image8_mb, output_image_mb, 'inf') # min(labels, black watershed lines)
    
    # Then, we obtain the final (and better) result. Each grain is labelled
    mb.convert(image8_mb, watershed_image8_mb)
    # min(labels, black watershed lines, input mask)
    mb.logic(output_image_mb, watershed_image8_mb, output_image_mb, 'inf')

    output_image[...] = output_image_np.view

####################################################################################################

def user_filter(image_hls_float, output_image):

    _module_logger.info("")

    height, width = image_hls_float.shape[:2]
    height_mb = int(math.ceil(height/2.)*2)
    width_mb = int(math.ceil(width/64.)*64)

    hue_image_float, lightness_image_float, saturation_image_float = cv2.split(image_hls_float)

    track_inf = 80. / 360
    track_sup = 170. / 360
    mask = ((hue_image_float >= track_inf) &
            (hue_image_float <= track_sup))
    mask = mask == False # cv

    mask = np.array(mask, dtype=np.uint8)
    mask *= 255
    # radius = 2
    # CvTools.morphology_erode(output_image, output_image, CvTools.ball_structuring_element(radius, radius))
    CvTools.alternate_sequential_filter(mask, mask,
                                        2,
                                        lambda radius: CvTools.ball_structuring_element(radius, radius),
                                        # lambda radius: CvTools.circular_structuring_element(radius),
                                        open_first=False)
    cv2.bitwise_not(mask, mask)

    # track_image_float = hue_image_float
    track_image_float = lightness_image_float
    # track_image_float = saturation_image_float
    track_image_float *= 255
    track_image = np.array(track_image_float, dtype=np.uint8)
    cv2.bitwise_and(track_image, mask, track_image)

    filtered_image = np.array(track_image)

    # cv2.blur(track_image, (1, 10), filtered_image)

    # marker_image = np.array(track_image)
    # blob_height = 5
    # cv2.subtract(track_image, blob_height, marker_image)

    # mask_np = mb.NumpyWrapper(height, width, 8)
    # mask_np.view[...] = track_image
    # marker_np = mb.NumpyWrapper(height, width, 8)
    # marker_np.view[...] = marker_image
    # mask_mb = mb.imageMb(mask_np)
    # marker_mb = mb.imageMb(marker_np)
    # print('start build')
    # mc.geodesy.build(mask_mb, marker_mb)
    # print('end build')

    # filtered_image -= marker_np.view

    # cv2.subtract(track_image, 255, filtered_image)
    # cv2.blur(track_image, (3, 3), track_image)
    # CvTools.morphology_gradient(track_image, filtered_image, CvTools.unit_ball)
    # CvTools.morphology_close(filtered_image, filtered_image, CvTools.horizontal_structuring_element(3))
    # CvTools.morphology_close(filtered_image, filtered_image, CvTools.vertical_structuring_element(3))
    # cv2.subtract(filtered_image, 15, filtered_image)

    for i in range(3):
        output_image[:,:,i] = filtered_image #* 10
        # input_image[:,:,i] = track_image

####################################################################################################
# 
# End
# 
####################################################################################################
