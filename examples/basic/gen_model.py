from collections import OrderedDict
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegressionCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from flask_sklearn.form import sklearn_form

data = load_iris()
X = data['data']
y = data['target']

form_func = sklearn_form(OrderedDict((i, 1) for i in data['feature_names']))

lr_params = dict(
    Cs=[1,2,3,5],
    cv=5,
    multi_class='auto'
)

model = form_func(Pipeline([
    ('scale', StandardScaler()),
    ('lr', LogisticRegressionCV(**lr_params))
]))

def main():
    model.fit(X, y)

    model.save('mod.joblib')

if __name__ == '__main__':
    main()
