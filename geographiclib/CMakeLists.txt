configure_file (__init__.py.in __init__.py @ONLY)
foreach (f ${PYTHON_FILES} ${TEST_FILES})
  configure_file (${f} ${f} COPYONLY)
endforeach ()

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
    --max-public-methods=34
    --min-public-methods=0
    --min-similarity-lines=9
    --max-nested-blocks=10
    --max-positional-arguments=16
    --argument-naming-style=any
    --attr-naming-style=any
    --method-naming-style=any
    --variable-naming-style=any
    --indent-string=${INDENT}
    # C0321 multiple statements on one line (needed for brevity)
    # C0325 unnecessary parens after 'not' keyword (needed for clarity)
    # C0415 import outside toplevel (needed because of
    #   Geodesic+ GeodesicLine interdependency)
    # R0124 comparison with self (needed for nan test)
    # R0401 Cyclic import
    # W0212 access to a protected member
    -d C0321,C0325,C0415,R0124,R0401,W0212
    __init__.py ${PYTHON_FILES} ${TEST_FILES}
    COMMENT "Linting with ${LINT}")
endif ()
