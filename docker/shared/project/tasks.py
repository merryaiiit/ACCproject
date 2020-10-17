from project.celery import app
from subprocess import call
import os

@app.task
def analyze(filename):
    call("cd ./murtazo/navier_stokes_solver/ && ./airfoil 10 0.0001 10. 1 ../cloudnaca/msh/" + filename, shell=True)
    # call("cp ./murtazo/navier_stokes_solver/results/drag_ligt.m /results/"+filename+"result.m")

    return 0
