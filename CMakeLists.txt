project (GeographicLib-Python NONE)

# Version information
set (PROJECT_VERSION_MAJOR 2)
set (PROJECT_VERSION_MINOR 0)
set (PROJECT_VERSION_PATCH 0)
set (PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}")
if (PROJECT_VERSION_PATCH GREATER 0)
  set (PROJECT_VERSION "${PROJECT_VERSION}.${PROJECT_VERSION_PATCH}")
endif ()

cmake_minimum_required (VERSION 3.13.0)

# Set a default build type for single-configuration cmake generators if
# no build type is set.
if (NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set (CMAKE_BUILD_TYPE Release)
endif ()

add_subdirectory (geographiclib)

enable_testing ()
# Run the test suite
add_test (NAME python2
  COMMAND python2 -m unittest -v geographiclib.test.test_geodesic
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
add_test (NAME python3
  COMMAND python3 -m unittest -v geographiclib.test.test_geodesic
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})

# The documentation depends on doxygen.
if (BUILD_DOCUMENTATION)
  # For Python documentation
  find_program (SPHINX sphinx-build REQUIRED)
  add_subdirectory (doc)
endif ()
