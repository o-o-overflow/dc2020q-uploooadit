accesslog = "-"
access_log_format = (
    '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
bind = "127.0.0.1:8000"
capture_output = True
chdir = "/app"
errorlog = "-"
group = "app"
keepalive = 60
user = "app"
worker_class = "gevent"
worker_tmp_dir = "/dev/shm"
workers = 1
