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

        from PyOpenGLng.Tools.Interval import IntervalInt2D
        front_input = self.front_pipeline.input_filter.get_primary_output()
        image_format = front_input.image_format
        print(image_format)
        glwidget._image_interval = IntervalInt2D((0, image_format.width), (0, image_format.height))

        from .Sketcher import FrontBackSketcher
        self.sketcher = FrontBackSketcher(image_format)
        
        # Load Painters
        from Elbrea.GraphicEngine import ForegroundPainter 
        from Elbrea.GraphicEngine.FrontBackPainter import FrontBackPainterManager
        self.painter_manager = FrontBackPainterManager(glwidget)

        from Elbrea.GraphicEngine.FrontBackPainter import FrontBackPainter
        from Elbrea.GraphicEngine.ForegroundPainter import SketcherPainter
        painter = FrontBackPainter(self.painter_manager, 'sketcher', SketcherPainter)
        self.painter_manager.register_foreground_painter(painter)
        for painter, sketcher in ((painter.front_painter, self.sketcher.front_sketcher),
                                  (painter.back_painter, self.sketcher.back_sketcher),
                              ):
            painter.create_texture(sketcher)
        painter.enable()
        
        from Elbrea.GraphicEngine import ShaderProgrames as ShaderProgrames
        shader_manager = ShaderProgrames.shader_manager

        background_painter = self.painter_manager.background_painter.front_painter
        painter = background_painter.add_painter('raw')
        painter.shader_program = shader_manager.texture_shader_program
        front_input = self.front_pipeline.input_filter.get_primary_output()
        painter.source = front_input
        painter = background_painter.add_painter('hls')
        painter.shader_program = shader_manager.texture_shader_program
        front_input = self.front_pipeline.hls_filter.get_primary_output()
        painter.source = front_input
        painter = background_painter.add_painter('user')
        painter.shader_program = shader_manager.texture_shader_program
        # painter.shader_program = shader_manager.texture_label_shader_program
        front_input = self.front_pipeline.hls_filter.get_primary_output()
        # front_input = self.front_pipeline.user_filter.get_primary_output()
        painter.source = front_input
        background_painter.select_painter('raw')

        background_painter = self.painter_manager.background_painter.back_painter
        painter = background_painter.add_painter('raw')
        painter.shader_program = shader_manager.texture_shader_program
        back_input = self.back_pipeline.input_filter.get_primary_output()
        painter.source = back_input
        painter = background_painter.add_painter('hls')
        painter.shader_program = shader_manager.texture_shader_program
        back_input = self.back_pipeline.hls_filter.get_primary_output()
        painter.source = back_input
        # painter = background_painter.add_painter('user')
        # # painter.shader_program = shader_manager.texture_label_shader_program
        # painter.shader_program = shader_manager.texture_shader_program
        # back_input = self.back_pipeline.user_filter.get_primary_output()
        # painter.source = back_input
        background_painter.select_painter('raw')

        # glwidget.makeCurrent()
        # from PyOpenGLng.HighLevelApi.RandomTexture import GlRandomTexture
        # shader_manager.texture_label_shader_program._random_texture = GlRandomTexture(size=1000, texture_unit=1)
        # glwidget.doneCurrent()

        self.load()
        
        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()

    ##############################################

    def switch_face(self):

        self._logger.info("")

        self.painter_manager.switch_face()
        self.sketcher.switch_face()

    ##############################################

    def reload_user(self):

        self._logger.info("")

        front_input = self.front_pipeline.user_filter.generate_data()
        back_input = self.back_pipeline.user_filter.generate_data()
        front_input = self.front_pipeline.user_filter.get_primary_output().modified()
        back_input = self.back_pipeline.user_filter.get_primary_output().modified()
        self._main_window.glwidget.update()

    ##############################################

    def on_filter_changed(self, filter_name):

        self._logger.info(filter_name)

        background_painter = self.painter_manager.background_painter.front_painter
        background_painter.select_painter(filter_name)
        background_painter = self.painter_manager.background_painter.back_painter
        background_painter.select_painter(filter_name)
        self._main_window.glwidget.update()

    ##############################################

    def save(self): # get False ???

        self._logger.info("")

        from .HdfAnnotation import HdfAnnotation
        path = 'test.hdf5'
        hdf_annotation = HdfAnnotation(path, update=True)
         # Fixme: recto/verso
        group = hdf_annotation.create_group('front')
        self.sketcher.front_sketcher.save(group)
        group = hdf_annotation.create_group('back')
        self.sketcher.back_sketcher.save(group)

    ##############################################

    def load(self):

        from .HdfAnnotation import HdfAnnotation
        from .Sketcher import Path
        path = 'test.hdf5'
        if os.path.exists(path):
            hdf_annotation = HdfAnnotation(path, update=False) # rewrite
            # Fixme: recto/verso
            self.sketcher.front_sketcher.from_hdf5(hdf_annotation['front'])
            
####################################################################################################
#
# End
#
####################################################################################################
