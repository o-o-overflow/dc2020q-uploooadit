FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl python3-pip python3-wheel supervisor \
    && pip3 install -U pip setuptools \
    && pip install boto3 flask gunicorn[gevent]==20.0.0 requests

COPY app.py store.py /app/
COPY config/gunicorn.conf.py /etc/
COPY config/supervisord.conf /etc/supervisor/conf.d/

RUN chmod 444 /app/app.py /app/store.py \
    && chmod 400 /etc/gunicorn.conf.py \
    && chmod 400 /etc/supervisor/conf.d/supervisord.conf \
    && mkdir --mode=111 --parents /home/haproxy \
    && mkdir --mode=111 --parents /home/invoker \
    && useradd -UM app \
    && useradd -UMr haproxy \
    && useradd -UM invoker

COPY --chown=haproxy:haproxy bin/haproxy config/haproxy.cfg errorfiles/* /home/haproxy/
COPY --chown=invoker:invoker scripts/invoker.py /home/invoker/

RUN chmod 500 /home/haproxy/haproxy /home/invoker/invoker.py \
    && chmod 400 /home/haproxy/*.http \
    && chmod 400 /home/haproxy/haproxy.cfg

WORKDIR app
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
