# -*- CMake -*-

####################################################################################################
#
# Include directories
#

include_directories(${CMAKE_CURRENT_SOURCE_DIR}
  ${ImageProcessing_SOURCE_DIR}/modules/algorithm
  ${ImageProcessing_SOURCE_DIR}/modules/math
  ${ImageProcessing_SOURCE_DIR}/modules/platform
  )

####################################################################################################
#
# Library
#

set(labelling_files
  ../../algorithm/UnionFind.cpp
  Island.cpp
  Label.cpp
  RandomPixelColour.cpp
)
string(REPLACE ".hpp" ".cpp" labelling_hpp_files "${labelling_files}")
add_library(labelling SHARED ${labelling_files})
link_libraries(labelling ${ROOT_LIBRARIES})

####################################################################################################
#
# SWIG
#

set_source_files_properties(Labelling.i PROPERTIES CPLUSPLUS ON)
set(Labelling_files Labelling.i)
SET(SWIG_MODULE_Labelling_EXTRA_DEPS ${labelling_hpp_files})
swig_add_module(Labelling python ${Labelling_files})
swig_link_libraries(Labelling ${PYTHON_LIBRARIES} ${GSL_LIBRARIES}
  -L../math geometry labelling)

####################################################################################################
#
# Install
#

install(TARGETS
  labelling
  ${SWIG_MODULE_Labelling_REAL_NAME}
  LIBRARY DESTINATION lib/python${PYTHON_VERSION}/ImageProcessing/C)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/Labelling.py
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
