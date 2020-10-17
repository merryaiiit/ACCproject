sed 's,to_be_replaced,'"${RMQIP}"',g' ./worker-cloud.txt | sudo tee ./worker-cloud.txt
celery -A project worker & python3 -m project.run & sleep infinity
