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

        # for screen in self.platform.screens:
        #     print(screen)
        # dpi_x, dpi_y = self.platform.screens[0].dpi
        
        journal_path = self.args.journal 
        if os.path.exists(journal_path):
            pages = self.load_journal(journal_path)
        else:
            pages = None
        from .PageManager import PageManager
        self.page_manager = PageManager(self, pages)
        self._main_window.sketcher_tool_bar.init_sketcher_state()

        glwidget = self._main_window.glwidget
        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()
        
    ##############################################

    def load_journal(self, journal_path):

        if not os.path.exists(journal_path):
            raise NameError()    
        
        from .Importer.Hdf import HdfImporter
        return HdfImporter(journal_path).read_pages()
       
    ##############################################

    def save(self, journal_path=None):

        if journal_path is None:
            journal_path = self.args.journal

        from .Importer.Hdf import HdfWriter
        HdfWriter(journal_path).save_pages(self.page_manager.pages)
    
    ##############################################

    def refresh(self):

        self._main_window.glwidget.update()
    
####################################################################################################
#
# End
#
####################################################################################################
