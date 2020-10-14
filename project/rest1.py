from flask import Flask, request
from flask_restful import Resource, Api

from .tasks import analyze
import time
import os
from random import sample

app = Flask(__name__)
api = Api(app)

class Analyze(Resource):
    def get_all(self, num):
        all = os.listdir("../murtazo/cloudnaca/msh/")

        # Skip msh files
        all_files = []
        for file in all:
            if ".msh" in file:
                continue
            all_files.append(file)
       Sample requested files from all files
        files = sample(all_files, num)
        results = []

        # Submit tasks to celery
        for file in files:
            results.append(analyze.delay(file))

        # Waits for the tasks to be done
        finished = 0
        while (finished != len(results):
            print("waiting...")
            time.sleep(3)
            finished = sum(map(lambda a: a.ready(), results)
            print("Now finished: ", finished, "/", len(results)
        return "Done"

    def get(self, num):
        return self.get_all(num)

api.add_resource(Analyze, '/<int:num>')

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')