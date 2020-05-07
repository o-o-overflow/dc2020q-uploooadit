#!/bin/bash

gunicorn \
  --access-logfile=access.log \
  --bind=127.0.0.1:8000 \
  --capture-output \
  --daemon \
  --error-logfile=error.log \
  --keep-alive=60 \
  --strip-header-spaces \
  --worker-class=gevent \
  --worker-tmp-dir=/dev/shm \
  --workers=1 \
  app:app
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start gunicorn: $status"
  exit $status
fi

haproxy -f /etc/haproxy -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start haproxy: $status"
  exit $status
fi

echo "Started!"

while sleep 60; do
  ps aux |grep gunicorn |grep -q -v grep
  GUNICORN_STATUS=$?
  ps aux |grep haproxy |grep -q -v grep
  HAPROXY_STATUS=$?
  if [ $GUNICORN_STATUS -ne 0 -o $HAPROXY_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done
