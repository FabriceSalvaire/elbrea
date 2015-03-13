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

        from .Page import Page
        self._page = Page()
        
        from .Sketcher import SketcherState, SegmentSketcher, PathSketcher
        self.sketcher_state = SketcherState()
        self._main_window.tool_bar.init_sketcher_state()
        self.segment_sketcher = SegmentSketcher(self.sketcher_state, self._page, segment_painter)
        self.path_sketcher = PathSketcher(self.sketcher_state, self._page, path_painter)
        
        self.load(self.args.journal)

        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()
        
    ##############################################

    def save(self, journal_path=None):

        self._logger.info("")

        if journal_path is None:
            journal_path = self.args.journal
            
        # Fixme:
        from Elbrea.Viewer.HdfAnnotation import HdfAnnotation
        hdf_annotation = HdfAnnotation(journal_path, update=True)
        group = hdf_annotation.create_group('page')
        self._page.save(group)

    ##############################################

    def load(self, journal_path):

        from Elbrea.Viewer.HdfAnnotation import HdfAnnotation
        if os.path.exists(journal_path):
            hdf_annotation = HdfAnnotation(journal_path, update=False) # rewrite
            self._page.from_hdf5(hdf_annotation['page'])
            path_painter = self.painter_manager['path']
            for path in self._page.paths:
                path_painter.add_path(path)
            
####################################################################################################
#
# End
#
####################################################################################################
