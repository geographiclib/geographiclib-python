# setup.py, config file for distutils
#
# To install this package, execute
#
#   python setup.py install
#
# in this directory.  To upload the latest version to the python reposity run
#
#   python setup.py sdist --formats gztar,zip upload
#
# The initial version of this file was provided by
# Andrew MacIntyre <Andrew.MacIntyre@acma.gov.au>.
#
# $Id: 12bd54636c048825af9c9bfa33adc2eec4330a31 $

from distutils.core import setup

setup(name="geographiclib",
      version="1.16",
      description=
        "A translation of the GeographicLib::Geodesic class to Python",
      author="Charles Karney",
      author_email="charles@karney.com",
      url="http://geographiclib.sourceforge.net/",
      packages=["geographiclib"],
      data_files=[],
      license="MIT",
      keywords="gis geographical earth distance geodesic",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Scientific/Engineering :: GIS",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      )
