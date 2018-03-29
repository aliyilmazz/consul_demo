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

# Add KV via HTTP rest-api call to consul.
REDIS_IP = SELF_IP
REDIS_PORT = '6379'
REGISTRY = ':'.join([REDIS_IP, REDIS_PORT])
c.kv.put('redis', REGISTRY)

# start service
call(["redis-server"])
