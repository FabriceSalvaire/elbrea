####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import numpy as np
import h5py

####################################################################################################

from Elbrea.Sketcher.Page import Pages, Page
from Elbrea.Sketcher.Path import Path

####################################################################################################

class HdfFile(object):

    ##############################################
        
    def __init__(self, file_path, update=False):

        """ Open an HDF5 file in append mode
        """

        if update:
            mode = 'w' # a
        else:
            mode = 'r'

        self._hdf_file = h5py.File(file_path, mode)

    ##############################################

    def __del__(self):

        self._hdf_file.close()
    
    ##############################################

    @property
    def root(self):
        return self._hdf_file['/']

    ##############################################

    def __getitem__(self, path):
        return self._hdf_file[path]

    ##############################################
        
    def create_group(self, name):

        return self._hdf_file.create_group(name)

####################################################################################################

class HdfImporter(HdfFile):

    ##############################################

    def __init__(self, file_path):
    
        super(HdfImporter, self).__init__(file_path)

        self._pages_group = self['pages']

        attributes = self.root.attrs
        self._number_of_pages = attributes['number_of_pages']

    ##############################################

    def read_path(self, group, name):

        dataset = group[name]
        attributes = dataset.attrs

        colour = [int(x) for x in attributes['colour']]
        pencil_size = int(attributes['pencil_size'])
        points = np.array(dataset)

        return Path(colour, pencil_size, points)
   
    ##############################################

    def read_page(self, page_index):

        group = self._pages_group[str(page_index)]
        page = Page()
        for name in group:
            path = self.read_path(group, name)
            page.add_path(path)

        return page

    ##############################################

    def read_pages(self):

        pages = Pages()
        for i in range(self._number_of_pages):
            pages.add_page(self.read_page(i))

        return pages
        
####################################################################################################

class HdfWriter(HdfFile):

    ##############################################

    def __init__(self, file_path):
    
        super(HdfWriter, self).__init__(file_path, update=True)

        self._pages_group = self.create_group('pages')

    ##############################################

    def save_path(self, group, path):

        name = 'path-{}'.format(path.id)
        dataset = group.create_dataset(name, data=path.points,
                                       shuffle=True, compression='lzf')
        attributes = dataset.attrs
        attributes['colour'] = path.colour
        attributes['pencil_size'] = path.pencil_size

    ##############################################

    def save_page(self, page_index, page):

        group = self._pages_group.create_group(str(page_index))
        for path in page.paths:
            self.save_path(group, path)
            
    ##############################################

    def save_pages(self, pages):

        attributes = self.root.attrs
        attributes['number_of_pages'] = pages.number_of_pages
        
        for i, page in enumerate(pages):
            self.save_page(i, page)
            
####################################################################################################
# 
# End
# 
####################################################################################################
