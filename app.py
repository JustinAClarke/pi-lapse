#!/usr/bin/env python

from flask import Flask, render_template, request, url_for,redirect,request
from time import sleep
from picamera import PiCamera

from urlparse import urlparse
import random
import os

app = Flask(__name__)
camera = False

@app.route('/on/')
def cameraon():
    global camera
    camera = PiCamera()
    #return redirect(url_for('home'))
    return request.referrer


@app.route('/off/')
def cameraoff():
    global camera
    camera.close()
    camera = False
    #return redirect(url_for('home'))
    return request.referrer


@app.route('/')
def home():
    """Camera home page."""
    links = getRoutes(app)
    #links = [{'url': "/preview/", 'title': "Preview"}
     #        ]
    return render_template("home.html", title="Camera", links=links,cameraStatus=getCameraStatus())


@app.route('/preview')
def preview():
    links = getRoutes(app)
    cameraStatus=getCameraStatus()
    template='noPreview.html'
    if cameraStatus:
        global camera
        width = request.args.get('width', default=2592, type=int)
        height = request.args.get('height', default=1944, type=int)
        template='preview.html'
        """Preview the camera image"""
        #url = urlparse(request.url)
        camera.resolution = (int(width),int(height))
        #camera.resolution = (2592,1944)
    #    camera.start_preview()
        # Camera warm-up time
        sleep(2)
        camera.capture('/home/pi/pi-camera/static/preview.jpg')
    return render_template(template,
                           title="Preview",
                           links=links,
                           cameraStatus=cameraStatus)

def getCameraStatus():
    global camera
    if camera == False:
        return False
    else:
        return True
    
def getRoutes(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = getRoutes(app)
    return render_template("map.html",
                           title="SiteMap",
                           links=links)

@app.errorhandler(404)
def page_not_found(error):
    links = getRoutes(app)
    return render_template('page_not_found.html',links=links,title="404 Not Found"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
