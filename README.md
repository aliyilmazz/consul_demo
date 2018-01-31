## Usage

clone repository
```
$ git clone git@gitlab.spp42.net:ali.yilmaz/consul-demo.git
$ cd consul_demo
```

checkout to branch
```
$ git checkout registrator
```


build image
```
$ docker-compose up -d --build
```

scale webservices
```
$ docker-compose scale web=5
```

After running commands above, visit:

- traefik webui: localhost:8080

- consul webui: localhost:8500 (consul should have 5 services under "web")

- web service access using traefik: localhost:8081
