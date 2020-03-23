#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from flask import Blueprint, render_template, url_for
from flask_googlemaps import Map

from .data import FOOD, HYGIENE
from .utils import get_items, get_names, make_person


www = Blueprint("site", __name__)


@www.route("/", methods=["GET", "POST"])
def mapview():
    food = get_items(FOOD)
    hygiene = get_items(HYGIENE)
    listoflist = [*food, *hygiene]

    mymap = Map(
        identifier="view-side",
        lat=53.5461,
        lng=-113.4938,
        markers=[(53.5461, -113.4938)]
    )

    markers2 = []
    for _ in range(1, 20):
        lat = random.randrange(5346000, 5363000)/100000
        lng = random.randrange(11342000, 11361000)/100000

        markers2.append(
            {
                "icon": "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
                "lat": lat,
                "lng": -lng,
                "infobox": make_person(),
            }
        )

    sndmap = Map(
        identifier="sndmap",
        lat=53.5461,
        lng=-113.4938,
        style="height:600px;width:100%;margin:0;",
        markers=markers2
    )

    return render_template("example.html",
                           mymap=mymap,
                           sndmap=sndmap,
                           listoflist=listoflist)


@www.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@www.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
