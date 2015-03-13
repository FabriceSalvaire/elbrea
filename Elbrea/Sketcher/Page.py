####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import logging

import rtree

####################################################################################################

from .Path import Path

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Pages(list):
    pass

####################################################################################################

class Page(object):

    # Page is scene, GL page keeps reference to vao, painter render the scene
    # We could reimplement add_path and remove_path
    
    ##############################################

    def __init__(self):

        self._paths = {}
        self._rtree = rtree.index.Index()

    ##############################################

    @property
    def paths(self):
        return self._paths.values()

    ##############################################

    def add_path(self, path):

        self._paths[path.id] = path
        # self._rtree.add(path.id, path.interval.bounding_box(), obj=path)

    ##############################################

    def remove_path(self, path):

        print(self._paths)
        del self._paths[path.id]
        # self._rtree.delete(path.id, path.interval.bounding_box())

    ##############################################

    def add_paths(self, paths):

        # self._paths.update({path.id:path for path in paths})
        for path in paths:
            self.add_path(path)

    ##############################################

    def objects_near(self, position, radius):

        # Fixme: cost ?
        # lower_position = position - radius
        # upper_position = position + radius
        hits = self._rtree.intersection((position[0] - radius, position[1] - radius,
                                         position[0] + radius, position[1] + radius),
                                        objects='raw')
        return hits
    
####################################################################################################
#
# End
#
####################################################################################################
