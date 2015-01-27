####################################################################################################

from Elbrea.Image.Colour import RgbIntColour, RgbNormalisedColour, HlsNormalisedColour

####################################################################################################

rgb_colour = RgbIntColour(50, 100, 150)
hls_colour = rgb_colour.to_hls()
print(rgb_colour.normalise())
print(hls_colour)
rgb_colour2 = hls_colour.to_rgb()
print(rgb_colour2)

####################################################################################################
# 
# End
# 
####################################################################################################
