echo "hello world! "
tar xzvf murtazo.tgz && cd murtazo
tar xvf navier_stokes_solver.tar
cd navier_stokes_solver/src && ./compile_forms
cd .. && cmake . && make -j 2
echo "Make --- finished"

celery -A project worker & sleep infinity
