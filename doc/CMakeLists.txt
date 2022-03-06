set (FILES conf.py
  index.rst geodesics.rst interface.rst code.rst examples.rst)
set (SOURCES)
foreach (f ${SOURCES})
  set (SOURCES ${SOURCES} "../geographiclib/${f}")
endforeach ()

configure_file (conf.py . COPYONLY)

add_custom_target (doc DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/html/index.html)
add_custom_command (OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/html/index.html
  DEPENDS ${FILES} ${SOURCES}
  COMMAND ${SPHINX} -q -b html -d doctree -c . ${CMAKE_CURRENT_SOURCE_DIR} html
  COMMENT "Generating documentation tree")
