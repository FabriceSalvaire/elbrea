####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

from PyQt5 import QtWidgets

####################################################################################################

from .ui.image_properties_form_ui import Ui_image_properties_form

####################################################################################################

class ImagePropertiesForm(QtWidgets.QDialog, Ui_image_properties_form):

    ###############################################

    def __init__(self, position):

        QtWidgets.QDialog.__init__(self)

        self.setupUi(self)

        extensions = '*.png *.jpg *.jpeg *.tif *.tiff'
        extension_filter = 'Images (' + extensions + ' ' + extensions.upper() + ')'
        dialog = QtWidgets.QFileDialog.getOpenFileName
        self._image_path, ok = dialog(self, 'Open File', directory='', filter=extension_filter)

        self.path_label.setText(self._image_path)

####################################################################################################
#
# End
#
####################################################################################################
