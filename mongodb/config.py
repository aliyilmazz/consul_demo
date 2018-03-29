import os, socket, requests, json, ast, subprocess, consul
from subprocess import call
SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)

# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]

# create consul instance (not consul agent, just python instance)
c = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)

# add kv
MONGODB_IP = SELF_IP
MONGODB_PORT = '27017'
REGISTRY = ':'.join([MONGODB_IP, MONGODB_PORT])
c.kv.put('mongodb', REGISTRY)

# start service
call(["mongod", "--bind_ip_all"])
