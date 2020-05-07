FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip python3-wheel \
    && pip3 install -U pip setuptools \
    && pip install flask gunicorn[gevent]

RUN mkdir -p /var/uploads

WORKDIR /app

COPY app.py launch_wrapper.sh ./
COPY bin/haproxy /usr/local/sbin/
COPY haproxy.cfg /etc/haproxy/

CMD ["./launch_wrapper.sh"]
