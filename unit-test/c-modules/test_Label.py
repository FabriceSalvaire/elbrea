####################################################################################################

import os
import unittest

import numpy as np

####################################################################################################

from Elbrea.Image.AsciiArtImage import ascii_art_to_image
from Elbrea.Image.Image import Image
from Elbrea.Tools.Painter import paint_ellipse
from Elbrea.Tools.Timer import Timer
import Elbrea.C.Labelling as Labelling

####################################################################################################

class TestLabel(unittest.TestCase):

    ##############################################

    # @unittest.skip('')
    def test_label(self):

        test_image_file_name = os.path.join(os.path.dirname(__file__), 'label-test-image-1.txt')
        image = ascii_art_to_image(test_image_file_name)
        image_buffer = image.buffer
        # write_from_image(image, test_image_file_name.replace('.txt', '.tiff'))
        
        labeler = Labelling.Label(0, * image.buffer.shape)
        labeler.run_length_encode(image.buffer)
        # labeler.print_segments()
        # labeler.print_row_map()
        labeler.merge_segments()
        # labeler.print_segments()
        labeler.generate_islands(image.buffer)

        labelled_image = image.copy_image_format()
        labeler.make_label_image(labelled_image.buffer)
        # write_from_image(labelled_image, test_image_file_name.replace('.txt', '-label.tiff'))

        colour_label_image = image.copy_image_format(format='rgb8', is_planar=False)
        labeler.make_colour_image(colour_label_image.buffer)
        # write_from_image(colour_label_image, test_image_file_name.replace('.txt', '-colour-label.tiff'))

        labels = {}
        total_number_of_pixels = 0
        label_max = image_buffer.max()
        for label in range(label_max +1):
            if not label:
                continue
            indices = np.where(image_buffer == label)
            number_of_pixels = (indices[0]).size
            if number_of_pixels:
                labels[label] = {'number_of_pixels':number_of_pixels}
                total_number_of_pixels += number_of_pixels
        # print 'Label max', label_max
        # print 'Number of labels', len(labels)
        # print 'Number of pixels', total_number_of_pixels
        # print 'Labels:', labels

        # label 0 = sea
        self.assertEqual(len(labels), labeler.islands.size() -1)
        for label in range(1, labeler.islands.size()):
            cpp_island = labeler.islands[label]
            cpp_island.analyse(1)
            self.assertEqual(label, cpp_island.label)
            self.assertEqual(cpp_island.intensity_min, cpp_island.intensity_max)
            self.assertEqual(labels[cpp_island.intensity_min]['number_of_pixels'], cpp_island.number_of_pixels)
            # print cpp_island.print_object()

    ##############################################

    @unittest.skip('')
    def test_label_perf(self):

        test_image_file_name = os.path.join(os.path.dirname(__file__), 'label-test-perf-image-1.txt')
        number_of_labels_per_template = 7
        
        template = ascii_art_to_image(test_image_file_name).buffer
        template_height, template_width = template.shape
        height_scale_factor, width_scale_factor = 100, 50
        image = Image(format='gray16',
                      height=template_height*height_scale_factor,
                      width=template_width*width_scale_factor)
        for r in range(height_scale_factor):
            for c in range(width_scale_factor):
                r_min = r*template_height
                r_max = r_min + template_height
                c_min = c*template_width
                c_max = c_min + template_width
                image.buffer[r_min:r_max,c_min:c_max] = template
        # # write_from_image(image, test_image_file_name.replace('.txt', '.tiff'))

        print('\nStart Perf Loop ...')
        timer = Timer()
        for i in range(50):
            labeler = Labelling.Label(0, * image.buffer.shape)
            labeler.run_length_encode(image.buffer)
            labeler.merge_segments()
            labeler.generate_islands(image.buffer)
        print('Perf Loop Done')
        timer.print_delta_time()
            
        # labelled_image = image.copy_image_format()
        # labeler.make_label_image(labelled_image.buffer)
        # # write_from_image(labelled_image, test_image_file_name.replace('.txt', '-label.tiff'))

        colour_label_image = image.copy_image_format(format='rgb8', is_planar=False)
        labeler.make_colour_image(colour_label_image.buffer)
        # write_from_image(colour_label_image, test_image_file_name.replace('.txt', '-colour-label.tiff'))

        self.assertEqual(labeler.islands.size() -1,
                         number_of_labels_per_template*height_scale_factor*width_scale_factor)

    ##############################################

    # @unittest.skip('')
    def test_island(self):

        image = Image(format='gray16', width=1000, height=1000)

        def paint_pixel(x, y):
            image.buffer[y, x] = intensity_level

        island_definitions = (
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

        island_map = {}
        for island_parameters in island_definitions:
            island_map[island_parameters['intensity_level']] = island_parameters
            intensity_level = island_parameters['intensity_level']
            paint_ellipse(xm=island_parameters['cm_r'],
                          ym=island_parameters['cm_c'],
                          a=island_parameters['a'],
                          b=island_parameters['b'],
                          angle=island_parameters['angle'],
                          paint_pixel=paint_pixel, fill=True)
        
        test_image_file_name = 'test-island-image.tiff'
        # write_from_image(image, test_image_file_name)

        labeler = Labelling.Label(0, * image.buffer.shape)
        labeler.run_length_encode(image.buffer)
        labeler.merge_segments()
        labeler.generate_islands(image.buffer)

        colour_label_image = image.copy_image_format(format='rgb8', is_planar=False)
        labeler.make_colour_image(colour_label_image.buffer)
        # write_from_image(colour_label_image, test_image_file_name.replace('.tiff', '-colour-label.tiff'))

        # label 0 = sea
        self.assertEqual(labeler.islands.size() -1, 4)
        for label in range(1, labeler.islands.size()):
            cpp_island = labeler.islands[label]
            cpp_island.analyse(1)
            print(cpp_island.print_object())
            island_parameters = island_map[cpp_island.intensity_min]

            self.assertEqual(cpp_island.intensity_min, cpp_island.intensity_max)
            self.assertEqual(cpp_island.intensity_min, island_parameters['intensity_level'])

            # Fixme: check r/c inversion
            self.assertAlmostEqual(cpp_island.cm_r_weighted, island_parameters['cm_c'], places=1)
            self.assertAlmostEqual(cpp_island.cm_c_weighted, island_parameters['cm_r'], places=1)
            self.assertAlmostEqual(cpp_island.cm_r_unweighted, island_parameters['cm_c'], places=1)
            self.assertAlmostEqual(cpp_island.cm_c_unweighted, island_parameters['cm_r'], places=1)

            angle = island_parameters['angle']
            # Fixme
            if angle == 90:
                angle = -angle
            self.assertAlmostEqual(cpp_island.major_axis_angle_weighted, angle, delta=1.)
            self.assertAlmostEqual(cpp_island.major_axis_angle_unweighted, angle, delta=1.)

            def check_length(ref_value, test_value):
                print('Check Length: %.3f versus %.3f' % (ref_value, test_value))
                ref_value, test_value = [.1*x for x in (ref_value, test_value)]
                self.assertAlmostEqual(ref_value, test_value, places=0)
                
            check_length(cpp_island.major_axis_weighted, 2*island_parameters['a'])
            check_length(cpp_island.minor_axis_weighted, 2*island_parameters['b'])
        
####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
