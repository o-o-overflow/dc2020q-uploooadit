FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip python3-wheel \
    && pip3 install -U pip setuptools \
    && pip install flask gunicorn[gevent]

RUN mkdir -p /var/uploads

COPY app.py .

CMD ["gunicorn", "--access-logfile=-", "--bind=0.0.0.0:8080", "--keep-alive=60", "--strip-header-spaces", "--worker-class=gevent", "--workers=1", "app:app"]
