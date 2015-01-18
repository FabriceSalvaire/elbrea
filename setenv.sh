####################################################################################################

source /srv/scratch/python-virtual-env/py3-pyqt5/bin/activate

####################################################################################################
# PyOpenGLng

append_to_ld_library_path_if_not /usr/local/stow/freetype-2.5.2/lib

append_to_python_path_if_not $HOME/pyglfw-cffi
append_to_python_path_if_not $HOME/PyOpenGLng

####################################################################################################

append_to_path_if_not ${PWD}/bin
append_to_path_if_not ${PWD}/tools

append_to_python_path_if_not ${PWD}

####################################################################################################
# 
# End
# 
####################################################################################################
