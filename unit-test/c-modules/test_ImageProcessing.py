####################################################################################################
####################################################################################################

import unittest

import numpy as np

####################################################################################################

from Elbrea.C.ImageProcessing import Image
import Elbrea.C.ImageProcessing as ImageProcessing

SSE_BYTE_ALIGNEMENT = 16;

####################################################################################################

INF, SUP = 0, 0xFFFF

####################################################################################################

def print_image(image, in_buffer=False, max_r=None, max_c=None, number_of_digit=1):
    if in_buffer:
        image_size = image.buffer_size()
    else:
        image_size = image.image_size()
    height = image_size.height()
    width = image_size.width()
    if (max_r is not None):
        height = min(max_r, height)
    if (max_c is not None):
        width = min(max_c, width)
    rule = '='*(width*(number_of_digit +1) -1)
    print rule
    string_format = '%' + str(number_of_digit) + 'u'
    for r in xrange(height):
        line = []
        for c in xrange(width):
            if in_buffer:
                value = image.get_in_buffer(r, c)
            else:
                value = image.get(r, c)
            if value == SUP:
                value_str = 'S'
            elif value:
                value_str = string_format % value
            else:
                value_str = ' '
            line.append(value_str)
        print ' '.join(line)
    print rule

####################################################################################################

class TestImageProcessing2(unittest.TestCase):

    ##############################################

    #@unittest.skip('')
    def test_basic(self):

        image = Image(100, 100, False)
        print 'Data Pointer:', hex(image.data_pointer_as_integer())
        print 'Image Size:', image.height(), image.width()
        self.assertFalse(image.is_data_aligned())

        image.zero()

        self.assertEqual(image.get(0, 0), 0)
        image.set_constant(4095)
        self.assertEqual(image.get(0, 0), 4095)
         
        image.set(10, 10, 10)
        self.assertEqual(image.get(10, 10), 10)
        
        # image.add_constant(100)
        # self.assertEqual(image.get(10, 10), 110)
         
        # image.scale(2)
        # self.assertEqual(image.get(10, 10), 2*(10+100))

    ##############################################

    # @unittest.skip('')
    def test_numpy_interface(self):

        np_array = np.arange(50, dtype=np.uint16)
        np_array.shape = 5, 10
        print np_array
        image = Image(np_array)
        print 'Data Pointer:', hex(image.data_pointer_as_integer())
        self.assertEqual(image.data_pointer_as_integer(), np_array.ctypes.data)
        self.assertFalse(image.is_allocated())
        self.assertEqual(image.height(), 5)
        self.assertEqual(image.width(), 10)
        self.assertEqual(image.step(), 10*2)
        print_image(image)
        for r in xrange(5):
            self.assertEqual(image.get(r, 0), r*10)
            self.assertEqual(image.get(r, 9), r*10 +9)
        image.set(1, 1, 123)
        self.assertEqual(np_array[1, 1], 123)

    ##############################################

    #@unittest.skip('')
    def test_arithmetic_operator(self):

        image_height, image_width = 32, 32 +3
        align = SSE_BYTE_ALIGNEMENT

        print 'Allocate'
        image1 = Image(image_height, image_width, align)
        print image1.is_allocated()

        print 'Set Constant'
        constant1 = 100
        image1.set_constant(constant1)

        print 'Allocate'
        image2 = Image(image_height, image_width, align)
        print image2.is_allocated()

        print 'Set Constant'
        constant2 = 200
        image2.set_constant(constant2)

        print 'Add'
        # image2.saturated_addition(image1)
        image3 = Image(image_height, image_width, align)
        ImageProcessing.saturated_addition_sse(image1, image2, image3)
        self.assertEqual(image3.get(0, 0), constant1+constant2)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
