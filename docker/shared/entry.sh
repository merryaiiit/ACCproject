sed 's,to_be_replaced,'"${RMQIP}"',g' ./entry-cloud.txt | sudo tee ./worker.txt
pip3 install python-novaclient
pip3 install python-keystoneclient
celery -A project worker & python3 -m project.run & sleep infinity
