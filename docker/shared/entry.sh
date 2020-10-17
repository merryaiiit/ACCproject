sed 's,to_be_replaced,'"${RMQIP}"',g' ./entry-cloud.txt | sudo tee ./worker.txt
celery -A project worker & python3 -m project.run & sleep infinity
