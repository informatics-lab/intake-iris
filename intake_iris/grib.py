# -*- coding: utf-8 -*-
from .base import DataSourceMixin


class GRIBSource(DataSourceMixin):
    """Open a netCDF file with iris.

    Parameters
    ----------
    urlpath: str or list
        Path to source file. May include glob "*" characters. Must be a
        location in the local file-system or opendap url.
    """
    name = 'grib'

    def __init__(self, urlpath, warnings='default', iris_kwargs=None, metadata=None,
                 **kwargs):
        self.urlpath = urlpath
        self.warnings = warnings
        self._kwargs = iris_kwargs or kwargs
        self._iris_object = self._kwargs.pop('iris-object', 'iris-cubelist')
        self._ds = None
        super(GRIBSource, self).__init__(metadata=metadata)
