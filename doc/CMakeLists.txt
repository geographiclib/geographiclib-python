file (GLOB SOURCES *.rst conf.py ../geographiclib/*.py)
add_custom_target (doc ALL
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/html/index.html)
add_custom_command (OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/html/index.html
  DEPENDS ${SOURCES}
  COMMAND ${SPHINX} -v -b html ${CMAKE_CURRENT_SOURCE_DIR} html > pythondoc.log
  COMMENT "Generating documentation tree")
