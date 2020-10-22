echo "hello world! "
tar xzvf murtazo.tgz && cd murtazo
tar xvf cloudnaca.tgz && tar xvf navier_stokes_solver.tar
cd navier_stokes_solver/src && ./compile_forms
cd .. && cmake . && make -j 2
echo "Make --- finished"
cd ../cloudnaca && sudo apt-get update && sudo dpkg --configure -a
echo "apt-get updated"
sudo apt-get install -y gmsh && sudo apt install -y python-numpy
./runme.sh 0 30 10 200 2 && cd ./msh 

sfx=".xml"
for file in *
do
    name=${file%.msh}
    echo "${file}"
    echo "${name}${sfx}"
    dolfin-convert "${file}" "${name}${sfx}"
done

sudo cp ./* /meshes/
cd /home/fenics/shared/
sed 's,to_be_replaced,'"${RMQIP}"',g' ./worker-cloud.txt | sudo tee ./worker-cloud.txt
celery -A project worker & python3 -m project.run & sleep infinity
