from project.celery import app
import os

@app.task
def analyze(filename):
    os.system("rm -f ./murtazo/navier_stokes_solver/results/*")
    os.system("cd ./murtazo/navier_stokes_solver/ && ./airfoil 10 0.0001 10. 1 /meshes/" + filename)
    os.system("cp ./murtazo/navier_stokes_solver/results/drag_ligt.m /results/"+filename.split(sep='.')[0]+"_result.m")

    return 0
