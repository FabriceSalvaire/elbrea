# -*- coding: utf-8 -*-

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

####################################################################################################

import os
import uuid

from PyQt4 import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

####################################################################################################

# from .IntensityProfile import IntensityProfileHdf
from Elbrea.Tools.RangeTracker import IntervalAggregator

####################################################################################################

# from ui.intensity_profile_form_ui import Ui_intensity_profile_form
# from .ui.intensity_profile_save_form_ui import Ui_intensity_profile_save_form

####################################################################################################

class IntensityProfileBaseForm(QtGui.QDialog):

    ###############################################

    def __init__(self, number_of_plots):

        super(IntensityProfileBaseForm, self).__init__()

        # self._application = QtGui.QApplication.instance()

        self._figure = Figure()
        self._axes = [self._figure.add_subplot(number_of_plots, 1, i)
                      for i in xrange(number_of_plots)] 

        self._canvas = FigureCanvas(self._figure)
        self._canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._canvas.setFocus()

        self._matplotlib_toolbar = NavigationToolbar(self._canvas, self)

        vertical_layout = QtGui.QVBoxLayout(self)
        for widget in self._canvas, self._matplotlib_toolbar:
            vertical_layout.addWidget(widget)

        # form.save_button.clicked.connect(self.save)

####################################################################################################

class LineIntensityProfileForm(IntensityProfileBaseForm):

    ###############################################

    def __init__(self, x_intensity_profile, y_intensity_profile):

        super(LineIntensityProfileForm, self).__init__(number_of_plots=2)


        self._x_intensity_profile = x_intensity_profile
        self._y_intensity_profile = y_intensity_profile
        
        self._draw()

    ##############################################

    def _draw_axis(self, plot_index, intensity_profile):

        axes = self._axes[plot_index]
        axes.clear()        
        axes.grid(True)

        interval_aggregator = IntervalAggregator()
        for colour, values in zip(('r', 'g', 'b'), intensity_profile):
            interval_aggregator.union(values.min(), values.max())
            x_output, y_output = intensity_profile.back_profile(values)
            axes.plot(x_output, y_output, colour)
            axes.set_title(intensity_profile.axis + ' axis')

        axes.set_ylim(interval_aggregator.inf, axes.get_ylim()[1])

        axes.axvline(x=intensity_profile.abscissa, color='black')

    ##############################################

    def _draw(self):

        for axis, intensity_profile in enumerate((self._y_intensity_profile,
                                                  self._x_intensity_profile)):
            self._draw_axis(axis, intensity_profile)

        self._canvas.draw()

    ##############################################
        
    # def save(self):

    #     dialog = IntensityProfileSaveForm((self._x_intensity_profile, self._y_intensity_profile))
    #     dialog.exec_()

####################################################################################################

# class IntensityProfileSaveForm(QtGui.QDialog):

#     ###############################################

#     def __init__(self, data):

#         super(IntensityProfileSaveForm, self).__init__()

#         form = self.form = Ui_intensity_profile_save_form()
#         form.setupUi(self)

#         self._application = QtGui.QApplication.instance()

#         self._data = data
#         label = str(uuid.uuid1())
#         form.label_line_edit.setText(label)
#         # form.comment_line_edit.setText(u'')
        
#         intensity_profile_file_name = os.path.join(directory, 'XXX.hdf5')
#         form.file_name_line_edit.setText(intensity_profile_file_name)

#         form.select_file_name_button.clicked.connect(self.select_file_name)
        
#     ##############################################
    
#     def select_file_name(self):

#         extension_filter = 'HDF5 files (*.hdf5)'
        
#         dialog = QtGui.QFileDialog.getSaveFileName
#         file_name = unicode(dialog(self,
#                                    'Select HDF5 File',
#                                    self.form.file_name_line_edit.text(),
#                                    extension_filter,
#                                    ))
        
#         self._application.intensity_profile_file_name = file_name
#         self.form.file_name_line_edit.setText(file_name)
        
#     ##############################################

#     def accept(self):

#         form = self.form
#         file_name = unicode(form.file_name_line_edit.text())
#         label = str(form.label_line_edit.text())
#         comment = str(form.comment_line_edit.text())

#         hdf_file = IntensityProfileHdf(file_name)
#         if isinstance(self._data, tuple):
#             group = hdf_file.create_group(label)
#             for intensity_profile in self._data:
#                 intensity_profile.save(group=group, name=intensity_profile.axis, comment=comment)
#         else:
#             self._data.save(group=hdf_file.root, name=label, comment=comment)
        
#         super(IntensityProfileSaveForm, self).accept()

####################################################################################################
#
# End
#
####################################################################################################
