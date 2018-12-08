from flask import request, jsonify
from flask_restplus import Resource, Api

def add_predict(app, model):
    """adds predict route to flask application

    Assume that request is populated from form
    """
    
    api = Api(app)
    @api.route('/predict')
    class Predict(Resource):
        def post(self):
            form = model.gen_form()
            if form.validate_on_submit():
                X = [[form.data[i] for i in model.get_args()]]
                return jsonify({
                    "predict": model.predict(X).tolist()
                })
            else:
                return "error", 403
        
        def get(self):
            return model.name

    return app
