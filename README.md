# uploooadit

## Current Building Instructions

Build and deploy flask server hosted by gunicorn on gevent

```sh
docker build . -t uploooadit
docker run -it --name uploooadit --rm uploooadit
```

Build and deploy haproxy

```sh
docker build . -t haproxy -f Dockerfile-haproxy
docker run -p 8000:8000 --link uploooadit haproxy
```
