import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:8080'
proc_name = 'website'
pidfile = '%s/website.pid' % os.path.abspath(os.path.dirname(__file__))
accesslog = '%s/logs/gunicorn-access.log' % os.path.abspath(os.path.dirname(__file__))
errorlog = '%s/logs/gunicorn-error.log' % os.path.abspath(os.path.dirname(__file__))
