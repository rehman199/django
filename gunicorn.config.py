loglevel = 'debug'

capture_output = True

accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

workers = 4

worker_class = 'uvicorn_worker.UvicornWorker'

wsgi_app = 'backend.wsgi:application'
