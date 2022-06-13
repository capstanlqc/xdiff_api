from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/souto/Dev/xdiff_service/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/souto/Dev/xdiff_service/access_log'
errorlog =  '/home/souto/Dev/xdiff_service/error_log'
