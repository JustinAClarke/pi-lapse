#!/usr/bin/env python

from flask import Flask, render_template, request, url_for
from time import sleep
from picamera import PiCamera

from urlparse import urlparse
import random
import os

app = Flask(__name__)
camera = PiCamera()


@app.route('/')
def home():
    """Camera home page."""
    links = [{'url': "/preview/", 'title': "Preview"}
             ]
    return render_template("home.html", title="Camera", links=links)


@app.route('/preview/')
def preview():
    global camera
    """Preview the camera image"""
    url = urlparse(request.url)
    camera.resolution = (1024, 768)
#    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('/home/pi/pi-camera/static/preview.jpg')
    return render_template("preview.html",
                           title="Preview",
                           my_hostname=url.hostname,
                           my_http_port=url.port)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
