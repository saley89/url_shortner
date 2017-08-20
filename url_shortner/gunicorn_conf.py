import multiprocessing

bind = '0.0.0.0:8000'
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
graceful_timeout = 10