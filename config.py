import os

host = '0.0.0.0'
port = os.getenv('PORT', 5000)

bind = str(host) + ':' + str(port)

# Debugging
reload = True

# Logging
accesslog = '-'
loglevel = 'info'

# Proc Name
proc_name = 'zutool-linebot'

# Worker Processes
workers = 1
worker_class = 'sync'