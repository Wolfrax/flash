#!/usr/bin/python
#-*- coding: utf-8 -*-

__author__ = 'mm'


from flask import Flask, abort, render_template, send_from_directory
import os


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
    return send_from_directory(directory=os.path.join(app.root_path, 'static'), path=filename)
