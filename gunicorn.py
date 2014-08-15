import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:8080'
proc_name = 'vpn_website'
pidfile = '%s/vpn_website.pid' % os.getcwd()
accesslog = '%s/logs/gunicorn-access.log' % os.getcwd()
errorlog = '%s/logs/gunicorn-error.log' % os.getcwd()
