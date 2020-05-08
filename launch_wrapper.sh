#!/bin/bash

gunicorn --config=/etc/gunicorn.conf.py app:app
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start gunicorn: $status"
  exit $status
fi

su haproxy -c '/home/haproxy/haproxy -f /home/haproxy/haproxy.cfg -D'
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start haproxy: $status"
  exit $status
fi

su invoker -c '/home/invoker/invoker.py --daemon' &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start invoker: $status"
  exit $status
fi

echo "Started!"

while sleep 60; do
  ps aux |grep gunicorn |grep -q -v grep
  GUNICORN_STATUS=$?
  ps aux |grep haproxy |grep -q -v grep
  HAPROXY_STATUS=$?
  ps aux |grep invoker |grep -q -v grep
  INVOKER_STATUS=$?
  if [ $GUNICORN_STATUS -ne 0 -o $HAPROXY_STATUS -ne 0 -o $INVOKER_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done
