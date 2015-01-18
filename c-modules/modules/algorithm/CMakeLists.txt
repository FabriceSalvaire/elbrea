# -*- CMake -*-

####################################################################################################
#
# Include directories
#

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

####################################################################################################
#
# SWIG
#

set_source_files_properties(DisjointSet.i PROPERTIES CPLUSPLUS ON)
set(DisjointSet_files DisjointSet.i
  DisjointSet.cpp)
SET(SWIG_MODULE_DisjointSet_EXTRA_DEPS DisjointSet.hpp)
swig_add_module(DisjointSet python ${DisjointSet_files})
swig_link_libraries(DisjointSet ${PYTHON_LIBRARIES})

####################################################################################################
#
# Install
#

install(TARGETS
  ${SWIG_MODULE_DisjointSet_REAL_NAME}
  LIBRARY DESTINATION lib/python${PYTHON_VERSION}/ImageProcessing/C)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/DisjointSet.py
  DESTINATION lib/python${PYTHON_VERSION}/ImageProcessing/C)

####################################################################################################
#
# Clean
#

# set_directory_properties(PROPERTIES ADDITIONAL_MAKE_CLEAN_FILES "")

####################################################################################################
#
# End
#
####################################################################################################
