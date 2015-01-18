#######################################################################################################################
#
# Find Intel(R) Thread Building Block Library (TBB)
#
#######################################################################################################################

message(STATUS "Looking for TBB ...")

# "/opt/intel/tbb/include"
# "/opt/intel/tbb/lib"

find_path(TBB_INCLUDE_PATH
  NAMES "tbb/tbb.h"
  PATHS ${WITH_TBB}/include "/usr/local/include" "/usr/include"
  DOC "The path to Intel(R) TBB header files"
  NO_DEFAULT_PATH
  NO_CMAKE_PATH
)

find_library(TBB_LIBRARY_PATH
  NAMES "tbb"
  PATHS "/usr/local/lib" "/usr/lib"
  DOC "The path to Intel(R) TBB library file"
  NO_DEFAULT_PATH
  NO_CMAKE_PATH
)

mark_as_advanced(
  TBB_INCLUDE_PATH
  TBB_LIBRARY_PATH
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(TBB DEFAULT_MSG TBB_INCLUDE_PATH TBB_LIBRARY_PATH)

if(TBB_FOUND)
  find_file(TBB_STDDEF_PATH "tbb/tbb_stddef.h" "${TBB_INCLUDE_PATH}")
  if(TBB_STDDEF_PATH)
    include(Tools)
    parse_header_for_define("${TBB_STDDEF_PATH}" TBB_VERSION_MAJOR TBB_VERSION_MINOR TBB_INTERFACE_VERSION)
  else()
    unset(TBB_VERSION_MAJOR)
    unset(TBB_VERSION_MINOR)
    unset(TBB_INTERFACE_VERSION)
  endif()

  message(STATUS "  found TBB ${TBB_VERSION_MAJOR}.${TBB_VERSION_MINOR} / ${TBB_INTERFACE_VERSION}")
  message(STATUS "  TBB include path ${TBB_INCLUDE_PATH}")
  message(STATUS "  TBB library path ${TBB_LIBRARY_PATH}")  
endif()

#######################################################################################################################
#
# End
#
#######################################################################################################################
