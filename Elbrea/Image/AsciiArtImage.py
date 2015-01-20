####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

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
