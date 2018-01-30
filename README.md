## Usage

clone repository
```
$ git clone git@gitlab.spp42.net:ali.yilmaz/guvenlik-kontrol.git
$ cd guvenlik-kontrol
```

checkout to branch
```
$ git checkout registrator_demo
```

build image
```
$ docker-compose up -d --build
```

scale webservices
```
$ docker-compose scale web=5
```


After Execution, visit:

- traefik webui: localhost:8080

- consul webui: localhost:8500 (consul should have 5 services under "web")

- web service access using traefik: localhost:8081
