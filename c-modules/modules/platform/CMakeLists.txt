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

add_library(IntelCpuTools SHARED IntelCpuTools.cpp MemoryAlignment.cpp DataType.cpp)
add_library(PlatformC SHARED Platform.cpp) 

####################################################################################################
#
# SWIG
#

set_source_files_properties(PlatformC.i PROPERTIES CPLUSPLUS ON)
set(PlatformC_files
  PlatformC.i)
SET(SWIG_MODULE_PlatformC_EXTRA_DEPS Platform.hpp)
swig_add_module(PlatformC python ${PlatformC_files})
swig_link_libraries(PlatformC ${PYTHON_LIBRARIES} PlatformC)

if(CMAKE_SYSTEM_NAME MATCHES "Windows")
  SET_TARGET_PROPERTIES(
    ${SWIG_MODULE_PlatformC_REAL_NAME}
    PROPERTIES SUFFIX .pyd)
endif(CMAKE_SYSTEM_NAME MATCHES "Windows")

####################################################################################################
#
# Install
#

install(TARGETS
  IntelCpuTools
  PlatformC
  ${SWIG_MODULE_PlatformC_REAL_NAME}
  LIBRARY DESTINATION lib/python${PYTHON_VERSION}/ImageProcessing/C)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/PlatformC.py
  DESTINATION lib/python${PYTHON_VERSION}/ImageProcessing/C)

####################################################################################################
#
# Executables rules
#

add_executable(test-cpu-features test-cpu-features.cpp)
target_link_libraries (test-cpu-features IntelCpuTools)

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
