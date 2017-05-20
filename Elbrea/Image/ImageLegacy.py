####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import hashlib

import numpy as np

####################################################################################################

from Elbrea.Math.Functions import rint

####################################################################################################

class ImageFormat(object):

    ##############################################

    def __init__(self, shape, data_type):

        self._height, self._width = shape
        self._data_type = data_type

        self._size = self._height * self._width * np.nbytes[self._data_type]

    ##############################################

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def shape(self):
        return (self._height, self._width)

    @property
    def dimension(self):
        return (self._width, self._height)

    @property
    def data_type(self):
        return self._data_type

    @property
    def gray_data_format(self):
        return self.data_type_to_gray_format(self._data_type)

    @property
    def size(self):
        return self._size

    ##############################################

    @classmethod
    def pixel_depth_to_data_type(self, pixel_depth):

        if pixel_depth == 8:
            return np.uint8
        elif pixel_depth == 16:
            return np.uint16
        else:
            raise NotImplementedError

    ##############################################

    @classmethod
    def data_type_to_gray_format(self, data_type):

        if data_type == np.uint16:
            return 'gray16'
        elif data_type == np.uint8:
            return 'gray8'
        else:
            raise NotImplementedError

    ##############################################

    @classmethod
    def dimension_to_shape(self, dimension):

        """ Convert dimension to shape and vice versa """

        if len(dimension) == 2:
            return list(reversed(dimension))
        else:
            return ValueError

####################################################################################################

