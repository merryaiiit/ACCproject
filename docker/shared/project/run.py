from flask import Flask, request
from flask_restful import Resource, Api

from .tasks import analyze
import time
import os
from random import sample
from math import ceil
app = Flask(__name__)
api = Api(app)

def get_nova_creds():
    d = {}
    d['version']='2.1'
    d['username'] ="s17012"
    d['password'] ="An3y$h@31287"
    d['auth_url'] ="https://east-1.cloud.snic.se:5000/v3"
    d['project_id'] ="fc1aade83c2e49baa7498b3918560d9f"
    return d

def create_vm(vmname):
    # http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
    import time, os, sys
    import inspect
    from os import environ as env

    from  novaclient import client
    import keystoneclient.v3.client as ksclient
    from keystoneauth1 import loading
    from keystoneauth1 import session

    flavor = "ssc.medium"
    private_net = "UPPMAX 2020/1-2 Internal IPv4 Network"
    floating_ip_pool_name = None
    floating_ip = None
    image_name = "Ubuntu 18.04"

    loader = loading.get_plugin_loader('password')

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
    cfg_file_path =  os.getcwd()+'/worker-cloud.txt'
    if os.path.isfile(cfg_file_path):
        userdata = open(cfg_file_path)
    else:
        sys.exit("cloud-cfg.txt is not in current working directory")

    secgroups = ['default']

    print("Creating instance ... ")
    instance = nova.servers.create(name="g10-"+vmname, key_name="liju_remote", image=image, flavor=flavor, userdata=userdata, nics=nics,security_groups=secgroups)
    inst_status = instance.status
    print("waiting for 10 seconds.. ")
    time.sleep(10)

    while inst_status == 'BUILD':
        print("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
        time.sleep(5)
        instance = nova.servers.get(instance.id)
        inst_status = instance.status

    print("Instance: "+ instance.name +" is in " + inst_status + "state")
    return instance

def delete_vm(vmname):
    from  novaclient import client
    import keystoneclient.v3.client as ksclient
    from keystoneauth1 import loading
    from keystoneauth1 import session


    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url="https://east-1.cloud.snic.se:5000/v3",
                                    username="s17012",
                                    password="An3y$h@31287",
                                    project_name="UPPMAX 2020/1-2",
                                    project_id="fc1aade83c2e49baa7498b3918560d9f",
                                    user_domain_name="snic")

    sess = session.Session(auth=auth)
    print("user authorization completed.")
    creds = get_nova_creds()
    print("getting creds")
    nova = client.Client(**creds,session=sess)
    print("novaclient authorization complete")
    server = nova.servers.find(name= vmname)
    print(vmname)
    server.delete()
    print("Instance deleted")	


class Analyze(Resource):
    def get_all(self, num):
        threshhold = 10
        all = os.listdir("./murtazo/cloudnaca/msh/")
        # Skip msh files
        all_files = []
        for file in all:
            if ".msh" in file:
                continue
            all_files.append(file)
        # Sample requested files from all files
        files = sample(all_files, num)
        num_worker = ceil(len(files)/threshhold)-1

        instances = []
        for i in range(num_worker):
           instances.append(create_vm("worker"+str(i)))

        results = []
        # Submit tasks to celery
        for file in files:
            results.append(analyze.delay(file))
        # Waits for the tasks to be done
        finished = 0
        while finished != len(results):
            print("waiting...")
            time.sleep(3)
            finished = sum(map(lambda a: a.ready(), results))
            print("Now finished:", finished, "/", len(results))

            # TODO: delete newly-created VMs, objects stored in list instances
        for i in range(num_worker):
            delete_vm("worker"+str(i))    
        print("hello world!")
        return 0

    def get(self, num):
        return self.get_all(num)

api.add_resource(Analyze, '/<int:num>')
if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
