####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

####################################################################################################

class Path(object):

    config_directory = os.path.join(os.environ['HOME'], '.config', 'elbrea')

    # data_directory = os.path.join(os.environ['HOME'], '.local', 'share', 'data', 'elbrea')
    data_directory = os.path.join(os.environ['HOME'], '.local', 'elbrea')

####################################################################################################

class Email(object):

    from_address = 'fabrice.salvaire@orange.fr'
    to_address = ['fabrice.salvaire@orange.fr',]

####################################################################################################

class Help(object):

    host = 'localhost'
    url_scheme = 'http'
    url_path_pattern = '/'

####################################################################################################

class RedmineRest(object):

    url = 'http://loalhost/redmine/'
    key = '02caaf292242bbfde9000291cb9955337fa87518'
    project = 'Elbrea'

####################################################################################################

class Shortcut(object):

    pass

####################################################################################################
#
# End
#
####################################################################################################
