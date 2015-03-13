####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

###################################################################################################

import logging
import os

####################################################################################################

from .Page import Page
from Elbrea.GUI.Base.GuiApplicationBase import GuiApplicationBase

####################################################################################################

class SketcherApplication(GuiApplicationBase):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):

        super(SketcherApplication, self).__init__(args=args)
        self._logger.debug(str(args))
        
        from .SketcherMainWindow import SketcherMainWindow
        self._main_window = SketcherMainWindow()
        self._main_window.showMaximized()
        
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(SketcherApplication, self)._init_actions()

    ##############################################

    def post_init(self):

        super(SketcherApplication, self).post_init()

        journal_path = self.args.journal 
        if os.path.exists(journal_path):
            self.load(journal_path)
        else:
            self._page = Page()
        
        # for screen in self.platform.screens:
        #     print(screen)
        # dpi_x, dpi_y = self.platform.screens[0].dpi
        
        glwidget = self._main_window.glwidget

        from Elbrea.Math.Interval import IntervalInt2D
        width = height = 1000
        glwidget._image_interval = IntervalInt2D((0, width), (0, height))

        # Load registered painters
        # from Elbrea.GraphicEngine import ForegroundPainter 
        
        from Elbrea.GraphicEngine.PainterManager import BasicPainterManager
        self.painter_manager = BasicPainterManager(glwidget)

        from .PagePainter import PagePainter
        page_painter = PagePainter(self.painter_manager)

        from Elbrea.GraphicEngine.PathPainter import SegmentPainter, PathPainter
        segment_painter = SegmentPainter(self.painter_manager)
        path_painter = PathPainter(self.painter_manager)

        from .Sketcher import SketcherState, SegmentSketcher, PathSketcher
        self.sketcher_state = SketcherState()
        self._main_window.tool_bar.init_sketcher_state()
        self.segment_sketcher = SegmentSketcher(self.sketcher_state, self._page, segment_painter)
        self.path_sketcher = PathSketcher(self.sketcher_state, self._page, path_painter)

        # Update painter
        for path in self._page.paths:
            path_painter.add_path(path)
            
        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()
        
    ##############################################

    def save(self, journal_path=None):

        self._logger.info("")

        if journal_path is None:
            journal_path = self.args.journal

        from .Importer.Hdf import HdfWriter
        hdf_writer = HdfWriter(journal_path)
        hdf_writer.save_page(self._page)
        
    ##############################################

    def load(self, journal_path):

        if not  os.path.exists(journal_path):
            raise NameError()    
        
        from .Importer.Hdf import HdfImporter
        hdf_importer = HdfImporter(journal_path)
        self._page = hdf_importer.read_page('page')
            
####################################################################################################
#
# End
#
####################################################################################################
