import multiprocessing

bind = '0.0.0.0:80'
workers = multiprocessing.cpu_count() * 2 + 1
chdirs = '/home/docker/code/app'
user = 'root'
max_requests = 5000
max_requests_jitter = 100
