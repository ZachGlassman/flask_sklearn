from flask import request, jsonify

def add_predict(app, model):
    """adds predict route to flask application

    Assume that request is populated from form
    """
    @app.route('/predict', methods=['POST'])
    def predict():
        form = model.gen_form()
        if form.validate_on_submit():
            X = [[form.data[i] for i in model.get_args()]]
            return jsonify({
                "predict": model.predict(X).tolist()
            })
        else:
            return "error", 403

    return app
