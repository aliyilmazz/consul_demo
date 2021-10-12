# Foreword

in this branch, I provided playground with 7 containers:

* 3 consul container
* 3 service (redis,mongodb,rabbitmq)
* 1 webservice (flaskapp)

their start commands are overridden with `CMD ["/bin/sh"]` so that they do not run anything on start.
it is intentionally left for you to start them manually.

for consul connections, `python-consul` library is used. official docs [here](https://python-consul.readthedocs.io/en/latest/)

# Requirements

docker, python, docker-compose, consul

# Instructions


## 0. clone repo

```
$ git clone git@github.com:aliyilmazz/consul_demo.git
$ cd consul_demo
```

## 1. run containers
```
$ docker-compose up -d --build
```
now you should have 7 containers in tty mode (persistent), waiting in shell.


## 2. attach to consul containers

open 3 different terminal tabs. in each tab, attach to consul containers.

1st terminal for container labeled `consuldemo_consul_1` (this will be consul server)
```
$ docker exec -it consuldemo_consul_1 /bin/sh
```

2nd terminal for container labeled `consuldemo_consul_two_1` (this will be consul client)
```
$ docker exec -it consuldemo_consul_two_1 /bin/sh
```

3rd terminal for container labeled `consuldemo_consul_three_1` (this will be another consul client)
```
$ docker exec -it consuldemo_consul_three_1 /bin/sh
```


## 3. start consul agents

recall: in consul jargon, servers and clients are both known as `agent`s

in this step, we will start a server agent in `consuldemo_consul_1`, and two clients in `consuldemo_consul_two_1` and `consuldemo_consul_three_1`.

below are some useful notes before we run consul agents.

* **-server** (optional): this indicates that we run agent in server mode. without this flag, agent runs in client mode.   

* **-bootstrap-expect=1** (optional): this means we run server in **bootstrap** mode. without this flag, server needs to be redirected to an already-existing cluster, using -join flag. "-expect-1" part is optional. (-bootstrap would be enough, too)

* **-client=0.0.0.0** (optional): this means that cluster can accept requests from any IP. without this flag, only  processes in localhost can send query to this cluster. thus, this flag is required for almost all setups.

* **-ui** (optional): this flag enables Web User Interface. (localhost:8500).
    * Important: without this flag, we can still use RESTful HTTP API

* **-data-dir** (required) : this flag is required for all setups. we provide a (preferably empty) directory so that consul agent can place its node metadata and runtime configuration inside this directory.

* **-node** (optional) : assign name to agent.

  ​

that being said, let's run our agents.



* consuldemo_consul_1 shell:

```
$ mkdir /var/lib/consul
$ consul agent -server -bootstrap-expect=1 -client=0.0.0.0 -ui -data-dir=/var/lib/consul -node consul-server
```

now let's see consul agents using command `consul members`. The result should look like this:

```
$ docker exec consuldemo_consul_1 consul members
Node           Address          Status  Type    Build  Protocol  DC   Segment
consul-master  172.25.0.3:8301  alive   server  1.0.2  2         dc1  <all>
```

results state that a server agent named `consul-master` is running at `172.25.0.3`. Save this IP because following agents will need it to join `consul-master`'s cluster.

* consuldemo_consul_two_1 shell:

```
$ mkdir /var/lib/consul
$ consul agent -client=0.0.0.0 -ui -data-dir=/var/lib/consul -node consul-client1 -join <CONSUL_1 IP HERE>
```

* consuldemo_consul_three_1 shell:

```
$ mkdir /var/lib/consul
$ consul agent -client=0.0.0.0 -data-dir=/var/lib/consul -node consul-client2 -join <CONSUL_1 IP HERE>
```

now you should have a working consul cluster with 1 server and 2 clients. notice that in consuldemo_consul_1's agent logs, new clients are recognized with a message similar to this:

        2018/01/31 08:42:27 [INFO] serf: EventMemberJoin: consul-client1 172.25.0.4
        2018/01/31 08:42:27 [INFO] consul: member 'consul-client1' joined, marking health alive
        2018/01/31 08:44:01 [INFO] serf: EventMemberJoin: consul-client2 172.25.0.3
        2018/01/31 08:44:01 [INFO] consul: member 'consul-client2' joined, marking health alive

in order to see consul members, let's send `consul members` command to containers from a new terminal tab:
```
$ docker exec consul_demo_consul_1 consul members
```
after typing that, you should see terminal output similar to this:

```
$ docker exec consuldemo_consul_1 consul members
Node            Address          Status  Type    Build  Protocol  DC   Segment
consul-master   172.25.0.3:8301  alive   server  1.0.2  2         dc1  <all>
consul-client1  172.25.0.2:8301  alive   client  1.0.2  2         dc1  <default>
consul-client2  172.25.0.4:8301  alive   client  1.0.2  2         dc1  <default>

```

note: `consul members` command is available from all members of cluster. In other words, you can replace docker container name in the docker execution command above, with any other container that runs a consul agent.

consul web ui is available at localhost:18500 (see docker inspect port bindings)

we also used -ui flag in consul_two_1, so web ui is available on client named `consul-client1` as well. visit localhost:18501 to see webui. server and client webUIs are almost always synchronized because clients/servers gossip to each other periodically. notice that in consul-client2 we didn't use -ui flag. try to visit localhost:18502, you will see that there is only `Consul Agent` message in homepage. It means that it does not serve user interface, but it is still available to HTTP API calls.



in the next steps, we will register our services to this consul cluster.


## 4. attach to services' containers

so far, we have set our consul cluster up and working.

next, we will follow a similar procedure to deploy our services.

open up another 3 terminal tabs. in each terminal tab, attach to redis,mongodb,rabbitmq containers:

* redis terminal:

```
$ docker exec -it consuldemo_redis_1 /bin/bash
```

- rabbitmq terminal:

```
$ docker exec -it consuldemo_rabbitmq_1 /bin/bash
```

- mongodb terminal:

```
$ docker exec -it consuldemo_mongodb_1 /bin/bash
```

important note:
in consul containers, we had alpine distribution. alpine doesnt support `/bin/bash` so we used `/bin/sh` in step 2. now we have ubuntu on the rest of containers, so we can use `/bin/bash` on step 4 and 6.



## 5. register and start services

in each container, there is a configuration module named `config.py`. This script is no more than 10 lines. It basically fetches consul_ip using `getent hosts consul` command, then registers service using `python-consul` functions. I strongly recommend you to take a look at those scripts.

* redis terminal:
```
$ python3 config.py
```

- rabbitmq terminal:
```
$ chmod +x init.sh
$ python3 config.py
```

- mongodb terminal:
```
$ python3 config.py
```

now all services are started. visit consul WebUI at localhost:18500 and check KV section to see registered KV pairs.

note: in `docker-compose.yml` file, we declared a `link` to consul from all containers. this way, we can access consul's IP using `getent hosts consul` command. without that link, we can't resolve consul's IP address from hostname.


## 6. start flask application

so far, we launched consul and registered our services. now we can finally use consul for service discovery.

let's suppose flask application needs to know about rabbitmq, redis, mongodb services.

open one final terminal tab. in this tab, attach to flaskapp container with the command below:
```
$ docker exec -it consuldemo_flaskapp_1 /bin/bash
```
once you are attached, type `python3 app.py` to start flask application.

visit localhost:5000 to see flaskapp working. in homepage, you should see that flask successfully obtained service IPs from consul.

feel free to check `app.py` as well. this module registers flaskapp service to consul catalogs first, then searches consul KV for redis, rabbitmq, mongodb IPs.

go to localhost:18500 and click on KV button, check key-value pairs to verify that flaskapp obtained correct IP numbers for those services. you can also check `services` tab to verify that flaskapp has successfully registered its service. now some other service is able to discover flaskapp service via HTTP API, using the queries below:

http://localhost:18500/v1/catalog/service/flaskapp

http://localhost:18501/v1/catalog/service/flaskapp

http://localhost:18502/v1/catalog/service/flaskapp


# Contact

for any questions/errors, contact yilmazalimetu@gmail.com
