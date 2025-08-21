Python package
==============

Installation
------------

The full `GeographicLib <../../index.html>`_ package
can be downloaded from
`sourceforge
<https://sourceforge.net/projects/geographiclib/files/distrib-Python>`_.
However the python implementation is available as a stand-alone package.
To install this, run

.. code-block:: sh

  pip install geographiclib

Alternatively downloaded the source package directly from
`Python Package Index <https://pypi.org/project/geographiclib/>`_
and install it with

.. code-block:: sh

  pip install geographiclib-2.0.tar.gz

It's a good idea to run the unit tests to verify that the installation
worked OK by running

.. code-block:: sh

  python -m unittest geographiclib.test.test_geodesic

Other links
-----------

* Library documentation (all versions):
  `https://geographiclib.sourceforge.io/Python <..>`_
* Git repository: https://github.com/geographiclib/geographiclib-python
  Releases are tagged in git as, e.g., v1.52, v2.0, etc.
* Source distribution:
  https://sourceforge.net/projects/geographiclib/files/distrib-Python
* GeographicLib:
  `https://geographiclib.sourceforge.io <../../index.html>`_
* The library has been implemented in a few other
  `languages <../../doc/library.html#languages>`_

Change log
----------

* Version 2.1 (released 2025-08-21)

* Version 2.0 (released 2022-04-23)

  * Minimum version of Python supported in 3.7.  Support for Python 2.x
    has been dropped.
  * This is a major reorganization with the Python package put into its own
    git repository, https://github.com/geographiclib/geographiclib-python.
    Despite this, there are only reasonably minor changes to the package
    itself.
  * Fix bug where the solution of the inverse geodesic problem with φ\
    :sub:`1` = 0 and φ\ :sub:`2` = nan was treated as equatorial.
  * More careful treatment of ±0° and ±180°.

    * These behave consistently with taking the limits

      * ±0 means ±ε as ε → 0+
      * ±180 means ±(180 − ε) as ε → 0+
    * As a consequence, azimuths of +0° and +180° are reckoned to be
      east-going, as far as tracking the longitude with
      Geodesic.LONG_UNROLL and the area goes, while azimuths −0° and
      −180° are reckoned to be west-going.
    * When computing longitude differences, if λ\ :sub:`2` − λ\ :sub:`1`
      = ±180° (mod 360°), then the sign is picked depending on the sign
      of the difference.
    * The normal range for returned longitudes and azimuths is
      [−180°, 180°].
    * A separate test suite test_sign has been added to check this
      treatment.

* Version 1.52 (released 2021-06-22)

  * Work around inaccurate math.hypot for python 3.[89]
  * Be more aggressive in preventing negative s12 and m12 for short
    lines.

* Version 1.50 (released 2019-09-24)

  * PolygonArea can now handle arbitrarily complex polygons.  In the
    case of self-intersecting polygons the area is accumulated
    "algebraically", e.g., the areas of the 2 loops in a figure-8
    polygon will partially cancel.
  * Fixed bug in counting pole encirclings when adding edges to a
    polygon.
  * Work around problems caused by sin(inf) and fmod(inf) raising
    exceptions.
  * Math.cbrt, Math.atanh, and Math.asinh now preserve the sign of −0.

* Version 1.49 (released 2017-10-05)

  * Fix code formatting; add tests.

* Version 1.48 (released 2017-04-09)

  * Change default range for longitude and azimuth to (−180°, 180°]
    (instead of [−180°, 180°)).

* Version 1.47 (released 2017-02-15)

  * Fix the packaging, incorporating the patches in version 1.46.3.
  * Improve accuracy of area calculation (fixing a flaw introduced in
    version 1.46)

* Version 1.46 (released 2016-02-15)

  * Add Geodesic.DirectLine, Geodesic.ArcDirectLine,
    Geodesic.InverseLine, GeodesicLine.SetDistance, GeodesicLine.SetArc,
    GeodesicLine.s13, GeodesicLine.a13.
  * More accurate inverse solution when longitude difference is close to
    180°.
  * Remove unnecessary functions, CheckPosition, CheckAzimuth,
    CheckDistance.
