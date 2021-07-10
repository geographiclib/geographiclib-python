# Install the python files.
# Probably full-time python users should install the python package from
# http://pypi.python.org/pypi/geographiclib
file (GLOB PYTHON_FILES [A-Za-z_]*.py)
file (GLOB TEST_FILES test/[A-Za-z_]*.py)
if (COMMON_INSTALL_PATH)
  set (INSTALL_PYTHON_DIR "lib${LIB_SUFFIX}/python/site-packages")
else ()
  set (INSTALL_PYTHON_DIR "python")
endif ()

install (FILES ${PYTHON_FILES}
  DESTINATION ${INSTALL_PYTHON_DIR}/geographiclib)
install (FILES ${TEST_FILES}
  DESTINATION ${INSTALL_PYTHON_DIR}/geographiclib/test)

# Only install setup.py under Windows because the installation tree is,
# e.g., c:/Program Files/GeographicLib/${INSTALL_PYTHON_PATH}.  Don't
# install on other systems where this command would create, e.g.,
# /usr/local/${INSTALL_PYTHON_PATH}/setup.py which is likely to cause
# conflicts.
if (NOT COMMON_INSTALL_PATH)
  install (FILES ../setup.py DESTINATION ${INSTALL_PYTHON_DIR})
endif ()

# From: https://bloerg.net/posts/cmake-and-distutils/
# find_program(PYTHON "python")

# if (PYTHON)
#   set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
#   set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
#   set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/module/__init__.py")
#   set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")

#   configure_file(${SETUP_PY_IN} ${SETUP_PY})

#   add_custom_command(OUTPUT ${OUTPUT}
#     COMMAND ${PYTHON} ${SETUP_PY} build
#     COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
#     DEPENDS ${DEPS})

#   add_custom_target(target ALL DEPENDS ${OUTPUT})

#   install(CODE "execute_process(COMMAND ${PYTHON} ${SETUP_PY} install)")
# endif()

# setup.py.in
# from distutils.core import setup

# setup(name='foo',
#       version='${PACKAGE_VERSION}',
#       package_dir={ '': '${CMAKE_CURRENT_SOURCE_DIR}' },

# linting...

find_program (LINT pylint)
if (LINT)
  set (INDENT "  ")
  add_custom_target (lint ${LINT}
    --max-attributes=36
    --max-module-lines=1295
    --max-branches=34
    --max-args=15
    --max-locals=76
    --max-statements=175
    --argument-naming-style=any
    --attr-naming-style=any
    --method-naming-style=any
    --variable-naming-style=any
    --indent-string=${INDENT}
    -d C0321,R0124
    ${PYTHON_FILES})
endif ()

