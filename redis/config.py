import os, socket, requests, json, ast, subprocess
from subprocess import call
SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'

# fetch consul's ip, so that we can talk to it.
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]

# Add KV via HTTP rest-api call to consul.
REDIS_IP = SELF_IP
REDIS_PORT = '6379'
REGISTRY = ':'.join([REDIS_IP, REDIS_PORT])
response = requests.put("http://" + CONSUL_IP + ":" + CONSUL_PORT + "/v1/kv/redis", data=REGISTRY)


call(["redis-server"])
