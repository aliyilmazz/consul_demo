import flask, os, socket, subprocess, requests, json, consul
from flask import Flask

SELF_HOSTNAME = str(socket.gethostname())
SELF_IP = socket.gethostbyname(SELF_HOSTNAME)

# fetch consul's ip, so that we can talk to it.
CONSUL_ALIAS = 'consul'
CONSUL_PORT = '8500'
CONSUL_IP = subprocess.check_output(['getent', 'hosts', CONSUL_ALIAS]).decode().split()[0]

consul_registry = {
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

# create consul instance (not agent, just python instance)
c = consul.Consul(host=CONSUL_IP, port=CONSUL_PORT)

# get rabbitmq IP
keyindex, rabbitmq_ip_bytes = c.kv.get('rabbitmq')
keyindex, redis_ip_bytes = c.kv.get('redis')
keyindex, mongodb_ip_bytes = c.kv.get('mongodb')

rabbitmq_ip = rabbitmq_ip_bytes['Value'].decode()
redis_ip = redis_ip_bytes['Value'].decode()
mongodb_ip = mongodb_ip_bytes['Value'].decode()

# add webservice to catalog
c.catalog.register('flaskapp-node', SELF_IP, service=consul_registry, dc='dc1')


app = Flask(__name__)

@app.route('/')
def hello_world():
    text = """Welcome to Guvenlik-Kontrol webservice. <br>
              Host ID: %s <br>
              RabbitMQ IP: %s <br>
              Redis IP: %s <br>
              MongoDB IP: %s <br>

              Consul rocks!""" % (SELF_HOSTNAME, rabbitmq_ip, redis_ip, mongodb_ip)
    return text, 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
