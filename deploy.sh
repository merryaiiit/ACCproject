sudo apt update && sudo apt -y install python3-pip
pip3 install python-novaclient && pip3 install python-keystoneclient
cd ./cloudinit && python3 create_rmq.py
