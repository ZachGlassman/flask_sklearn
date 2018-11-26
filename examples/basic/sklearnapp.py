from flask import Flask, render_template

from flask_sklearn.form import ScikitForm
from flask_sklearn.app import add_predict
from sklearn.linear_model import LinearRegression
from collections import OrderedDict
app = Flask(__name__)
app.config['SECRET_KEY'] = ';alskdjf;aldjkfqoiier'

model = ScikitForm.load('mod.joblib')

@app.route('/')
def index():
    form = model.gen_form()
    return render_template('index.html', form=form)

app = add_predict(app, model)

if __name__ == '__main__':
    app.run()
