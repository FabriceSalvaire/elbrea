# -*- CMake -*-

####################################################################################################
#
# Include directories
#

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

####################################################################################################
#
# Library
#

set(geometry_files
  Vector.cpp
  Line.cpp
  InertiaMatrix.cpp
)
string(REPLACE ".hpp" ".cpp" geometry_hpp_files "${geometry_files}")
add_library(geometry SHARED ${geometry_files})

####################################################################################################
#
# SWIG
#

set_source_files_properties(Geometry.i PROPERTIES CPLUSPLUS ON)
set(Geometry_files Geometry.i)
SET(SWIG_MODULE_Geometry_EXTRA_DEPS ${geometry_hpp_files})
swig_add_module(Geometry python ${Geometry_files})
swig_link_libraries(Geometry ${PYTHON_LIBRARIES} geometry)

####################################################################################################
#
# Executables rules
#

add_executable(test_geometry test_geometry.cpp GeometrySimd.cpp)

####################################################################################################
#
# Install
#

install(TARGETS
  geometry
  ${SWIG_MODULE_Geometry_REAL_NAME}
  LIBRARY DESTINATION lib/python${PYTHON_VERSION}/ImageProcessing/C)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/Geometry.py
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
