####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

import logging

import numpy as np

####################################################################################################

from .Path import Segment, Path, DynamicPath
from .TabletEvent import TabletEventType
from Elbrea.Math.Interval import IntervalInt2D, Interval2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class SketcherState(object):

    ##############################################

    def __init__(self):

        self.pencil_size = 1
        self.eraser_size = 1
        self.pencil_colour = (255, 255, 255)
        self.previous_position = None

####################################################################################################

class SegmentSketcher(object):

    _logger = _module_logger.getChild('SegmentSketcher')

    ##############################################

    def __init__(self, sketcher_state, page_provider, painter):

        self._sketcher_state = sketcher_state

        self._page_provider = page_provider
        self._painter = painter

        self._current_segment = None

    ##############################################

    def _start_segment(self, position):

        self._current_segment = Segment(self._sketcher_state.pencil_colour,
                                        self._sketcher_state.pencil_size,
                                        position)

    ##############################################

    def _update_segment(self, position):

        self._current_segment.update_second_point(position)

    ##############################################

    def _end_segment(self, position):

        self._current_segment.update_second_point(position)
        self._page_provider.page.add_item(self._current_segment)
        self._first_point = None

        return self._current_segment

    ##############################################

    def on_pen_event(self, tablet_event):

        # self._logger.info(str(tablet_event))

        modified = False
        position = tablet_event.position
        if tablet_event.type == TabletEventType.move:
            previous_position = self._sketcher_state.previous_position
            distance = np.sum((position - previous_position)**2) # _square
            if distance > 1:
                self._update_segment(position)
                self._painter.update_current_item(self._current_segment)
                modified = True # Fixme: modified signal ?
                self._sketcher_state.previous_position = position
        else:
            if tablet_event.type == TabletEventType.press:
                self._start_segment(position)
            else: # tablet_event.type == TabletEventType.release
                path = self._end_segment(position)
                self._painter.reset_current_path()
                self._painter.add_item(path)
                modified = True
            self._sketcher_state.previous_position = position

        return modified

####################################################################################################

class PointFilter(object):

    ##############################################

    def __init__(self, window_size):

        self._window_size = window_size
        self._window_points = np.zeros((self._window_size, 2), dtype=np.float32)
        self._window_counter = 0
        self._window_index = 0

    ##############################################

    def __bool__(self):

        return self._window_counter >= self._window_size

    ##############################################

    def reset(self):

        self._window_index = 0
        self._window_counter = 0
        self._window_points[...] = 0 # fixme: required ???

    ##############################################

    def send(self, point):

        self._window_points[self._window_index] = point
        self._window_index = (self._window_index + 1) % self._window_size
        self._window_counter += 1

    ##############################################

    @property
    def value(self):

        if bool(self):
            return np.mean(self._window_points, axis=0)
        else:
            return None

####################################################################################################

class PathSketcher(object):

    _logger = _module_logger.getChild('PathSketcher')

    ##############################################

    def __init__(self, sketcher_state, page_provider, painter):

        self._sketcher_state = sketcher_state

        self._page_provider = page_provider
        self._painter = painter

        self._current_path = None
        self._point_filter = PointFilter(window_size=10)

    ##############################################

    @property
    def _page(self):
        return self._page_provider.page

    ##############################################

    def _start_path(self):

        self._current_path = DynamicPath(self._sketcher_state.pencil_colour,
                                         self._sketcher_state.pencil_size)
        self._point_filter.reset()

    ##############################################

    def _end_path(self):

        path = self._current_path.to_path()
        path = path.backward_smooth_window(radius=3)
        # path = path.simplify(tolerance=1)
        self._page.add_item(path)
        self._current_path = None

        return path

    ##############################################

    def on_pen_event(self, tablet_event):

        self._logger.info(str(tablet_event))

        modified = False
        if tablet_event.type == TabletEventType.move:
            self._point_filter.send(tablet_event.position)
            position = self._point_filter.value
            # if position is None:
            #     self._logger.warning('Not ready')
            # Fixme: case previous_position is None ?
            if position is not None and self._sketcher_state.previous_position is not None:
                previous_position = self._sketcher_state.previous_position
                distance = np.sum((position - previous_position)**2) # _square
                if distance > 1:
                    self._current_path.add_point(position)
                    self._painter.update_current_item(self._current_path.to_path())
                    modified = True # Fixme: modified signal ?
                    self._sketcher_state.previous_position = position
        else:
            position = tablet_event.position
            if tablet_event.type == TabletEventType.press:
                self._start_path()
                self._point_filter.send(position)
                self._current_path.add_point(position)
            elif tablet_event.type == TabletEventType.release:
                # add point ?
                path = self._end_path()
                self._painter.reset_current_path()
                self._painter.add_item(path)
                modified = True
            self._sketcher_state.previous_position = position

        self._painter.enable() # Fixme: here ?

        return modified

####################################################################################################

class Eraser(object):

    _logger = _module_logger.getChild('Eraser')

    ##############################################

    def __init__(self, sketcher_state, page_provider):

        self._sketcher_state = sketcher_state
        self._page_provider = page_provider

    ##############################################

    def on_pen_event(self, tablet_event):

        self._logger.info("")

        # Fixme: design, self._page, painter access
        
        radius = self._sketcher_state.eraser_size
        position = tablet_event.position
        page = self._page_provider.page
        removed_items, new_items = page.erase(position, radius)

        page_provider = self._page_provider
        for item in removed_items:
            painter = page_provider.painter_for_item(item)
            if painter is not None:
                painter.remove_item(item)
        for item in new_items:
            painter = page_provider.painter_for_item(item)
            if painter is not None:
                painter.add_item(item)

        return bool(removed_items)

####################################################################################################
#
# End
#
####################################################################################################
