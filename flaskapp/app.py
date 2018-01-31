import flask, os, socket, subprocess, requests, json
from flask import Flask

SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'

# fetch consul's ip, so that we can talk to it.
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]

consul_registry = {
"Node":"flaskapp-node",
"Address":SELF_IP,
"Datacenter":"dc1",
  "Service": {
    "id":SELF_HOSTNAME,
    "name": "flaskapp",
    "service": "flaskapp",
    "tags": [
    "traefik.enable=true",
    "traefik.frontend.entryPoints=http",
    "traefik.frontend.rule=Host:localhost"],
    "address":SELF_IP,
    "port": 5000
    }
    }

# PUT webservice registry
response = requests.put("http://"+ CONSUL_IP + ":" + CONSUL_PORT + "/v1/catalog/register", data=json.dumps(consul_registry))

# GET service IPs from Consul-KV
params = ( ('raw', ''), )
rabbitmq_ip = requests.get("http://"+ CONSUL_IP + ":" + CONSUL_PORT + "/v1/kv/rabbitmq", params=params).content.decode()
redis_ip = requests.get("http://"+ CONSUL_IP + ":" + CONSUL_PORT + "/v1/kv/redis", params=params).content.decode()


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Welcome to Guvenlik-Kontrol webservice.\nHost ID: " + str(SELF_HOSTNAME) + "\nRabbitMQ IP: " + str(rabbitmq_ip) + "\nRedis IP: " + str(redis_ip)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
