echo "hello world! "
tar xzvf murtazo.tgz && cd murtazo
tar xvf cloudnaca.tgz && tar xvf navier_stokes_solver.tar
cd navier_stokes_solver/src && ./compile_forms
cd .. && cmake . && make -j 2
echo "Make --- finished"
cd ../cloudnaca && sudo apt-get update && sudo dpkg --configure -a
echo "apt-get updated"
sudo apt-get install -y gmsh && sudo apt install -y python-numpy
cd /home/fenics/shared/
sed 's,to_be_replaced,'"${RMQIP}"',g' ./worker-cloud.txt | sudo tee ./worker-cloud.txt
celery -A project worker & python3 -m project.run & sleep infinity
