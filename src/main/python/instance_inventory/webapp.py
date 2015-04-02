import os
import socket
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, g
from instance_inventory.resource.instances import Instance, Instances

app = Flask(__name__)


# set app secret to something considered random from os
app.secret_key = os.urandom(24)


def render_application_template(template_name, **template_parameters):
    return render_template(template_name, **template_parameters)


def init_access_log(access_log_file):
    logger = logging.getLogger('werkzeug')
    handler = RotatingFileHandler(access_log_file, maxBytes=10000, backupCount=5)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def run(bind, port, debug=False, access_log_file=False):
    if access_log_file:
        init_access_log(access_log_file)

    app.run(bind, port, threaded=True, debug=debug)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    version = '1.0.0'
    hostname = socket.gethostname()
    events = [{'source': 'system', 'start': '', 'end': '', 'state': 'success', 'message': 'This was a good one!'},
              {'source': 'system', 'start': '', 'end': '', 'state': 'failure', 'message': 'This was a bad one!'}
              ]
    pie_chart_stats = {'success': 30, 'error': 10}

    return render_application_template('index.html', **locals())


if __name__ == '__main__':
    run(bind='127.0.0.1', port=8080, debug=True)