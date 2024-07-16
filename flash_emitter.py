#!/usr/bin/python
#-*- coding: utf-8 -*-

__author__ = 'mm'


from flask import Flask, abort, render_template, send_from_directory, json, make_response, request
import glob, os
import gzip


class ReverseProxied(object):
    def __init__(self, app, script_name):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.script_name
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/flash')


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/flash/<filename>', methods=['GET'])  #Note, used when running flask locally, not on RPi
@app.route('/flash/static/<filename>', methods=['GET'])  #Note, used when running flask locally, not on RPi
@app.route('/<filename>', methods=['GET'])
def download(filename):
    with open(os.path.join(app.root_path, 'static', filename)) as fp:
        flash_content = json.load(fp)
        content = gzip.compress(json.dumps(flash_content).encode('utf8'), 5)
        response = make_response(content)
        response.headers['Content-length'] = len(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response

@app.route("/heatmap", methods=['GET'])
def heat():
    year = request.args.get('year')
    db_file = glob.glob(os.path.join(app.root_path, 'static', year + '_flash_db.json'))
    if db_file:
        return render_template('heatmap.html', year=year)
    else:
        abort(404)
