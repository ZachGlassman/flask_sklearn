#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `flask_sklearn.form`"""
import os
from datetime import datetime
from collections import OrderedDict
import pytest
from sklearn.linear_model import LinearRegression
from flask_sklearn import form
from flask import Flask
from flask_wtf import FlaskForm

data_cols = ['a', 'b']
X = [[1, 2], [5, 6], [7, 8]]
y = [1, 2, 3]


@pytest.fixture
def abform():
    return form.sklearn_form(OrderedDict((('a', 1),
                                          ('b', 1))))

@pytest.fixture
def est(abform):
    return abform(LinearRegression)

@pytest.fixture
def fit_est(est):
    return est.fit(X, y)

@pytest.fixture
def temp_file():
    filename = 'testing_{}'.format(datetime.now())
    yield filename
    os.remove(filename)

@pytest.fixture
def request():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super secret'

    context = app.test_request_context()
    context.push()
    yield app
    context.pop()

def test_invalid_data(est):
    with pytest.raises(ValueError):
        est.fit([[1, 2, 3], [1, 2, 3]], [1, 2])

def test_args(est):
    assert est.args == ['a', 'b']

def test_form_generate(request, fit_est):
    form = fit_est.gen_form()
    for ele in data_cols:
        assert getattr(form, ele)
    assert isinstance(form, FlaskForm)

def test_save_load(fit_est, temp_file):
    fit_est.save(temp_file)
    new_est = form.ScikitForm.load(temp_file)
    assert all(fit_est.model_attr('coef_') == new_est.model_attr('coef_'))
    assert type(fit_est._model) == type(new_est._model)
