# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from collections import OrderedDict
from sklearn.externals import joblib

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

def sklearn_form(ordered_args):
    def f(sklearn_class):
        """generates a flask_wtf form from a sklearn class"""
        class Cls(sklearn_class):
            def gen_form(self):
                return gen_wtf_form(ordered_args)

            def _check_cols(self, X):
                return len(X[0]) == len(ordered_args)

            def get_args(self):
                return list(ordered_args)

            def fit(self, X, y):
                """additional check on shape of X"""
                if not self._check_cols(X):
                    raise ValueError("Shape of Input data doesn't match form")
                return super().fit(X, y)

            def save(self, path):
                joblib.dump(self, path)

            @staticmethod
            def load(path):
                return joblib.load(path)

        Cls.__name__ = sklearn_class.__name__ + '_Form'
        return Cls
    return f


