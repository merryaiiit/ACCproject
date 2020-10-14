from project.celery import app
from subprocess import call
import os

@app.task
def analyze(filename):
    call("cd ../murtazo/navier_stokes_solver/ && ./airfoil 10 0.0001 10. 1 ../cloudnaca/msh/" + filename, shell=True)
    call("scp ../murtazo/navier_stokes_solver/results/drag_ligt.m ubuntu@"+os.environ['BASEIP']+":/home/ubuntu/.")

    return 0