class Image(object):

    #######################################

    @staticmethod
    def get_format(samples_per_pixel, bits_per_pixel):

        """ Return format string from *samples_per_pixel* and *bits_per_pixel*.
        """

        if samples_per_pixel == 1 and bits_per_pixel == 8:
            return 'gray8'
        elif samples_per_pixel == 1 and bits_per_pixel == 16:
            return 'gray16'
        elif samples_per_pixel == 3 and bits_per_pixel == 8:
            return 'rgb8'
        elif samples_per_pixel == 3 and bits_per_pixel == 16:
            return 'rgb16'
        else:
            return None

    #######################################

    @staticmethod
    def format_to_dtype(format):

        if format == 'gray8':
            dtype = np.uint8
        elif format == 'gray16':
            dtype = np.uint16
        elif format == 'rgb8':
            dtype = np.uint8
        elif format == 'rgb16':
            dtype = np.uint16
        else:
            raise NameError('Image format %s is not supported' % (format))

        return dtype

    #######################################
    
    def __init__(self, format, width, height, is_planar=True):

        if not (width and height):
            raise ValueError('Wrong image size %i x %i' % (width, height))
        self.height = height
        self.width = width

        dtype = self._init_from_format(format, is_planar)

        self.size = self._compute_size()
        self.intensity_max = 2**self.bits_per_pixel -1

        self.buffer = np.zeros(self.size, dtype=dtype)
        self.size_byte = self.buffer.nbytes
        self.reshape()

    #######################################
    
    def _init_from_format(self, format, is_planar):

        self.format = format
        self.is_planar = is_planar

        # Fixme: enum w<<16+b
        if format == 'gray8':
            dtype = np.uint8
            self.bits_per_pixel = 8
            self.samples_per_pixel = 1
            # interleaved makes no sense
            self.is_planar = True

        elif format == 'gray16':
            dtype = np.uint16
            self.bits_per_pixel = 16
            self.samples_per_pixel = 1
            # interleaved makes no sense
            self.is_planar = True

        elif format == 'rgb8':
            dtype = np.uint8
            self.bits_per_pixel = 8
            self.samples_per_pixel = 3

        elif format == 'rgb16':
            dtype = np.uint16
            self.bits_per_pixel = 16
            self.samples_per_pixel = 3

        else:
            raise NameError('Image format %s is not supported' % (format))

        return dtype

    #######################################

    def _compute_size(self):

        """ Return the size in pixels. """

        return self.width * self.height * self.samples_per_pixel

    #######################################
    
    def copy_image_format(self, format=None, width=None, height=None, is_planar=None):

        """ Make a clone of the image using its format and size. The *format* could be specified as
        argument.
        """

        if format is None:
            format = self.format
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if is_planar is None:
            is_planar = self.is_planar

        return self.__class__(format, width, height, is_planar)

    #######################################
    
    def copy(self):

        """ Make a copy of the image. """

        image = self.copy_image_format()
        image.buffer = self.buffer.copy()

        return image

    #######################################

    def dtype(self):

        """ Return the data type. """

        return self.buffer.dtype

    #######################################
        
    def print_object(self):

        message = """
width x height   %u x %u
sample per pixel %u
bit per sample   %u
is planar        %s
""" 
        print(message % (self.width, self.height,
                         self.samples_per_pixel,
                         self.bits_per_pixel,
                         self.is_planar))

    #######################################

    def reshape_to_linear(self):

        """ Reshape the buffer to a linear shape. """

        self.buffer.shape = self.size

    #######################################

    def planar_shape(self, array):

        """ Reshape the buffer to a planar 3D shape [*samples_per_pixel*, *height*, *width*]. If
        *samples_per_pixel* is equal to one then this dimension is omitted.
        """

        if self.samples_per_pixel > 1:
            array.shape = self.samples_per_pixel, self.height, self.width
        else:
            array.shape = self.height, self.width

    #######################################

    def planar_shape_2d(self, array):

        """ Reshape the buffer to a planar 2D shape [*samples_per_pixel* * *height*, *width*].
        """

        array.shape = self.samples_per_pixel * self.height, self.width

    #######################################

    def interleaved_shape(self, array):

        """ Reshape the buffer to an interleaved 3D shape [*height*, *width*, *samples_per_pixel*].
        """

        if self.samples_per_pixel > 1:
            array.shape = self.height, self.width, self.samples_per_pixel
        else:
            array.shape = self.height, self.width

    #######################################

    def interleaved_shape_2d(self, array):

        """ Reshape the buffer to an interleaved 2D shape [*height*, *samples_per_pixel* * *width*].
        """

        array.shape = self.height, self.samples_per_pixel * self.width 

    #######################################

    def reshape(self):

        """ Reshape the buffer to its normal (3D) shape. """

        if self.is_planar:
            self.planar_shape(self.buffer)
        else:
            self.interleaved_shape(self.buffer)

    #######################################

    def reshape2d(self):

        """ Reshape the buffer to its normal 2D shape. """

        if self.is_planar:
            self.planar_shape_2d(self.buffer)
        else:
            self.interleaved_shape_2d(self.buffer)

    #######################################

    def planar_to_interleaved(self):

        """ Convert a planar image to an interleaved image. """

        if self.is_planar:

            self.reshape2d()

            if self.format == 'rgb8':
                ImageProcessing.planar_to_interleaved_uint8(self.buffer)
            else:
                raise NotImplementedError

            self.is_planar = False
            self.reshape()

    #######################################

    def interleaved_to_planar(self):

        """ Convert an interleaved image to a planar image. """

        if not self.is_planar:

            self.is_planar = True
            self.interleaved_shape_2d(self.buffer)

            if self.format == 'rgb8':
                ImageProcessing.interleaved_to_planar_uint8(self.buffer)
            else:
                raise NotImplementedError

            self.reshape()

    #######################################

    def channel(self, channel):
        """ Return an :class:`ImageChannelView` instance for the *channel*. """
        return ImageChannelView(self, channel)

    def gray_channel(self):
        """ Return an :class:`ImageChannelView` instance for the gray channel (0). """
        return self.channel(0)

    def red_channel(self):
        """ Return an :class:`ImageChannelView` instance for the red channel (0). """
        return self.channel(0)

    def green_channel(self):
        """ Return an :class:`ImageChannelView` instance for the green channel (1). """
        return self.channel(1)

    def blue_channel(self):
        """ Return an :class:`ImageChannelView` instance for the blue channel (2). """
        return self.channel(2)

    #######################################
        
    def extract_channel(self, channel):

        if self.format not in ('rgb8', 'rgb16'):
            raise NameError('extract_channel: format %s is not supported' % (self.format))
        if not self.is_planar:
            raise NameError('extract_channel: image must be planar')

        channel_image = self.__class__(format='gray8', width=self.width, height=self.height, is_planar=True)
        channel_view = self.channel(channel)
        channel_view.copy_to(channel_image)

        return channel_image

    #######################################

    # Fixme cf. supra, cf. LabelDetector

    def copy_with_two_intervals(self, interval_dst, interval_src, image):

        """ Set the *interval_dst* region of *image* with the content from the *interval_src* region
        of :obj:`self`.
        """

        dst = self.buffer[interval_dst.y.inf:interval_dst.y.sup +1,
                          interval_dst.x.inf:interval_dst.x.sup +1]

        src = image.buffer[interval_src.y.inf:interval_src.y.sup +1,
                           interval_src.x.inf:interval_src.x.sup +1]

        dst[...] = src[...]

    #######################################

    def md5(self):

        """ Return the MD5 checksum of the image. """

        return hashlib.md5(self.buffer.tostring()).hexdigest()

    #######################################

    def image_to_histogram(self, histogram, protected=True):

        # Fixme: histogram check

        """ Fill an histogram with the image content. *histogram* must be compatible with a Numpy 1D
        array of data type unsigned int 64-bit.

        If *protected* is :obj:`True`, then the histogram has an overflow bin.  Thus for the
        unprotected mode the number of bins must be greather then the maximum intensity.
        """

        if self.buffer.dtype == np.uint8:
            function = ImageProcessing.image_to_histogram_uint8
        elif self.buffer.dtype == np.uint16:
            function = ImageProcessing.image_to_histogram_uint16
        else:
            raise ValueError
        self.reshape_to_linear()
        function(self.buffer, histogram, protected)
        self.reshape()

    #######################################

    def get_stat_in_roi(self, interval):

        """ Return the mean and standard deviation in the *interval* region. Only the format
        samples_per_pixel = 1 is supported.
        """

        if self.samples_per_pixel != 1:
            raise NotImplementedError

        view = self.buffer[interval.y.inf:interval.y.sup +1,
                           interval.x.inf:interval.x.sup +1]

        return np.mean(view), np.std(view)

    #######################################

    def flip_horizontally(self):

        """ Flip horizontalaly the image. """

        self.buffer = np.fliplr(self.buffer)

    #######################################

    def flip_vertically(self):

        """ Flip vertically the image. """

        self.buffer = np.flipud(self.buffer)

    #######################################

    def rotate90(self):

        """ Rotate the image of 90 degrees. """

        # numpy.rot90(m, k=1)

        self.width, self.height = self.height, self.width

        src_buffer = self.buffer
        dst_buffer = self.buffer = np.zeros((self.height, self.width), dtype=src_buffer.dtype)

        if self.buffer.dtype == np.uint8:
            function = ImageProcessing.rotate90_uint8
        elif self.buffer.dtype == np.uint16:
            function = ImageProcessing.rotate90_uint16
        else:
            raise ValueError
        function(src_buffer, dst_buffer)

    #######################################

    def rebin(self, bin_size):

        """ Return a rebined image. """

        if self.format not in ('gray8', 'gray16'):
            raise NameError('rebin: format %s is not supported' % (self.format))

        # Fixme: bin_size must be multiple
        width = self.width / bin_size
        height = self.height / bin_size
        dst_image = self.copy_image_format(width=width, height=height)

        # Fixme: use slot [dtype][func_name]
        dtype = self.buffer.dtype
        if dtype == np.uint8:
            function = ImageProcessing.rebin_uint8
        elif dtype == np.uint16:
            function = ImageProcessing.rebin_uint16
        else:
            raise NotImplementedError
        function(self.buffer, dst_image.buffer)

        return dst_image

    #######################################
    
    def scale(self, factor=1):

        """ Scale the image pixel by a *factor*. """

        self.buffer *= factor

    #######################################

    def remap_intensity_range(self, lower_intensity, upper_intensity, dtype):

        """ Remap the intensities in the [*lower_intensity*, *upper_intensity*] range and change the
        data type to *dtype*.
        """

        if self.buffer.dtype == np.uint8:
            function = ImageProcessing.remap_intensity_range_uint8
            depth = 8
        elif self.buffer.dtype == np.uint16:
            function = ImageProcessing.remap_intensity_range_uint16
            if dtype == np.uint16:
                depth = 16
            elif dtype == np.uint8:
                depth = 8
            else:
                raise NameError('remap_intensity_range: wrong dtype')
        else:
            raise ValueError

        dst_upper_intensity = 2**depth -1
        self.reshape_to_linear()
        function(self.buffer, lower_intensity, upper_intensity, dst_upper_intensity)
        self.reshape()

    #######################################

    # Fixme: not here

    def generate_binary(self, threshold, value_factor=1):

        r""" Binarise the image.

        .. math::

          dst = \begin{cases}
            \text{value factor} * \text{intensity max} & \text{if } src \geq \text{ threshold} \\
            0 &
          \end{cases}

        Return an new instance and the percentage of pixel on.
        """

        # np.array(np.where(data > threshold, value, 0))

        binary_image = self.copy_image_format()

        if value_factor < 1:
            value = rint(value_factor*self.intensity_max)
        else:
            value = self.intensity_max

        self.reshape_to_linear()
        binary_image.reshape_to_linear()

        if self.buffer.dtype == np.uint8:
            function = ImageProcessing.make_binary_uint8
        elif self.buffer.dtype == np.uint16:
            function = ImageProcessing.make_binary_uint16
        else:
            raise ValueError
        number_of_pixels_true = function(self.buffer, binary_image.buffer, threshold, value)

        percent_of_pixels_true = 100. * number_of_pixels_true / float(self.size)

        self.reshape()
        binary_image.reshape()

        return binary_image, percent_of_pixels_true

