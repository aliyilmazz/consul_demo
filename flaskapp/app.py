import flask, redis, os, socket
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
host = socket.gethostname()

@app.route('/')
def hello_world():
    return 'Welcome to Guvenlik-Kontrol webservice. Host ID: ' + str(host)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
