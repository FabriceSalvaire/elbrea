# -*- CMake -*-

####################################################################################################
#
# Customizable settings
#

# -D <var>:<type>=<value>: Create a cmake cache entry.

# Install path prefix, prepended onto install directories.
# -D CMAKE_INSTALL_PREFIX:PATH=/usr/local/stow/bar

# Choose the type of build, options are: None(CMAKE_CXX_FLAGS or
# CMAKE_C_FLAGS used) Debug Release RelWithDebInfo MinSizeRel.
# -D CMAKE_BUILD_TYPE:STRING=Debug

# If this value is on, makefiles will be generated without the
# .SILENT directive, and all commands will be echoed to the console
# during the make.  This is useful for debugging only.
# -D CMAKE_VERBOSE_MAKEFILE:BOOL=ON

####################################################################################################

project(ImageProcessing)

# cf. Version.py
set(IMAGE_PROCESSING_VERSION_MAJOR 0)
set(IMAGE_PROCESSING_VERSION_MINOR 8)
set(IMAGE_PROCESSING_VERSION_PATCH 0)

set(IMAGE_PROCESSING_VERSION ${IMAGE_PROCESSING_VERSION_MAJOR}.${IMAGE_PROCESSING_VERSION_MINOR}.${IMAGE_PROCESSING_VERSION_PATCH})

####################################################################################################

# check cmake version
cmake_minimum_required(VERSION 2.8)

if(COMMAND cmake_policy)
  cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

# where to look first for cmake modules, before ${CMAKE_ROOT}/Modules/ is checked
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules")

####################################################################################################
#
# Compiler Options
#

# SET(CMAKE_BUILD_TYPE RELEASE)
# SET(CMAKE_VERBOSE_MAKEFILE FALSE)

# disallow -fstrict-aliasing for swig
# -Werror
# Other optimisations : -finline-limit=1500 -pipe -fomit-frame-pointer -fno-strict-aliasing

if(CMAKE_SYSTEM_NAME MATCHES "Linux")
  set(CMAKE_CXX_FLAGS_COMMON  "-Wall -DSystemLinux")
  set(CMAKE_CXX_FLAGS_DEBUG   "${CMAKE_CXX_FLAGS_COMMON} -g -O0 -DDEBUG")
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_COMMON} $ENV{OPTIMISATION}")
endif(CMAKE_SYSTEM_NAME MATCHES "Linux")

####################################################################################################
#
# Find Libraries
#

# OpenMP
#  Set:
#   OpenMP_C_FLAGS - flags to add to the C compiler for OpenMP support
#   OpenMP_CXX_FLAGS - flags to add to the CXX compiler for OpenMP support
#   OPENMP_FOUND - true if openmp is detected
#!# include(FindOpenMP)

#!# include(FindTBB)

####################################################################################################
#
# Python
#

include(FindPython)

##################################################
#
# Numpy
#

find_path(NUMPY_INCLUDE_PATH
  NAMES "numpy/arrayobject.h"
  PATHS "${PYTHON_PREFIX}/lib/python${PYTHON_VERSION}/site-packages/numpy/core/include"
)
mark_as_advanced(NUMPY_INCLUDE_PATH)
include_directories(${NUMPY_INCLUDE_PATH})

####################################################################################################
#
# Swig
#

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

include_directories(${PYTHON_INCLUDE_PATH})

set(CMAKE_SWIG_FLAGS_COMMON "-Wall")

if(CMAKE_SYSTEM_NAME MATCHES "Linux")
  set(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS_COMMON} -DSystemLinux)
endif(CMAKE_SYSTEM_NAME MATCHES "Linux")

####################################################################################################
#
# Sub directories
#

add_subdirectory(modules)

####################################################################################################
#
# End
#
####################################################################################################
