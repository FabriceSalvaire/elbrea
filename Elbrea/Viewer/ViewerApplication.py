####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

###################################################################################################

import logging

####################################################################################################

from Elbrea.GUI.Base.GuiApplicationBase import GuiApplicationBase

####################################################################################################

class ViewerApplication(GuiApplicationBase):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):


        super(ViewerApplication, self).__init__(args=args)
        self._logger.debug(str(args))
        
        from .ViewerMainWindow import ViewerMainWindow
        self._main_window = ViewerMainWindow()
        self._main_window.showMaximized()
        
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(ViewerApplication, self)._init_actions()

    ##############################################

    def post_init(self):

        super(ViewerApplication, self).post_init()

        from .ImageProcessingPipeline import ImageProcessingPipeline
        # front_image_processing_pipeline
        self.front_pipeline = ImageProcessingPipeline(self.args.front_image)
        self.back_pipeline = ImageProcessingPipeline(self.args.back_image)

        glwidget = self._main_window.glwidget
        glwidget.init_tools() # Fixme: for shader
        glwidget.create_vertex_array_objects()
        glwidget.display_all()

####################################################################################################
#
# End
#
####################################################################################################
