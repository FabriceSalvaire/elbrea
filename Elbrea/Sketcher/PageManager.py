####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

####################################################################################################

from .Page import Pages
from .PageFormat import page_format_database

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PageData(object):

    ##############################################

    def __init__(self):

        self.paths = {} # VAO
        self.segments = {} # VAO

        # self.paths = [] # vao id
        # self.segments = [] # vao id
        
####################################################################################################

class PageManager(object):

    _logger = _module_logger.getChild('PageManager')
    
    ##############################################

    def __init__(self, application, pages=None):

        self._application = application
           
        self._page_data = {}
        
        if pages is None:
            self._pages = Pages()
            self._pages.add_page()
            load_page_data = False
        else:
            self._pages = pages
            load_page_data = True
        self._application.main_window.page_tool_bar.update_number_of_pages(self._pages.number_of_pages)
            
        self._current_page_number = None
        self._current_page = None
        self._current_page_data = None

        self._init_painters()
        if load_page_data:
            self._load_page_data()
        self.select_page(0)
        
    ##############################################

    def _init_painters(self):
    
        # Load registered painters
        # from Elbrea.GraphicEngine import ForegroundPainter 

        main_window = self._application.main_window
        glwidget = main_window.glwidget

        # for screen in self.platform.screens:
        #     print(screen)
        dpi_x, dpi_y = self._application.platform.screens[0].dpi
        dpi = min(dpi_x, dpi_y)
        from Elbrea.Math.Interval import IntervalInt2D
        page_format = self._pages.page_format
        glwidget._image_interval = IntervalInt2D((0, page_format.width_px(dpi)),
                                                 (0, page_format.height_px(dpi)))
        
        # Fixme: Basic...
        from Elbrea.GraphicEngine.PainterManager import BasicPainterManager
        self.painter_manager = BasicPainterManager(glwidget)
        
        # steered by page size and type
        from .PagePainter import PagePainter
        page_painter = PagePainter(self.painter_manager)

        from Elbrea.GraphicEngine.PathPainter import SegmentPainter, PathPainter
        self._segment_painter = SegmentPainter(self.painter_manager, self)
        self._path_painter = PathPainter(self.painter_manager, self)

        from .Sketcher import SketcherState, SegmentSketcher, PathSketcher
        self.sketcher_state = SketcherState()
        self.segment_sketcher = SegmentSketcher(self.sketcher_state, self, self._segment_painter)
        self.path_sketcher = PathSketcher(self.sketcher_state, self, self._path_painter)
       
    ##############################################

    def _load_page_data(self):

        # use lazy allocation instead ?
        path_painter = self._path_painter
        for page in self._pages:
            self._update_page_data(page)
            for path in page.paths:
                path_painter.add_path(path)

    ##############################################

    def _update_page_data(self, page):

        # lazy allocation
        if page not in self._page_data:
            self._page_data[page] = PageData()
        self._current_page_data = self._page_data[page]
                
    ##############################################

    @property
    def number_of_pages(self):
        return self._pages.number_of_pages

    @property
    def last_page_index(self):
        return self._pages.last_page_index
    
    @property
    def page(self):
        return self._current_page

    @property
    def page_data(self):
        return self._current_page_data

    @property
    def pages(self):
        return self._pages
    
    ##############################################

    def add_page(self):

        self._pages.add_page()

    ##############################################

    def select_page(self, index):

        self._current_page_number = index
        self._current_page = self._pages[index]
        self._update_page_data(self._current_page)
        self._application.refresh()

####################################################################################################
#
# End
#
####################################################################################################
