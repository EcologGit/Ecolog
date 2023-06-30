import multiprocessing
from Ecolog_django.settings import DEBUG

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
reload = DEBUG
timeout = 120
max_requests = 1000
worker_class = 'gevent'