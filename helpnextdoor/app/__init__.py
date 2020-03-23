#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps


app = Flask(__name__)
app.config.from_object("config")
Bootstrap(app)
GoogleMaps(app, key="")


from .site.views import www

app.register_blueprint(www)
