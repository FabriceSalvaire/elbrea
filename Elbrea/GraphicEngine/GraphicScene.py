####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 20/10/2011 Fabrice
#  - z_value is not used
#  - glortho2d -> coordinate_mapper
#    - window_to_scene_coordinate
#    - window_to_scene_distance
#
####################################################################################################

####################################################################################################

import logging
import numpy as np

from rtree import Rtree

####################################################################################################

from Elbrea.Math.Interval import IntervalInt2D

####################################################################################################

def point_interval(x, y):
    return IntervalInt2D((x, x), (y, y))

def centred_interval(x, y, radius):
    return point_interval(x, y).enlarge(radius)

####################################################################################################

class GraphicScene(object):

    ITEM_SELECTION_RADIUS = 2 # px

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, glortho2d):

        self._glortho2d = glortho2d # Fixme: used for window_to_scene_coordinate window_to_scene_distance
        self._items = {}
        self._rtree = Rtree()
        self._selected_item = None

    ##############################################

    def _window_to_scene_coordinate(self, event):

        location = np.array((event.x(), event.y()), dtype=np.float)
        return list(self._glortho2d.window_to_gl_coordinate(location))

    ##############################################

    def _window_to_scene_distance(self, x):

        return self._glortho2d.window_to_gl_distance(x)

    ##############################################

    def add_item(self, item):

        item_id = hash(item)
        self._items[item_id] = item
        self._rtree.add(item_id, item.bounding_box)

    ##############################################

    def remove_item(self, item):

        if self._selected_item is item:
            self.deselect_item(item)

        item_id = hash(item)
        del self._items[item_id]
        self._rtree.delete(item_id, item.bounding_box)

    ##############################################

    def select_item(self, item):

        item.is_selected = True
        self._selected_item = item

    ##############################################

    def deselect_item(self, item):

        item.is_selected = False
        self._selected_item = None

    ##############################################

    def items_in(self, interval):

        self._logger.debug(str( interval))
        items = [self._items[x] for x in self._rtree.intersection(interval.bounding_box())]
        items.sort() # accordind to z value

        return items

    ##############################################

    def items_at(self, x, y):

        return self.items_in(point_interval(x, y))

    ##############################################

    def items_around(self, x, y, radius):

        return self.items_in(centred_interval(x, y, radius))

    ##############################################

    def item_under_mouse(self, event):

        x, y = self._window_to_scene_coordinate(event)
        radius = self._window_to_scene_distance(GraphicScene.ITEM_SELECTION_RADIUS)

        items = self.items_around(x, y, radius)
        if items:
            # return the highest z value
            # Fixme: ok ?
            return items[-1]
        else:
            return None

    ##############################################

    def keyPressEvent(self, event):

        return False

    ##############################################

    def keyReleaseEvent(self, event):

        return False

    ##############################################

    def mousePressEvent(self, event):

        item = self.item_under_mouse(event)
        if item is not None:
            self.select_item(item)
            item.mousePressEvent(event)
            return True
        else:
            return False

    ##############################################

    def mouseReleaseEvent(self, event):

        if self._selected_item is not None:
            self._selected_item.mouseReleaseEvent(event)
            self.deselect_item(self._selected_item)
            return True
        else:
            return False

    ##############################################

    def mouseDoubleClickEvent(self, event):

        return False

    ##############################################

    def wheelEvent(self, event):

        return False

    ##############################################

    def mouseMoveEvent(self, event):

        if self._selected_item is not None:
            self._selected_item.mouseMoveEvent(event)
            return True
        else:
            return False

####################################################################################################

class GraphicSceneItem(object):

    _last_id = 0

    ##############################################

    def __init__(self, interval, z_value=0):

        self._hash = GraphicSceneItem._get_new_id()
        self._interval = interval.copy()
        self._is_selected = False
        self._z_value = z_value

    ##############################################

    @staticmethod
    def _get_new_id():

        GraphicSceneItem._last_id += 1

        return GraphicSceneItem._last_id

    ##############################################

    @property
    def bounding_box(self):

        return self._interval.bounding_box()

    ##############################################

    def __lt__(self, other):

        return self._z_value < other._z_value

    ##############################################

    def __hash__(self):

        return self._hash

    ##############################################

    def keyPressEvent(self, event):

        pass

    ##############################################

    def keyReleaseEvent(self, event):

        pass

    ##############################################

    def mouseDoubleClickEvent(self, event):

        pass

    ##############################################

    def wheelEvent(self, event):

        pass

    ##############################################

    def mousePressEvent(self, event):

        pass

    ##############################################

    def mouseReleaseEvent(self, event):

        pass

    ##############################################

    def mouseMoveEvent(self, event):

        pass

####################################################################################################

class GraphicSceneSquareItem(GraphicSceneItem):

    ##############################################

    def __init__(self, x, y, radius, **kwargs):

        interval = centred_interval(x, y, radius)
        super(GraphicSceneSquareItem, self).__init__(interval, **kwargs)

####################################################################################################

# class GraphicSceneSegmentItem(GraphicSceneItem):
#
#     ##############################################
#
## Point2D ?
#
#     def __init__(self, x0, y0, x1, y1):
#
#         super(GraphicSceneSquareItem, self).__init__(...)

####################################################################################################
#
# End
#
####################################################################################################
