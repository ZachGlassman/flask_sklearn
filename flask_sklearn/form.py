# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField

def gen_wtf_form(**kwargs):
    class Form(FlaskForm):
        pass
    for key, value in kwargs.items():
        if isinstance(value, str):
            setattr(Form, key, StringField(key))
        else:
            setattr(Form, key, FloatField(key))
    return Form

def sklearn_form(**kwargs):
    def f(sklearn_class):
        """generates a flask_wtf form from a sklearn class"""
        class Cls(sklearn_class):
            def gen_form(self):
                return gen_wtf_form(**kwargs)

            def _check_cols(self, X):
                return len(X[0]) == len(kwargs)

            def fit(self, X, y):
                """additional check on shape of X"""
                if not self._check_cols(X):
                    raise ValueError("Shape of Input data doesn't match form")
                return super().fit(X, y)

        Cls.__name__ = sklearn_class.__name__ + '_Form'
        return Cls
    return f


