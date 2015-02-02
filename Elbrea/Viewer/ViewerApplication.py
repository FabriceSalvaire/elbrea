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

        front_input = self.front_pipeline.input_filter.get_primary_output()
        back_input = self.back_pipeline.input_filter.get_primary_output()

        from PyOpenGLng.Tools.Interval import IntervalInt2D
        image_format = front_input.image_format
        print(image_format)
        glwidget._image_interval = IntervalInt2D((0, image_format.width), (0, image_format.height))

        from Elbrea.GraphicEngine.PainterManager import PainterManager
        self.painter_manager = PainterManager(glwidget)

        from Elbrea.GraphicEngine.TexturePainter import TexturePainter
        from Elbrea.GraphicEngine import ShaderProgrames as ShaderProgrames
        shader_manager = ShaderProgrames.shader_manager

        background_painter = TexturePainter(self.painter_manager)
        self.painter_manager._background_painters['front'] = background_painter
        background_painter.shader_program = shader_manager.texture_shader_program
        background_painter.source = front_input
        background_painter.enable()

        background_painter = TexturePainter(self.painter_manager)
        self.painter_manager._background_painters['back'] = background_painter
        background_painter.shader_program = shader_manager.texture_shader_program
        background_painter.source = back_input
        background_painter.disable()

        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()

    ##############################################

    def switch_front_back(self):

        self._logger.info('')

        self.painter_manager.background_painter('front').switch()
        self.painter_manager.background_painter('back').switch()
        self._main_window.glwidget.update()        

        # if self.painter_manager['front']:
        #     self.painter_manager.background_painter('front').disable()
        #     self.painter_manager.background_painter('back').enable()
        # else:
        #     self.painter_manager.background_painter('front').enable()
        #     self.painter_manager.background_painter('back').disable()

####################################################################################################
#
# End
#
####################################################################################################
