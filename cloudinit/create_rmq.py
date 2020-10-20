# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ssc.xsmall"
private_net = "UPPMAX 2020/1-2 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 18.04"

loader = loading.get_plugin_loader('password')

#auth = loader.load_from_options(auth_url="https://east-1.cloud.snic.se:5000/v3",
  #                              username="s16071",
   #                             password="Sariel199524",
    #                            project_name="UPPMAX 2020/1-2",
     #                           project_id="fc1aade83c2e49baa7498b3918560d9f",
    #                            user_domain_name="snic")
    
auth = loader.load_from_options(auth_url="https://east-1.cloud.snic.se:5000/v3",
                                username="s17012",
                                password="An3y$h@31287",
                                project_name="UPPMAX 2020/1-2",
                                project_id="fc1aade83c2e49baa7498b3918560d9f",
                                user_domain_name="snic")

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/rmq-cloud.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default']

print("Creating instance ... ")
instance = nova.servers.create(name="g10-rmq", key_name="Aneysha_test_instance", image=image, flavor=flavor, userdata=userdata, nics=nics,security_groups=secgroups)
inst_status = instance.status
print("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status == 'BUILD':
    print("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print("Instance: "+ instance.name +" is in " + inst_status + "state")
