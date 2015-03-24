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

from .GraphicScene import GraphicScene

from .PageFormat import page_format_database
a4_portrait = page_format_database('a4')

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Pages(object):

    # We don't store a page number in page instance, since a page remaniment could require to update
    # a lot of page numbers.
    
    ##############################################

    def __init__(self, page_format=a4_portrait):

        self._page_format = page_format
        self._pages = []
        # dict to quickly find a page ?

    ##############################################

    @property
    def page_format(self):
        return self._page_format
    
    @property
    def number_of_pages(self):
        return len(self._pages)

    @property
    def last_page_index(self):
        return len(self._pages) -1
    
    ##############################################

    def __len__(self):

        return len(self._pages)
    
    ##############################################

    def __iter__(self):

        return iter(self._pages)

    ##############################################

    def __getitem__(self, slice_):

        return self._pages[slice_]
    
    ##############################################

    def add_page(self, page=None):

        if page is None:
            page = Page()
        self._pages.append(page)
        return page

    ##############################################

    def insert_page(self, position):

        page = Page()
        self._pages.insert(position, page)
        return page

    ##############################################

    def remove_page(self, position):

        del self._pages[position]

    ##############################################

    def move_page(self, from_, to):

        page = self._pages[from_]
        del self._pages[from_]
        self._pages.insert(to, page)
        
####################################################################################################

class Page(GraphicScene):

    # Page is scene, GL page keeps reference to vao, painter render the scene
    # We could reimplement add_path and remove_path

    ##############################################

    def __init__(self):

        super(Page, self).__init__()

####################################################################################################
#
# End
#
####################################################################################################
