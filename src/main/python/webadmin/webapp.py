import os
import time
import socket
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, Response, render_template

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


def get_event_stream(string):
    lines = string.split('\n')
    for line in lines[:-1]:
        if line:
            yield 'data: {0}<br>\n'.format(line)
    yield 'data: {0}\n\n'.format(lines[-1])


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


@app.route('/network-counters-stream', methods=['GET'])
def network_counters_stream():
    return Response(get_event_stream("Hallo Welt {0}".format(time.strftime("%H:%M:%S"))), mimetype="text/event-stream")


if __name__ == '__main__':
    run(bind='127.0.0.1', port=8080, debug=True)