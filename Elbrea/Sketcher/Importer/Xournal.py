####################################################################################################
# 
# xxx - xxx
# Copyright (C) Salvaire Fabrice 2015
# 
####################################################################################################

####################################################################################################

from io import StringIO
import base64
import gzip
import logging

import numpy as np

from lxml import etree

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class XournalImporter(object):

    # http://xournal.sourceforge.net/manual.html#file-format

    _logger = _module_logger.getChild('XournalImporter')
    
    ##############################################

    def __init__(self, file_path):
        
        # Xournal stores its data in gzipped XML-like files. The gzipped data consists of a
        # succession of XML tags describing the document. By convention, the file header and trailer
        # look like this:
        #
        # <?xml version="1.0" standalone="no"?>
        # <xournal version="...">
        # <title>...</title>
        # ... sequence of pages ...
        # </xournal>
        #
        # Dimension are expressed as floating number in points, 1/72 inch.

        xml_file = gzip.open(file_path)
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        for node in root:
            self._logger.debug(type(node), node.tag)
            if node.tag == 'title':
                self._parse_title(node)
            elif node.tag == 'page':
                self._parse_page(node)
                
    ##############################################

    def _parse_title(self, node):

        self._title = node.text
        self._logger.debug('Title: ' + self._title)
                
    ##############################################

    def _parse_page(self, page_node):

        # <page width="..." height="...">
        # ... page contents ...
        # </page>
        
        kwargs = dict(page_node.attrib)
        self._logger.debug('Page {}'.format(kwargs))
        
        for node in page_node:
            self._logger.debug(type(node), node.tag)
            if node.tag == 'background':
                self._parse_background(node)
            elif node.tag == 'layer':
                self._parse_layer(node)

    ##############################################

    def _parse_background(self, node):

        # Solid background: <background type="solid" color="..." style="..." />
        #
        # The color attribute takes one of the standard values "white", "yellow", "pink", "orange",
        # "blue", "green", or can specify a hexadecimal RGBA value in the format "#rrggbbaa". The
        # style attribute takes one of the standard values "plain", "lined", "ruled", or "graph".

        # Bitmap background: <background type="pixmap" domain="..." filename="..." />
        #
        # The domain attribute takes one of the standard values "absolute", "attach", or "clone". A
        # value of "absolute" indicates that the bitmap is found in the file specified by
        # filename. The bitmap can be in any format recognized by the gdk-pixbuf library; this
        # includes most of the common bitmap formats (JPEG, PNG, BMP, GIF, PCX, PNM, TIFF, ...).  A
        # value of "attach" indicates that the bitmap is an attachment to the Xournal file. The
        # bitmap is in PNG format, and resides in a file whose name is derived from that of the main
        # Xournal file by appending to it a dot and the contents of the filename attribute. For
        # example, if the Xournal file is in file.xoj and the filename attribute is "bg_1.png" then
        # the bitmap file is file.xoj.bg_1.png (Xournal saves attached bitmaps sequentially in files
        # ...bg_1.png, ...bg_2.png, etc.)  A value of "clone" indicates that the bitmap is identical
        # to the background of a previous page of the journal; the filename attribute then specifies
        # the page number, starting with 0 for the first page. For example, if a filename value of
        # "1" indicates that the background bitmap is identical to that of the second page.

        # PDF background: <background type="pdf" domain="..." filename="..." pageno="..." />
        #   or <background type="pdf" pageno="..." />
        #
        # The domain and filename attributes must be specified for the first page of the journal
        # that uses a PDF background, and must be omitted subsequently for every other page that
        # uses a PDF background. The domain attribute takes one of the standard values "absolute"
        # and "attach"; the PDF document is to be found in the file specified by filename (if domain
        # is "absolute"), or in the file whose name is obtained by appending a dot and the contents
        # of the filename attribute to the name of the main Xournal file (if domain is
        # "attach"). The pageno attribute specifies which page of the PDF file is used as
        # background, starting with 1 for the first page of the PDF file.
        
        kwargs = dict(node.attrib)
        self._logger.debug('Background {}'.format(kwargs))
                
    ##############################################

    def _parse_layer(self, layer_node):

        # The successive layers are listed in their stacking order, from bottom to top.
        # <layer> ... </layer>
        
        for node in layer_node:
            self._logger.debug(type(node), node.tag)
            if node.tag == 'stroke':
                self._parse_stroke(node)
            elif node.tag == 'text':
                self._parse_text(node)
            elif node.tag == 'image':
                self._parse_image(node)

    ##############################################

    def _parse_stroke(self, node):

        # <stroke tool="..." color="..." width="...">
        # ... list of coordinates ...
        # </stroke>
        #
        # The tool attribute can take the values "pen", "highlighter", or "eraser" depending on the
        # tool used to create the stroke (pen, highlighter, or whiteout eraser); a value of
        # "highlighter" indicates that the stroke should be painted in a partially transparent
        # manner (Xournal uses an alpha coefficient of 0.5).
        #
        # The color attribute can take one of the standard values "black", "blue", "red", "green",
        # "gray", "lightblue", "lightgreen", "magenta", "orange", "yellow", "white", or can specify
        # a hexadecimal RGBA value in the format "#rrggbbaa".
        #
        # The width attribute is a floating-point number or a sequence of floating-point numbers
        # starting, and specifies the width of the stroke in points. (For a variable-width stroke,
        # the width attribute contains a whitespace-separated succession of floating-point values:
        # first the nominal brush width, and then the width of each successive segment forming the
        # stroke.)
        # 
        # The list of coordinates is simply a succession of floating-point values, separated by
        # whitespace. The number of given values must be even; consecutive pairs of values give the
        # x and y coordinates of each point along the stroke. These values are expressed in
        # points. The coordinates (0,0) represent the top-left corner of the page: hence x is
        # measured from the left of the page, and y is measured from the top of the page.
        # 
        # Every stroke must contain at least two points (four floating point values). Moreover, two
        # consecutive points on the stroke should be spaced no more than 5 units apart or so; longer
        # line segments should be subdivided as appropriate (otherwise the eraser tool will not
        # interact properly with the stroke). The default precision used by Xournal for the x,y
        # coordinates is 0.01 unit (1/7200 in).
        
        kwargs = dict(node.attrib)
        points = np.loadtxt(StringIO(node.text))
        points = points.reshape(points.shape[0]//2, 2)
        self._logger.debug('Stroke {}:\n {}'.format(kwargs, points))

    ##############################################

    def _parse_text(self, node):

        # <text font="..." size="..." x="..." y="..." color="...">... text ...</text>
        #
        # The font attribute contains the font name, for example "Serif Bold Italic"; if the font is
        # not available, another font will be substituted. The size attribute specifies the font
        # size in points. The x and y attributes specify the coordinates of the top-left corner of
        # the text box in page coordinates (measured in points from the top-left corner of the
        # page). Finally, the color attribute contains either the name of a standard color or a
        # hexadecimal RGBA value (see above).
        #
        # The contents of the text are encoded in UTF-8, with the characters '&', '<', '>' replaced
        # by &amp;, &lt;, &gt;. Whitespace and linefeeds are preserved (in particular, no extraneous
        # whitespace should be inserted between the enclosing tags and the text itself).
        
        kwargs = dict(node.attrib)
        text = node.text
        self._logger.debug('Text {}:\n {}'.format(kwargs, text))

    ##############################################

    def _parse_image(self, node):

        # <image left="..." top="..." right="..." bottom="...">... data ...</image>
        # 
        # The left, top, right and bottom attributes specify the bounding box to which the image is
        # scaled, in page coordinates (measured in points from the top-left corner). The data is in
        # base64-encoded PNG format.

        kwargs = dict(node.attrib)
        decode_string = base64.decodestring(str.encode(node.text)) # PNG format
        self._logger.debug('Image {}'.format(kwargs))

####################################################################################################
# 
# End
# 
####################################################################################################
