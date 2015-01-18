####################################################################################################

import unittest

import numpy as np

####################################################################################################

from Elbrea.Tools.Painter import paint_ellipse
import Elbrea.C.Labelling as Labelling

####################################################################################################

class IslandPainter(object):

    ##############################################

    def __init__(self, intensity_level, cm_r, cm_c, a, b, angle):

        self.intensity_level = intensity_level

        area = 4 * (a+1) * (b+1)
        self._pixels = np.zeros((area, 4), dtype=np.uint16)
        self.number_of_pixels = 0

        paint_ellipse(cm_r, cm_c, a, b, angle, self._paint_pixel, fill=True)

    ##############################################

    def _paint_pixel(self, x, y):
        
        self._pixels[self.number_of_pixels,:3] = (y, x, self.intensity_level)
        self.number_of_pixels += 1

    ##############################################

    def _get_pixels(self):

        return self._pixels[:self.number_of_pixels,:]

    pixels = property(_get_pixels, None, None, '')

####################################################################################################

class TestIsland(unittest.TestCase):

    ##############################################

    def test_island(self):

        island_definitions = (
            {'intensity_level':100,
            'cm_r':300,
            'cm_c':200,
            'a':10,
            'b':10,
            'angle':0,
            },
            {'intensity_level':100,
            'cm_r':300,
            'cm_c':200,
            'a':100,
            'b':10,
            'angle':0,
            },
            {'intensity_level':200,
            'cm_r':300,
            'cm_c':400,
            'a':100,
            'b':10,
            'angle':90,
            },
            {'intensity_level':300,
            'cm_r':500,
            'cm_c':400,
            'a':100,
            'b':10,
            'angle':15,
            },
            {'intensity_level':400,
            'cm_r':500,
            'cm_c':600,
            'a':100,
            'b':10,
            'angle':-15,
            },
            )

        image_index = 0
        for island_parameters in island_definitions:

            island_painter = IslandPainter(** island_parameters)
            # island = Labelling.IslandOwned(0, 1, island_painter.number_of_pixels)
            # pixels = island_painter.pixels
            # for i in xrange(island_painter.number_of_pixels):
            #     pixel = pixels[i]
            #     island.set_pixel(i, int(pixel[0]), int(pixel[1]), int(pixel[2]))
            ## island = Labelling.Island(0, 1, island_painter.pixels)

            island = Labelling.Island(0, 1, Labelling.Pixel(), 0)
            island.set_pixels(island_painter.pixels)

            island.analyse(1)

            print(island.print_object())

            if False:
                image = Image(format='gray16', width=1000, height=1000)
                island.paint(image.buffer, island_parameters['intensity_level'])
                image_index += 1
                image_file_name = 'test-image-%u.tif' % image_index
                print('Write', image_file_name)
                write_from_image(image, image_file_name)

            self.assertEqual(island.intensity_min, island.intensity_max)
            self.assertEqual(island.intensity_min, island_parameters['intensity_level'])
             
            # Fixme: check r/c inversion
            self.assertAlmostEqual(island.cm_r_weighted, island_parameters['cm_c'], places=1)
            self.assertAlmostEqual(island.cm_c_weighted, island_parameters['cm_r'], places=1)
            self.assertAlmostEqual(island.cm_r_unweighted, island_parameters['cm_c'], places=1)
            self.assertAlmostEqual(island.cm_c_unweighted, island_parameters['cm_r'], places=1)
             
            angle = island_parameters['angle']
            # Fixme
            if angle == 90:
                angle = -angle
            self.assertAlmostEqual(island.major_axis_angle_weighted, angle, delta=1.)
            self.assertAlmostEqual(island.major_axis_angle_unweighted, angle, delta=1.)
             
            def check_length(ref_value, test_value):
                print('Check Length: %.3f versus %.3f' % (ref_value, test_value))
                ref_value, test_value = [.1*x for x in (ref_value, test_value)]
                self.assertAlmostEqual(ref_value, test_value, places=0)
                
            check_length(island.major_axis_weighted, 2*island_parameters['a'])
            check_length(island.minor_axis_weighted, 2*island_parameters['b'])

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
# 
# End
# 
####################################################################################################
