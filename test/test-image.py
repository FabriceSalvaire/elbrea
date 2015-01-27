import numpy as np
import matplotlib.pyplot as plt
import cv2

from Elbrea.Image.ImageLoader import load_image
from Elbrea.Image.Image import Image, ImageFormat

image = load_image('image-samples/front.jpg')

# print('to_normalised_float')
# float_image = image.to_normalised_float()
# print(repr(float_image))
# print(float_image)

print()
print('to_hls')
hls_image = image.convert_colour(ImageFormat.HLS)
print(hls_image.image_format)
print(hls_image[0,0])
# channel_images = hls_image.split_channels()
# print(channel_images)

def histogram_to_path(y_input):

    x = 0
    yc = 0
    x_output = []
    y_output = []
    for y in y_input:
        if y != yc:
            x_output.append(x)
            y_output.append(yc)
            x_output.append(x)
            y_output.append(y)
            yc = y
        x += 1
    if yc != 0:
        x_output.append(x)
        y_output.append(yc)
    x_output.append(x)
    y_output.append(0)

    return x_output, y_output

# hr = cv2.calcHist([image], [0], None, [256], [0, 256])
# hg = cv2.calcHist([image], [1], None, [256], [0, 256])
# hb = cv2.calcHist([image], [2], None, [256], [0, 256])
# hr = cv2.calcHist([hls_image], [0], None, [360], [0, 360])
# hg = cv2.calcHist([hls_image], [1], None, [256], [0, 1])
# hb = cv2.calcHist([hls_image], [2], None, [256], [0, 1])
for channel in range(3):
    histogram = hls_image.histogram(channel, number_of_bins=100)
    # plt.plot(histogram)
    # histogram /= image.image_format.number_of_pixels
    plt.plot(*histogram_to_path(histogram))
plt.show()

# import Elbrea.Image.Image as I
# a = I.Image(3,3)
# a.clear()
# print(a)
# a[...] = 10
# a *= 2
# print(a)
# b = a.to_normalised_float()
# # print(a)
# print(b)


