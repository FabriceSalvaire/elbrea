####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

import os

####################################################################################################

from PyOpenGLng.HighLevelApi.Shader import GlShaderManager, GlShaderProgramInterface
from PyOpenGLng.HighLevelApi.RandomTexture import GlRandomTexture, GlRandomTextureShaderProgram

####################################################################################################

class ConfigPath(object):

    module_path = os.path.dirname(__file__)

    ##############################################

    @staticmethod
    def glsl(file_name):

        return os.path.join(ConfigPath.module_path, 'glslv4', file_name)

####################################################################################################

shader_manager = GlShaderManager()

position_shader_program_interface = GlShaderProgramInterface(uniform_blocks=('viewport',),
                                                             attributes=('position',))

texture_shader_program_interface = GlShaderProgramInterface(uniform_blocks=('viewport',),
                                                            attributes=('position',
                                                                        'position_uv'))

text_shader_program_interface = GlShaderProgramInterface(uniform_blocks=('viewport',),
                                                         attributes=('position',
                                                                     'glyph_size',
                                                                     'position_uv',
                                                                     'colour'))

random_texture = GlRandomTexture(size=1000, texture_unit=1)

if shader_manager.has_visual():

    for shader_path in (
        #
        'vertex-shader/fixed_colour_vertex_shader',
        #
        'fragment-shader/simple_fragment_shader',
        'fragment-shader/antialiased_segment_fragment_shader',
        'fragment-shader/antialiased_path_fragment_shader',
        'fragment-shader/antialiased_object_fragment_shader',
        #
        'geometry-shader/fixed_colour_vertex_shader_in',
        #
        'geometry-shader/centred_rectangle_geometry_shader',
        'geometry-shader/rectangle_geometry_shader',
        'geometry-shader/roi_geometry_shader',
        'geometry-shader/object_geometry_shader',
        'geometry-shader/segment_geometry_shader',
        'geometry-shader/path_geometry_shader',
        #
        'texture-shader/texture_vertex_shader',
        'texture-shader/texture_fragment_shader',
        'texture-shader/texture_label_fragment_shader',
        #
        'text-shader/text_vertex_shader',
        'text-shader/text_geometry_shader',
        'text-shader/text_fragment_shader',
        ):
        shader_name = os.path.basename(shader_path)
        shader_manager.load_from_file(shader_name, ConfigPath.glsl(shader_path + '.glsl'))

    for args in (
        {'program_name':'fixed_shader_program',
         'shader_list':('fixed_colour_vertex_shader',
                        'simple_fragment_shader'),
         'program_interface':texture_shader_program_interface,
         },
        
        {'program_name':'texture_shader_program',
         'shader_list':('texture_vertex_shader',
                        'texture_fragment_shader'),
         'program_interface':texture_shader_program_interface,
         },
        
        {'program_name':'roi_shader_program',
         'shader_list':('fixed_colour_vertex_shader_in',
                        'roi_geometry_shader',
                        'simple_fragment_shader'),
         'program_interface':position_shader_program_interface,
         },
        
        {'program_name':'object_shader_program',
         'shader_list':('fixed_colour_vertex_shader_in',
                        'object_geometry_shader',
                        'antialiased_object_fragment_shader'),
         'program_interface':position_shader_program_interface,
         },
        
        {'program_name':'texture_label_shader_program',
         'shader_list':('texture_vertex_shader',
                        'texture_label_fragment_shader'),
         'program_interface':texture_shader_program_interface,
         'shader_program_class':GlRandomTextureShaderProgram,
         'shader_program_args':(random_texture,),
         },
        
        {'program_name':'text_shader_program',
         'shader_list':('text_vertex_shader',
                        'text_geometry_shader',
                        'text_fragment_shader'),
         'program_interface':text_shader_program_interface,
         },
        
        # {'program_name':'rectangle_shader_program',
        #  'shader_list':('fixed_colour_vertex_shader_in',
        #                 'rectangle_geometry_shader',
        #                 'simple_fragment_shader'),
        #  'program_interface':position_shader_program_interface,
        #  },
        
        # {'program_name':'centred_rectangle_shader_program',
        #  'shader_list':('fixed_colour_vertex_shader_in',
        #                 'centred_rectangle_geometry_shader',
        #                 'simple_fragment_shader'),
        #  'program_interface':position_shader_program_interface,
        #  },
        
        {'program_name':'segment_shader_program',
         'shader_list':('fixed_colour_vertex_shader_in',
                        'segment_geometry_shader',
                        'antialiased_segment_fragment_shader'),
         'program_interface':position_shader_program_interface,
         },
        
        {'program_name':'path_shader_program',
         'shader_list':('fixed_colour_vertex_shader_in',
                        'path_geometry_shader',
                        'antialiased_path_fragment_shader'),
         'program_interface':position_shader_program_interface,
         },
        
        ):
        shader_manager.link_program(**args)

####################################################################################################
#
# End
#
####################################################################################################
