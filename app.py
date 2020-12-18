from logging import error
from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from pickle import load
import json
import numpy as np


app = Flask(__name__)
api = Api(app)


################################################ Key Table Class ###########################


########################################## Importing model #########################
maModel = load(open("MaModel94", 'rb'))

################################################ Defining arguments that must be passes #############################
modelArgs = reqparse.RequestParser()

modelArgs.add_argument(
    "sex", type=int, help="sex value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "age", type=int, help="age value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "education", type=float, help="education value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "currentSmoker", type=int, help="currentSmoker value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "cigsPerDay", type=float, help="cigsPerDay value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "BPMeds", type=float, help="BPMeds value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "prevalentStroke", type=int, help="prevalentStroke value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "prevalentHyp", type=int, help="BPMeds value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "diabetes", type=int, help="diabetes value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "sysBP", type=float, help="sysBP value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "diaBP", type=float, help="diaBP value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "BMI", type=float, help="BMI value is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "heartRate", type=int, help="heartRate is required. Please refer to the documentation", required=True)
modelArgs.add_argument(
    "glucose", type=float, help="glucose value is required. Please refer to the documentation", required=True)


############################ class to convert message into JSON format ########################

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

#################################### Model Class for handling API prediction call ########################


class Model(Resource):
    def get(self):
        args = modelArgs.parse_args()
        try:
            v1 = int(args['sex'])
            v2 = int(args['age'])
            v3 = float(args['education'])
            v4 = int(args['currentSmoker'])
            v5 = float(args['cigsPerDay'])
            v6 = float(args['BPMeds'])
            v7 = int(args['prevalentStroke'])
            v8 = int(args['prevalentHyp'])
            v9 = int(args['diabetes'])
            v10 = float(args['sysBP'])
            v11 = float(args['diaBP'])
            v12 = float(args['BMI'])
            v13 = int(args['heartRate'])
            v14 = float(args['glucose'])
            response = maModel.predict(
                [[v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14]])
            result = {"status": 200,
                      "request URL": request.url,
                      "prediction": response[0]}
            result = json.dumps(result, cls=NumpyEncoder)
            return result, 200
        except:
            result = {"status": 400,
                      "request URL": request.url,
                      "error": "Please check the values passed. Please refer to the documentation."}
            result = json.dumps(result, cls=NumpyEncoder)
            return result, 400


api.add_resource(Model, '/predict')


####################################### Home screen ##########################
@app.route('/')
def Home():
    return '''<div style="font-family:sans-serif;
                         display:flex;
                         align-items:center;
                         justify-content:center;
                         flex-direction: column;
                         width:100%;
                         height:100%;">
              <div style="text-align:center;
                         background: lightgrey;
                         padding: 1rem 2rem;
                         border-radius: 10px">
              <h1 style="color: tomato">MA API.</h1>
              <p>Thanks for visiting.</p>
              <p>For further information refer to the documnentation.</p>
              </div>
              </div>'''


if __name__ == "__main__":
    app.run(debug=True)
