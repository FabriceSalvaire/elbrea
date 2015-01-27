####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2015 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import unittest
import itertools

import numpy.testing as npt

####################################################################################################

from Elbrea.Image.Colour import *

####################################################################################################

class TestColour(unittest.TestCase):

    ##############################################

    def _test_rgb_to_hls(self, red, green, blue):

        print()
        rgb_colour = RgbIntColour(red, green, blue)
        rgb_normalised_colour = rgb_colour.normalise()
        hls_normalised_colour = rgb_normalised_colour.to_hls()
        rgb_normalised_colour2 = hls_normalised_colour.to_rgb()
        print(rgb_normalised_colour)
        print(hls_normalised_colour)
        print(rgb_normalised_colour2)
        npt.assert_almost_equal(rgb_normalised_colour, rgb_normalised_colour2)

    ##############################################

    def test(self):

        # for hue in range(0, 360, 120):
        #     for luminosity in range(0, 256, 64):
        #         for saturation in range(0, 256, 64):
        #             if hue and luminosity:
        #                 print()
        #                 hls_colour = HlsIntColour(hue, luminosity, saturation)
        #                 hls_normalised_colour = hls_colour.normalise()
        #                 rgb_normalised_colour = hls_normalised_colour.to_rgb()
        #                 hls_normalised_colour2 = rgb_normalised_colour.to_hls()
        #                 print(hls_normalised_colour)
        #                 print(rgb_normalised_colour)
        #                 print(hls_normalised_colour2)
        #                 npt.assert_almost_equal(hls_normalised_colour, hls_normalised_colour2)
        
        for red, green, blue in itertools.product((0, 255), repeat=3):
            self._test_rgb_to_hls(red, green, blue)

        for red in range(0, 256, 64):
            for green in range(0, 256, 64):
                for blue in range(0, 256, 64):
                    self._test_rgb_to_hls(red, green, blue)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
# 
# End
# 
####################################################################################################
