# -*- coding: utf-8 -*-
import numpy as np
import os
import pytest

from iris.cube import CubeList

from intake import open_catalog
from .util import dataset  # noqa


@pytest.fixture
def catalog1():
    path = os.path.dirname(__file__)
    return open_catalog(os.path.join(path, 'data', 'catalog.yaml'))


def test_catalog(catalog1, dataset):
    source = catalog1['iris_source'].get()
    ds = source.read()

    assert isinstance(ds, CubeList)
