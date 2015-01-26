####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

def rgb_to_hsl(red, green, blue):

    print(red, green, blue)
    min_rgb = min(red, green, blue)
    max_rgb = max(red, green, blue)
    chroma = max_rgb - min_rgb # radius, small for grayscale
    print(max_rgb, min_rgb, chroma)

    if chroma == .0:
        hue = .0 # undefined
    elif max_rgb == red:
        hue = (green - blue) / chroma # in [-1, 1]
        if hue < 0:
            hue += 6.
    elif max_rgb == green:
        hue = (blue - red) / chroma + 2. # in [1, 3]
    elif max_rgb == blue:
        hue = (red - green) / chroma + 4. # in [3, 5]
    # hue *= 60.
    hue /= 6.
    print(hue)
    
    lightness = .5 * (max_rgb + min_rgb) # 0 means black and 1 means white
    
    if lightness == .0 or lightness == 1.:
        saturation = .0
    else:
        saturation = chroma / (1 - abs((max_rgb + min_rgb)/255 - 1))

    # if (lightness < .5)
    #   saturation = chroma / (max_rgb + min_rgb)
    # else if (lightness >= .5)
    #   saturation = chroma / (2. - (max_rgb + min_rgb))

    return hue, lightness, saturation # chroma

####################################################################################################
# 
# End
# 
####################################################################################################
