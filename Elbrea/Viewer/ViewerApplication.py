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
        
        from PyOpenGLng.Math.Interval import IntervalInt2D # duplicated
        front_input = self.front_pipeline.input_filter.get_primary_output()
        image_format = front_input.image_format # assume identical
        glwidget._image_interval = IntervalInt2D((0, image_format.width), (0, image_format.height))
        
        # Load registered painters
        from Elbrea.GraphicEngine import ForegroundPainter
        
        from Elbrea.Viewer.FrontBackPainter import FrontBackPainterManager, FrontBackPainter
        self.painter_manager = FrontBackPainterManager(glwidget)
        
        #!# from Elbrea.GraphicEngine.PathPainter import PathPainter
        #!# path_painter = FrontBackPainter(self.painter_manager, 'path', PathPainter)
        #!# self.painter_manager.register_foreground_painter(path_painter)
        #!# path_painter.enable()
        
        #!# from .Sketcher import FrontBackSketcher
        #!# self.sketcher = FrontBackSketcher(image_format, path_painter)
        
        #!# from Elbrea.GraphicEngine.ForegroundPainter import SketcherPainter
        #!# painter = FrontBackPainter(self.painter_manager, 'sketcher', SketcherPainter)
        #!# self.painter_manager.register_foreground_painter(painter)
        #!# for painter, sketcher in ((painter.front_painter, self.sketcher.front_sketcher),
        #!#                           (painter.back_painter, self.sketcher.back_sketcher),
        #!#                       ):
        #!#     painter.create_texture(sketcher)
        #!# painter.enable()
        
        from Elbrea.GraphicEngine import ShaderProgrames as ShaderProgrames
        shader_manager = ShaderProgrames.shader_manager
        
        from Elbrea.GraphicEngine.TexturePainter import DynamicTexturePainter
        
        background_painter = self.painter_manager.background_painter.front_painter
        painter = DynamicTexturePainter(self.painter_manager, name='front-raw')
        background_painter.add_painter(painter, 'raw')
        painter.shader_program = shader_manager.texture_shader_program
        front_input = self.front_pipeline.input_filter.get_primary_output()
        painter.source = front_input
        painter = DynamicTexturePainter(self.painter_manager, name='front-hls')
        background_painter.add_painter(painter, 'hls')
        painter.shader_program = shader_manager.texture_shader_program
        front_input = self.front_pipeline.hls_filter.get_primary_output()
        painter.source = front_input
        # painter = background_painter.add_painter('user')
        # painter.shader_program = shader_manager.texture_shader_program
        # # painter.shader_program = shader_manager.texture_label_shader_program
        # front_input = self.front_pipeline.hls_filter.get_primary_output()
        # # front_input = self.front_pipeline.user_filter.get_primary_output()
        # painter.source = front_input
        background_painter.select_painter('raw')
        
        background_painter = self.painter_manager.background_painter.back_painter
        painter = DynamicTexturePainter(self.painter_manager, name='back-raw')
        background_painter.add_painter(painter, 'raw')
        painter.shader_program = shader_manager.texture_shader_program
        back_input = self.back_pipeline.input_filter.get_primary_output()
        painter.source = back_input
        painter = DynamicTexturePainter(self.painter_manager, name='back-hls')
        background_painter.add_painter(painter, 'hls')
        painter.shader_program = shader_manager.texture_shader_program
        back_input = self.back_pipeline.hls_filter.get_primary_output()
        painter.source = back_input
        # painter = background_painter.add_painter('user')
        # # painter.shader_program = shader_manager.texture_label_shader_program
        # painter.shader_program = shader_manager.texture_shader_program
        # # back_input = self.back_pipeline.user_filter.get_primary_output()
        # painter.source = back_input
        background_painter.select_painter('raw')
        
        # glwidget.makeCurrent()
        # from PyOpenGLng.HighLevelApi.RandomTexture import GlRandomTexture
        # shader_manager.texture_label_shader_program._random_texture = GlRandomTexture(size=1000, texture_unit=1)
        # glwidget.doneCurrent()
        
        #!# self.load(self.args.board)
        
        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()

    ##############################################

    def switch_face(self):

        self._logger.info("")
        
        self.painter_manager.switch_face()
        #!# self.sketcher.switch_face()

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

    def save(self, board_path=None):

        self._logger.info("")
        
        if board_path is None:
            board_path = self.args.board
        
        from .HdfAnnotation import HdfAnnotation
        hdf_annotation = HdfAnnotation(board_path, update=True)
         # Fixme: recto/verso
        group = hdf_annotation.create_group('front')
        self.sketcher.front_sketcher.save(group)
        group = hdf_annotation.create_group('back')
        self.sketcher.back_sketcher.save(group)

    ##############################################

    def load(self, board_path):

        from .HdfAnnotation import HdfAnnotation
        if os.path.exists(board_path):
            hdf_annotation = HdfAnnotation(board_path, update=False) # rewrite
            self.sketcher.front_sketcher.from_hdf5(hdf_annotation['front'])
            self.sketcher.back_sketcher.from_hdf5(hdf_annotation['back'])

####################################################################################################
#
# End
#
####################################################################################################
