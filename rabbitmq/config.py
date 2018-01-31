import os, socket, requests, json, ast, subprocess, consul
from subprocess import call
SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)

# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]

# create consul instance (not agent, just python instance)
c = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)

# add kv
RABBITMQ_IP = SELF_IP
RABBITMQ_PORT = '5672'
REGISTRY = ':'.join([RABBITMQ_IP, RABBITMQ_PORT])
c.kv.put('rabbitmq', REGISTRY)

# start service
call(["./init.sh"])
