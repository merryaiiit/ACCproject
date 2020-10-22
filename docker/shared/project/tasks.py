from project.celery import app
from subprocess import call
import os

@app.task
def analyze(filename):
    call("rm -f ./murtazo/navier_stokes_solver/results/*")
    call("cd ./murtazo/navier_stokes_solver/ && ./airfoil 10 0.0001 10. 1 /meshes/" + filename, shell=True)
    call("cp ./results/drag_ligt.m /results/"+filename.split(sep='.')[0]+"_result.m")

    return 0
