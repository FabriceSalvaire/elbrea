#######################################################################################################################
#
# Find Python
#
#######################################################################################################################

message(STATUS "Looking for Python ...")

#######################################################################################################################

find_package(PythonInterp)

#######################################################################################################################

find_program(PYTHON_CONFIG NAMES python3.4-config)
mark_as_advanced(PYTHON_CONFIG)

#######################################################################################################################

set(_python_version_output "${PYTHON_CONFIG}")
string(REGEX REPLACE ".*python\([0-9.]+\)-config" "\\1" _python_version_output "${_python_version_output}")
set(PYTHON_VERSION ${_python_version_output} CACHE STRING "Python Version" FORCE)
message(STATUS "  Python version is ${PYTHON_VERSION}")

#######################################################################################################################

if(PYTHON_CONFIG)

  exec_program(${PYTHON_CONFIG}
    ARGS "--prefix"
    OUTPUT_VARIABLE PYTHON_PREFIX)
  
  #  exec_program(${PYTHON_CONFIG}
  #    ARGS "--includes"
  #    OUTPUT_VARIABLE PYTHON_INCLUDE_PATH)

  find_path(PYTHON_INCLUDE_PATH
    NAMES Python.h
    PATHS "${PYTHON_PREFIX}/include/python${PYTHON_VERSION}m"
    )

  mark_as_advanced(
    PYTHON_INCLUDE_PATH
  )

  message(STATUS "  Python include path ${PYTHON_INCLUDE_PATH}")
endif()

#######################################################################################################################
#
# End
#
#######################################################################################################################
