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

###################################################################################################

import logging
import math

from PyQt5 import Qt, QtCore, QtWidgets

####################################################################################################

from Elbrea.GUI.Base.GuiApplicationBase import GuiApplicationBase

####################################################################################################

import numpy as np

from mambaIm.mamba import *
import mambaIm.mambaComposed as mc
import mambaIm.mambaExtra as me

# import cv
import cv2

####################################################################################################

from Elbrea.Math.Functions import rint

import Elbrea.ImageProcessing.CvTools as CvTools
import Elbrea.ImageProcessing.MambaTools as MambaTools

####################################################################################################

class ViewerApplication(GuiApplicationBase):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):


        super(ViewerApplication, self).__init__(args=args)
        self._logger.debug(str(args))
        
        from .ViewerMainWindow import ViewerMainWindow
        self._main_window = ViewerMainWindow()
        self._main_window.showMaximized()
        
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(ViewerApplication, self)._init_actions()

    ##############################################

    @staticmethod
    def _open_jpeg_image(path):

        image = cv2.imread(path)

        image2 = cv2.flip(image, 0)

        # cv2.mixChannels(image, image, (0, 2, 1, 1, 2, 0)) # Swap R <-> B
        image[:,:,0] = image2[:,:,2]
        image[:,:,1] = image2[:,:,1]
        image[:,:,2] = image2[:,:,0]

        return image

    ##############################################

    def post_init(self):

        super(ViewerApplication, self).post_init()

        self.front_image = self._open_jpeg_image(self.args.front_image)
        self.back_image = self._open_jpeg_image(self.args.back_image)

        # self.front_image = self.process_images(self.front_image)
        # self.back_image = self.process_images(self.back_image)
        print('ready')

        glwidget = self._main_window.glwidget
        glwidget.init_tools() # Fixme: for shader
        glwidget.create_vertex_array_objects()
        glwidget.display_all()

    ##############################################

    def process_images(self, input_image):

        height, width = input_image.shape[:2]
        height_mb = int(math.ceil(height/2.)*2)
        width_mb = int(math.ceil(width/64.)*64)

        image_float = np.array(input_image, dtype=np.float32)
        image_float /= 255.
        image_hsl_float = cv2.cvtColor(image_float, cv2.COLOR_RGB2HLS)

        hue_image_float = np.zeros((height_mb, width_mb), dtype=np.float32)
        saturation_image_float = np.zeros((height_mb, width_mb), dtype=np.float32)
        lightness_image_float = np.zeros((height_mb, width_mb), dtype=np.float32)
        hue_image_float[:height,:width] = image_hsl_float[:,:,0]
        lightness_image_float[:height,:width] = image_hsl_float[:,:,1]
        saturation_image_float[:height,:width] = image_hsl_float[:,:,2]

        track_inf = 30.
        track_sup = 170.
        high_ligth = .45
        mask = ((hue_image_float >= track_inf) &
                (hue_image_float <= track_sup) &
                (lightness_image_float < high_ligth))
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

        lightness_image_float *= 255
        lightness_image = np.array(lightness_image_float, dtype=np.uint8)
        cv2.bitwise_and(lightness_image, mask, lightness_image)

        filtered_image = np.array(lightness_image)
        tmp_image = np.array(lightness_image)

        marker_image = np.array(lightness_image)
        blob_height = 50
        cv2.subtract(lightness_image, blob_height, marker_image)

        mask_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        MambaTools.cv2mamba(lightness_image, mask_mb)
        marker_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        MambaTools.cv2mamba(marker_image, marker_mb)
        print('start build')
        mc.geodesy.build(mask_mb, marker_mb)
        print('end build')
        MambaTools.mamba2cv(marker_mb, tmp_image)

        filtered_image -= tmp_image

        for i in range(3):
            input_image[:,:,i] = filtered_image[:height,:width]
            # input_image[:,:,i] = lightness_image[:height,:width]
            
        return input_image

####################################################################################################
#
# End
#
####################################################################################################
