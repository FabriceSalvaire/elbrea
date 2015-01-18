####################################################################################################

from Elbrea.Image.Image import Image

####################################################################################################

def ascii_art_to_image(file_name):

    ascii_code_0 = ord('0')
    ascii_code_1 = ord('1')
    ascii_code_9 = ord('9')
    ascii_code_a = ord('a')
    ascii_code_z = ord('z')
    
    with open(file_name) as f:

        lines = f.readlines()

        first_line = lines[0]
        if first_line[-2] != '|':
            raise NameError('Bad ASCII Art Image')

        image_height = len(lines)
        image_width = len(first_line) -2

        image = Image(format='gray16', width=image_width, height=image_height)
        image_buffer = image.buffer

        for r, line in enumerate(lines):
            for c, pixel in enumerate(line[:line.find('|')]):
                ascii_code = ord(pixel)
                if ascii_code_1 <= ascii_code <= ascii_code_9:
                    image_buffer[r,c] = ascii_code - ascii_code_0
                elif ascii_code_a <= ascii_code <= ascii_code_z:
                    image_buffer[r,c] = ascii_code - ascii_code_a + 10

        return image
                    
####################################################################################################
#
# End
#
####################################################################################################
