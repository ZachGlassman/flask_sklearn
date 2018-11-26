# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from collections import OrderedDict
from sklearn.externals import joblib
from sklearn.base import BaseEstimator

def gen_wtf_form(ordered_args):
    if not isinstance(ordered_args, OrderedDict):
        raise ValueError("ordered_args must be OrderedDict")
    class Form(FlaskForm):
        pass
    for key, value in ordered_args.items():
        if isinstance(value, str):
            setattr(Form, key, StringField(key))
        else:
            setattr(Form, key, FloatField(key))
    return Form()

def validate_pickle(obj):
    obj.save('temporary')
    obj.load('temporary')

class ScikitForm:
    def __init__(self, model, ordered_args):
        self._model = model
        self._ordered_args = ordered_args

    def gen_form(self):
        # TODO check if not fitted
        form = gen_wtf_form(self._ordered_args)
        form.args_ = self._ordered_args
        return form

    def _check_cols(self, X):
        return len(X[0]) == len(self._ordered_args)

    def get_args(self):
        return list(self._ordered_args)

    def fit(self, X, y=None):
        """additional check on shape of X"""
        if not self._check_cols(X):
            raise ValueError("Shape of Input data doesn't match form")
        self._model.fit(X, y)
        return self

    def predict(self, X):
        return self._model.predict(X)

    def save(self, path):
        joblib.dump(self, path)

    @staticmethod
    def load(path):
        return joblib.load(path)

    def model_attr(self, attr):
        return getattr(self._model, attr)

def sklearn_form(ordered_args):
    def f(sklearn_class):
        """generates a flask_wtf form from a sklearn class"""
        model = sklearn_class if isinstance(sklearn_class, BaseEstimator) else sklearn_class()
        return ScikitForm(model, ordered_args)
    return f


