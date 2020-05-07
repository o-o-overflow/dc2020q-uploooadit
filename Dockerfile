FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip python3-wheel \
    && pip3 install -U pip setuptools \
    && pip install flask gunicorn[gevent]

COPY app.py /app/
COPY launch_wrapper.sh /sbin/
COPY config/gunicorn.conf.py /etc/

RUN chmod 444 /app/app.py \
    && chmod 500 /sbin/launch_wrapper.sh \
    && chmod 600 /etc/gunicorn.conf.py \
    && mkdir --mode=111 --parents /home/haproxy \
    && mkdir --mode=733 --parents /var/log/gunicorn /var/uploads \
    && useradd -UM app \
    && useradd -UMr haproxy

COPY --chown=haproxy:haproxy bin/haproxy config/haproxy.cfg /home/haproxy/

RUN chmod 500 /home/haproxy/haproxy \
    && chmod 400 /home/haproxy/haproxy.cfg

WORKDIR app
CMD ["launch_wrapper.sh"]
