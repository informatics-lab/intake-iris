from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .netcdf import NetCDFSource
from .grib import GRIBSource

import intake.container
