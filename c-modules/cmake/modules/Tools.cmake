#######################################################################################################################
#
# Tools
#
#######################################################################################################################

# Fixme: "${}" ${} usage ?

#######################################################################################################################
#
# Read "# define" lines from an header file and set variables
#
# usage:
#   parse_header_for_define(FILENAME VAR1 VAR2 VAR3 ... [PARENT_SCOPE] [CACHE] )

macro(parse_header_for_define FILENAME)

  set(__parent_scope FALSE)
  set(__add_cache FALSE)
  set(__vars_regex "")
  set(__lines "")

  # Look for PARENT_SCOPE and CACHE in arguments, and build the regexp
  foreach(name ${ARGN})
    if("${name}" STREQUAL "PARENT_SCOPE")
      set(__parent_scope TRUE)
    elseif("${name}" STREQUAL "CACHE")
      set(__add_cache TRUE)
    elseif(__vars_regex)
      set(__vars_regex "${__vars_regex}|${name}")
    else()
      set(__vars_regex "${name}")
    endif()
  endforeach()

  if(EXISTS "${FILENAME}")
    file(STRINGS "${FILENAME}" __lines REGEX "#define[ \t]+(${__vars_regex})[ \t]+[0-9]+" )
  endif()

  foreach(name ${ARGN})
    if(NOT "${name}" STREQUAL "PARENT_SCOPE" AND NOT "${name}" STREQUAL "CACHE")
      if(__lines)
        if(__lines MATCHES ".+[ \t]${name}[ \t]+([0-9]+).*")
          string(REGEX REPLACE ".+[ \t]${name}[ \t]+([0-9]+).*" "\\1" ${name} "${__lines}")
        else()
          set(${name} "")
        endif()
        if(__add_cache)
          set(${name} ${${name}} CACHE INTERNAL "${name} parsed from ${FILENAME}" FORCE)
        elseif(__parent_scope)
          set(${name} "${${name}}" PARENT_SCOPE)
        endif()
      else()
        unset(${name} CACHE)
      endif()
    endif()
  endforeach()

endmacro()

#######################################################################################################################
#
# End
#
#######################################################################################################################
