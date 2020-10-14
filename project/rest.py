from flask import Flask, request
from flask_restful import Resource, Api

from project import tasks
from .tasks import analyze
import time
import os, random

app = Flask(__name__)
api = Api(app)

class Analyze(Resource):


@app.route('/<int:num>', methods=['GET'])
def airfoil_result():

    return tasks.analyze(filename=).delay().get()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
