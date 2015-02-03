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

        # front_input = self.front_pipeline.input_filter.get_primary_output()
        # back_input = self.back_pipeline.input_filter.get_primary_output()
        # front_input = self.front_pipeline.hls_filter.get_primary_output()
        # back_input = self.back_pipeline.hls_filter.get_primary_output()
        front_input = self.front_pipeline.user_filter.get_primary_output()
        back_input = self.back_pipeline.user_filter.get_primary_output()

        from PyOpenGLng.Tools.Interval import IntervalInt2D
        image_format = front_input.image_format
        print(image_format)
        glwidget._image_interval = IntervalInt2D((0, image_format.width), (0, image_format.height))

        from Elbrea.GraphicEngine.PainterManager import PainterManager
        self.painter_manager = PainterManager(glwidget)

        from Elbrea.GraphicEngine import ShaderProgrames as ShaderProgrames
        shader_manager = ShaderProgrames.shader_manager

        background_painter = self.painter_manager.background_painter 

        painter = background_painter.add_painter('front')
        painter.shader_program = shader_manager.texture_shader_program
        painter.source = front_input

        painter = background_painter.add_painter('back')
        painter.shader_program = shader_manager.texture_shader_program
        painter.source = back_input

        background_painter.select_painter('front')
        background_painter.enable()

        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()

    ##############################################

    def switch_front_back(self):

        self._logger.info("")

        background_painter = self.painter_manager.background_painter
        if background_painter.current_painter_name == 'front':
            source = 'back'
        else:
            source = 'front'
        background_painter.select_painter(source)
        self._main_window.glwidget.update()        

    ##############################################

    def reload_user(self):

        self._logger.info("")

        front_input = self.front_pipeline.user_filter.generate_data()
        back_input = self.back_pipeline.user_filter.generate_data()
        front_input = self.front_pipeline.user_filter.get_primary_output().modified()
        back_input = self.back_pipeline.user_filter.get_primary_output().modified()
        self._main_window.glwidget.update()
        
####################################################################################################
#
# End
#
####################################################################################################