####################################################################################################

# Fixme: improve

class ImageChannelView(object):

    #######################################

    def __init__(self, image, channel):

        """ Create a view on the *channel* of *image*. The image must be planar.

        If the source is *uint16* and the destination is *uint8* data type, then the integers are trunked.
        """

        if not image.is_planar:
            raise NameError('Image has interleaved format')

        if channel < 0 and channel > image.samples_per_pixel:
            raise IndexError

        self.image = image
        self.channel = channel

        if image.samples_per_pixel == 1:
            self.view = image.buffer[...]
        else:
            self.view = image.buffer[channel, ...]

    #######################################

    def copy_from(self, image):

        # Used in WaveMixer.merge_wave_images

        """ Set the channel view with the *image* content. """

        self.view[...] = image.buffer[...]

    #######################################

    def copy_to(self, image):

        # unused

        """ Set the *image* with the channel view content. """

        image.buffer[...] = self.view[...]

    #######################################

    def copy_with_interval(self, interval, image):

        # unused

        """ Set the channel view *interval* region with the *image* content. """

        self.view[interval.y.inf:interval.y.sup +1,
                  interval.x.inf:interval.x.sup +1] = image.buffer[...]

    #######################################

    def copy_with_two_intervals(self, interval_dst, interval_src, image):

        # used by MosaicPixels.crop

        """ Set the *interval_dst* region of the channel view with the content from the *interval_src* region
        of *image*.
        """

        dst = self.view[interval_dst.y.inf:interval_dst.y.sup +1,
                        interval_dst.x.inf:interval_dst.x.sup +1]

        src = image.buffer[interval_src.y.inf:interval_src.y.sup +1,
                           interval_src.x.inf:interval_src.x.sup +1]

        dst[...] = src[...]

    #######################################
        
##  Fixme: Don't work with View
#
#   def copy_and_remap_with_two_intervals(self, interval_dst, interval_src, image,
#                                          lower_intensity, upper_intensity, range):
# 
#       # Fixme: duplicated code
# 
#       dst = self.view[interval_dst.y.inf:interval_dst.y.sup +1,
#                       interval_dst.x.inf:interval_dst.x.sup +1]
# 
#       src = image.buffer[interval_src.y.inf:interval_src.y.sup +1,
#                          interval_src.x.inf:interval_src.x.sup +1]
# 
#
#       ImageProcessing.remap_intensity_range_uint16_to_8(src, dst, lower_intensity, upper_intensity, range)

####################################################################################################
#
# End
#
####################################################################################################
