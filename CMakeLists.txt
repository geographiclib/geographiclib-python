project (GeographicLib-Python NONE)

# Version information
set (PROJECT_VERSION_MAJOR 2)
set (PROJECT_VERSION_MINOR 0)
set (PROJECT_VERSION_PATCH 0)
set (PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}")
if (PROJECT_VERSION_PATCH GREATER 0)
  set (PROJECT_VERSION "${PROJECT_VERSION}.${PROJECT_VERSION_PATCH}")
endif ()
set (PROJECT_VERSION_SUFFIX "a0")
set (PROJECT_VERSION "${PROJECT_VERSION}${PROJECT_VERSION_SUFFIX}")

set (RELEASE_DATE "2022-mm-dd")

cmake_minimum_required (VERSION 3.13.0)

# Set a default build type for single-configuration cmake generators if
# no build type is set.
if (NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set (CMAKE_BUILD_TYPE Release)
endif ()

configure_file (setup.py.in setup.py @ONLY)
set (EXTRA_FILES setup.cfg README.md LICENSE MANIFEST.in)
foreach (f ${EXTRA_FILES})
  configure_file (${f} ${f} COPYONLY)
endforeach ()

find_package (Python ${Python_VERSION_NUMBER} COMPONENTS Interpreter)
message (STATUS
  "Python found: ${Python_EXECUTABLE}, Version: ${Python_VERSION}")

# Set source files here since they are used in multiple places
set (PYTHON_FILES
  accumulator.py constants.py geodesiccapability.py
  geodesicline.py geodesic.py geomath.py polygonarea.py)
set (TEST_FILES
  test/__init__.py test/test_geodesic.py test/test_sign.py)

add_subdirectory (geographiclib)

enable_testing ()
# Run the test suite
add_test (NAME testsuite
  COMMAND ${Python_EXECUTABLE} -m unittest -v geographiclib.test.test_geodesic)
add_test (NAME testsign
  COMMAND ${Python_EXECUTABLE} -m unittest -v geographiclib.test.test_sign)

# For Python documentation
find_program (SPHINX sphinx-build)
if (SPHINX)
  add_subdirectory (doc)
endif ()

set (ALLDEPENDS)
foreach (f setup.py ${EXTRA_FILES})
  set (ALLDEPENDS
    ${ALLDEPENDS} "${CMAKE_CURRENT_BINARY_DIR}/${f}")
endforeach  ()
foreach (f __init__.py ${PYTHON_FILES} ${TEST_FILES})
  set (ALLDEPENDS
    ${ALLDEPENDS} "${CMAKE_CURRENT_BINARY_DIR}/geographiclib/${f}")
endforeach  ()

set (SDIST dist/geographiclib-${PROJECT_VERSION}.tar.gz)
add_custom_command (OUTPUT ${SDIST}
  COMMAND ${Python_EXECUTABLE} -m build --sdist
  DEPENDS ${ALLDEPENDS}
  COMMENT "Creating source package")

set (WHEEL dist/geographiclib-${PROJECT_VERSION}-py2.py3-none-any.whl)
add_custom_command (OUTPUT ${WHEEL}
  COMMAND ${Python_EXECUTABLE} -m build --wheel
  DEPENDS ${ALLDEPENDS}
  COMMENT "Creating wheel")

add_custom_target (package ALL DEPENDS ${SDIST} ${WHEEL})

set (INSTALL_COMMAND
  "-m pip install -q --prefix ${CMAKE_INSTALL_PREFIX} ${SDIST}")
install (CODE
  "message (STATUS \"python ${INSTALL_COMMAND}\")")
install (CODE
  "execute_process(COMMAND ${Python_EXECUTABLE} ${INSTALL_COMMAND})")
