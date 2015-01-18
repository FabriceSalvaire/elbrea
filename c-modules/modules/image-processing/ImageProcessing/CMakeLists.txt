# -*- CMake -*-

####################################################################################################
#
# Compiler Flags
#

if(CMAKE_COMPILER_IS_GNUCXX)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -msse4.1 -std=c++11")
endif()

####################################################################################################
#
# Include directories
#

include_directories(${CMAKE_CURRENT_SOURCE_DIR}
  ${ImageProcessing_SOURCE_DIR}/modules/math
  ${ImageProcessing_SOURCE_DIR}/modules/platform
  )

####################################################################################################
#
# Library
#

set(image_processing_files
  ImageException.cpp
  Image.cpp
  ImageGeometry.cpp
  ImageOperations.cpp
  ImageSimdOperations.cpp
  ImageProfile.cpp
)
string(REPLACE ".hpp" ".cpp" image_processing_hpp_files "${image_processing_files}")
add_library(image_processing SHARED ${image_processing_files})
target_link_libraries(image_processing geometry IntelCpuTools)

####################################################################################################
#
# SWIG
#

set_source_files_properties(ImageProcessing.i PROPERTIES CPLUSPLUS ON)
set(ImageProcessing_files ImageProcessing.i)
SET(SWIG_MODULE_ImageProcessing_EXTRA_DEPS ${image_processing_hpp_files})
swig_add_module(ImageProcessing python ${ImageProcessing_files})
swig_link_libraries(ImageProcessing ${PYTHON_LIBRARIES} IntelCpuTools image_processing)

####################################################################################################
#
# Install
#

install(TARGETS
  ${SWIG_MODULE_ImageProcessing_REAL_NAME}
  LIBRARY DESTINATION lib/python${PYTHON_VERSION}/ImageProcessing/C)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/ImageProcessing.py
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
