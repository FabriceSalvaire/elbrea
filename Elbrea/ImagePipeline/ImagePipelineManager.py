####################################################################################################
# 
# Elbrea - Electronic Board Reverse Engineering Assistant
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

# shader_program is not image processing!

####################################################################################################

import logging

####################################################################################################

from .DependencyGraph import DependencyGraph
from .ImagePipeline import RawImagePipeline, ImagePipelineMetaClass
from Elbrea.Tools.AttributeDictionaryInterface import ExtendedDictionaryInterface

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ImagePipelineManager(ExtendedDictionaryInterface):

    # Fixme: The base class don't work as expected

    _logger = _module_logger.getChild('ImagePipelineManager')

    ##############################################

    def __init__(self, raw_data, shader_program=None):
        
        super(ImagePipelineManager, self).__init__()

        self._create_raw_image_pipelines(raw_data, shader_program)
        self._create_registered_image_pipelines()

    ##############################################

    def _create_raw_image_pipelines(self, raw_data, shader_program=None):

        self._logger.info("Create raw pipeline")

        pipeline = RawImagePipeline(raw_data, shader_program)
        self[pipeline.name] = pipeline
        # setattr(self, pipeline.name, pipeline)
        self.raw = pipeline

    ##############################################

    def _create_registered_image_pipelines(self):

        # should be a graph traversal
        dependency_graph = DependencyGraph(self.raw)
        for pipeline_name, cls in ImagePipelineMetaClass.classes.items():
            self._logger.info("pipeline {} depends of {}".format(pipeline_name, cls.__input_pipelines__))
            dependency_graph.add_node(cls())
        for node in dependency_graph:
            for input_pipeline in node.__input_pipelines__:
                parent_node = dependency_graph[input_pipeline]
                parent_node.childs.append(node) 
                node.parents.append(parent_node)
        for node in dependency_graph.top_down_visit():
            print(node.name)
            
            # if pipeline_name not in self:
            #     self._logger.info("Create pipeline {}".format(pipeline_name))
            #     self[pipeline_name] = cls(self.raw) # Fixme: should be input
            # else:
            #     raise NameError("Pipeline %s already registered" % (pipeline_name))

        # dependency_graph = DependencyGraph(self.raw)
        # for pipeline_name, cls in ImagePipelineMetaClass.classes.items():
        #     self._logger.info("pipeline {} depends of {}".format(pipeline_name, cls.__input_pipelines__))
        #     dependency_graph.add_node(DependencyGraphNode(pipeline_name, data=cls))
        # for node in dependency_graph.nodes.values():
        #     for input_pipeline in node.data.__input_pipelines__:
        #         parent_node = dependency_graph.nodes[input_pipeline]
        #         parent_node.childs.append(node) 
        #         node.parents.append(parent_node)
        # for node in dependency_graph.top_down_visit():
        #     print(node.node_id)


####################################################################################################
# 
# End
# 
####################################################################################################
