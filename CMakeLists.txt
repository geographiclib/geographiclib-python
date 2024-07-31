cmake_minimum_required (VERSION 3.13.0)
project (GeographicLib-Python NONE)

# The project name for python
set (PYTHON_PROJECT_NAME geographiclib)

# Version information
set (PROJECT_VERSION_MAJOR 2)
set (PROJECT_VERSION_MINOR 0)
set (PROJECT_VERSION_PATCH 1)
set (PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}")
if (PROJECT_VERSION_PATCH GREATER 0)
  set (PROJECT_VERSION "${PROJECT_VERSION}.${PROJECT_VERSION_PATCH}")
endif ()
# Follow Python conventions on the version suffix: {a,b,rc}N, see
# https://www.python.org/dev/peps/pep-0440
set (PROJECT_VERSION_SUFFIX "dev1")
set (PROJECT_FULLVERSION "${PROJECT_VERSION}${PROJECT_VERSION_SUFFIX}")

set (RELEASE_DATE "2022-04-23")

# Set a default build type for single-configuration cmake generators if
# no build type is set.
if (NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set (CMAKE_BUILD_TYPE Release)
endif ()

configure_file (setup.cfg.in setup.cfg @ONLY)
set (EXTRA_FILES README.md LICENSE pyproject.toml)
foreach (f ${EXTRA_FILES})
  configure_file (${f} ${f} COPYONLY)
endforeach ()

# Minimum version of Python supported in 3.7 (for math.remainder).  Next
# update will be to 3.10 (to catch the fix in math.hypot).
set (Python_VERSION_NUMBER 3.7 CACHE STRING "The minimum version of Python")
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
foreach (f setup.cfg ${EXTRA_FILES})
  set (ALLDEPENDS
    ${ALLDEPENDS} "${CMAKE_CURRENT_BINARY_DIR}/${f}")
endforeach  ()
foreach (f __init__.py ${PYTHON_FILES} ${TEST_FILES})
  set (ALLDEPENDS
    ${ALLDEPENDS} "${CMAKE_CURRENT_BINARY_DIR}/geographiclib/${f}")
endforeach  ()

set (SDIST dist/${PYTHON_PROJECT_NAME}-${PROJECT_FULLVERSION}.tar.gz)
set (WHEEL dist/${PYTHON_PROJECT_NAME}-${PROJECT_FULLVERSION}-py3-none-any.whl)
add_custom_command (OUTPUT ${SDIST} ${WHEEL}
  COMMAND ${Python_EXECUTABLE} -m build
  DEPENDS ${ALLDEPENDS}
  COMMENT "Creating packages")

add_custom_target (package ALL DEPENDS ${SDIST} ${WHEEL})

add_custom_target (deploy-package
  COMMAND ${Python_EXECUTABLE} -m twine upload ${SDIST} ${WHEEL}
  DEPENDS package)

set (INSTALL_COMMAND
  "-m pip install -q --prefix ${CMAKE_INSTALL_PREFIX} ${WHEEL}")
install (CODE
  "message (STATUS \"python ${INSTALL_COMMAND}\")")
install (CODE
  "execute_process (COMMAND ${Python_EXECUTABLE} ${INSTALL_COMMAND})")

if (IS_DIRECTORY ${PROJECT_SOURCE_DIR}/.git AND NOT WIN32)
  add_custom_target (checktrailingspace
    COMMAND git ls-files | xargs grep ' $$' || true
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    COMMENT "Looking for trailing spaces")
  add_custom_target (checktabs
    COMMAND git ls-files | xargs grep '\t' || true
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    COMMENT "Looking for tabs")
  add_custom_target (checkblanklines
    COMMAND git ls-files |
    while read f\; do tr 'X\\n' 'YX' < $$f |
    grep -E '\(^X|XXX|XX$$|[^X]$$\)' > /dev/null && echo $$f\; done || true
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    COMMENT "Looking for extra blank lines")

  add_custom_target (sanitize)
  add_dependencies (sanitize checktrailingspace checktabs checkblanklines)

  find_program (RSYNC rsync)
  if (IS_DIRECTORY ${PROJECT_SOURCE_DIR}/distrib-Python AND RSYNC)
    set (USER karney)
    set (DATAROOT $ENV{HOME}/web/geographiclib-files/distrib-Python)
    set (DOCROOT $ENV{HOME}/web/geographiclib-web/htdocs/Python)
    set (FRSDEPLOY ${USER}@frs.sourceforge.net:/home/frs/project/geographiclib)
    set (WEBDEPLOY ${USER},geographiclib@web.sourceforge.net:./htdocs)

    add_custom_target (stage-dist
      COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${SDIST} ${WHEEL} ${PROJECT_SOURCE_DIR}/distrib-Python/
      COMMAND ${RSYNC} --delete -av --exclude '*~'
        ${PROJECT_SOURCE_DIR}/distrib-Python/ ${DATAROOT}/)
    add_dependencies (stage-dist package)

    if (SPHINX)
      add_custom_target (stage-doc
        COMMAND ${RSYNC} --delete -a
        doc/html/ ${DOCROOT}/${PROJECT_VERSION}/)
      add_dependencies (stage-doc doc)
    endif ()

    add_custom_target (deploy-dist
      COMMAND ${RSYNC} --delete -av ${DATAROOT} ${FRSDEPLOY}/)
    add_custom_target (deploy-doc
      COMMAND ${RSYNC} --delete -av -e ssh ${DOCROOT} ${WEBDEPLOY}/)
  endif ()
endif ()
