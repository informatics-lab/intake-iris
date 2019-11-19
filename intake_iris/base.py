from . import __version__
from intake.source.base import DataSource, Schema

import warnings

import iris
from iris.cube import CubeList


class DataSourceMixin(DataSource):
    """Common behaviours for plugins in this repo"""
    version = __version__
    container = 'iris'
    partition_access = True

    def _open_dataset(self):
        with warnings.catch_warnings():
            warnings.simplefilter(self.warnings)
            if self._iris_object == 'iris-cube':
                self._ds = iris.load_cube(self.urlpath, **self._kwargs)
                self.IrisObjSource = CubeSource(self._ds)
            else:
                self._ds = iris.load(self.urlpath, **self._kwargs)
                self.IrisObjSource = CubeListSource(self._ds)

    def _get_schema(self):
        """Make schema object, which embeds iris object and some details"""
        if self._ds is None:
            self._open_dataset()
        return self.IrisObjSource._get_schema()

    def read(self):
        """Load entire dataset into a container and return it"""
        self._load_metadata()
        return self._ds

    def read_chunked(self):
        """Return iterator over container fragments of data source"""
        self._load_metadata()
        return self.read()

    def read_partition(self, i):
        """Return a part of the data corresponding to i-th partition.

        By default, assumes i should be an integer between zero and npartitions;
        override for more complex indexing schemes.
        """
        self._load_metadata()
        return self.IrisObjSource.read_partition(i)

    def to_dask(self):
        """Return a dask container for this data source"""
        self._load_metadata()
        return self.IrisObjSource.to_dask()

    def close(self):
        """Delete open file from memory"""
        self._ds = None
        self._schema = None


class CubeSource(object):
    def __init__(self, cube):
        self.cube = cube

    def _get_schema(self):
        """Make schema object, which embeds iris cube and some details"""
        metadata = {}
        self._schema = Schema(
            datashape=self.cube.shape,
            dtype=self.cube.dtype,
            shape=self.cube.shape,
            npartitions=self.cube.lazy_data().chunks,
            extra_metadata=metadata)
        return self._schema

    def read_partition(self, i):
        return self.cube[i]

    def to_dask(self):
        return self.cube.lazy_data()


class CubeListSource(object):
    def __init__(self, cubelist):
        self.cubelist = cubelist

    def _get_schema(self):
        """Make schema object, which embeds iris cubelist and some details"""
        metadata = {}
        self._schema = Schema(
            datashape=None,
            dtype=None,
            shape=len(self.cubelist),
            npartitions=len(self.cubelist),
            extra_metadata=metadata)
        return self._schema

    def read_partition(self, i):
        return self.cubelist[i]

    def to_dask(self):
        raise NotImplementedError