import os

workers = 2
bind = '0.0.0.0:443'
proc_name = 'website'
pidfile = '%s/website.pid' % os.path.abspath(os.path.dirname(__file__))
accesslog = '%s/logs/gunicorn-access.log' % os.path.abspath(os.path.dirname(__file__))
errorlog = '%s/logs/gunicorn-error.log' % os.path.abspath(os.path.dirname(__file__))

ca_certs = '%s/instance/ca.crt' % os.path.abspath(os.path.dirname(__file__))
certfile = '%s/instance/server.crt' % os.path.abspath(os.path.dirname(__file__))
keyfile = '%s/instance/server.key' % os.path.abspath(os.path.dirname(__file__))
