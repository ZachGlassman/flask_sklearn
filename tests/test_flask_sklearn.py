#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `flask_sklearn` package."""

import pytest
from sklearn.linear_model import LinearRegression
from flask_sklearn import form

data_cols = ['a', 'b']
X = [[1, 2], [5, 6], [7, 8]]
y = [1, 2, 3]


@pytest.fixture
def abform():
    return form.sklearn_form(**{'a':1, 'b':1})

def test_invalid_data(abform):
    est = abform(LinearRegression)()
    with pytest.raises(ValueError):
        est.fit([[1, 2, 3], [1, 2, 3]], [1, 2])
