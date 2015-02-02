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

        input_ = self.front_pipeline.input_filter.get_primary_output()

        from PyOpenGLng.Tools.Interval import IntervalInt2D
        image_format = input_.image_format
        print(image_format)
        glwidget._image_interval = IntervalInt2D((0, image_format.width), (0, image_format.height))

        from Elbrea.GraphicEngine.PainterManager import PainterManager
        self.painter_manager = PainterManager(glwidget)

        background_painter = self.painter_manager.background_painter
        from Elbrea.GraphicEngine import ShaderProgrames as ShaderProgrames
        shader_manager = ShaderProgrames.shader_manager
        background_painter.shader_program = shader_manager.texture_shader_program
        background_painter.source = input_

        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()

####################################################################################################
#
# End
#
####################################################################################################
