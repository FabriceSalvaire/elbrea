####################################################################################################

import numpy as np

from mambaIm.mamba import *
import mambaIm.mambaComposed as mc
import mambaIm.mambaExtra as me

import cv2

####################################################################################################

from Elbrea.Math.Functions import rint

import Elbrea.ImageProcessing.CvTools as CvTools
import Elbrea.ImageProcessing.MambaTools as MambaTools

####################################################################################################

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

        track_inf = 80.
        track_sup = 170.
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

        lightness_image_float *= 255
        lightness_image = np.array(lightness_image_float, dtype=np.uint8)
        cv2.bitwise_and(lightness_image, mask, lightness_image)

        filtered_image = np.array(lightness_image)
        # tmp_image = np.array(lightness_image)

        # marker_image = np.array(lightness_image)
        # blob_height = 50
        # cv2.subtract(lightness_image, blob_height, marker_image)

        # mask_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        # MambaTools.cv2mamba(lightness_image, mask_mb)
        # marker_mb = MambaTools.imageMb(width_mb, height_mb, 8)
        # MambaTools.cv2mamba(marker_image, marker_mb)
        # print('start build')
        # mc.geodesy.build(mask_mb, marker_mb)
        # print('end build')
        # MambaTools.mamba2cv(marker_mb, tmp_image)

        # filtered_image -= tmp_image

        for i in range(3):
            input_image[:,:,i] = filtered_image[:height,:width]
            # input_image[:,:,i] = lightness_image[:height,:width]
            
        return input_image
