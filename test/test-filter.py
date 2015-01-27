####################################################################################################

import Elbrea.Logging.Logging as Logging

logger = Logging.setup_logging('elbrea')

####################################################################################################

from Elbrea.ImagePipeline.ImageFilter import ImageFilter

####################################################################################################

class ImageFilterA(ImageFilter):

    __filter_name__ = 'Filter A'
    __input_names__ = ()
    __output_names__ = ('primary output',)

####################################################################################################

class ImageFilterB1(ImageFilter):

    __filter_name__ = 'Filter B1'
    __input_names__ = ('primary input',)
    __output_names__ = ('primary output',)

####################################################################################################

class ImageFilterB2(ImageFilter):

    __filter_name__ = 'Filter B2'
    __input_names__ = ('primary input',)
    __output_names__ = ('primary output',)

####################################################################################################

class ImageFilterC(ImageFilter):

    __filter_name__ = 'Filter C'
    __input_names__ = ('input1', 'input2')
    __output_names__ = ('primary output',)

####################################################################################################

filter_a = ImageFilterA()
filter_b1 = ImageFilterB1()
filter_b2 = ImageFilterB2()
filter_c = ImageFilterC()

filter_b1.connect_input('primary input', filter_a.get_primary_output())
filter_b2.connect_input('primary input', filter_a.get_primary_output())
filter_c.connect_input('input1', filter_b1.get_primary_output())
filter_c.connect_input('input2', filter_b2.get_primary_output())

filter_c.update()

print("\n", "recall") 
filter_c.update()

print("\n", "recall") 
filter_b1.modified()
filter_c.update()

####################################################################################################
# 
# End
# 
####################################################################################################
