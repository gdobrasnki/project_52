from django.shortcuts import render, redirect
from .models import cases
from .forms import casesForm, volunteersForm, UserRegisterForm
from django.contrib import messages
from django.db import connection, connections, transaction
from django.contrib.gis.geos import (Point, fromstr, fromfile,
                                     GEOSGeometry, MultiPoint, MultiPolygon, Polygon)
from django.contrib.gis.gdal import *
from django.contrib.auth.models import User
import geocoder
from django.db import connection, connections, transaction

# Create your views here.

# def base(request):
#     return render(request, 'app/base.html')


def main(request):
    if request.method == 'POST':
        form = casesForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            lati = profile.y
            longi = profile.x
            profile.geom = GEOSGeometry('POINT(%s %s)' % (
                longi, lati), srid=4326)
            profile.save()

            messages.success(request, "Location created successfully!")  # <-
        else:
            messages.error(request, "Please fill form completely!")
    else:
        form = casesForm()

    context = {
        'form': form
    }

    return render(request, 'app/index.html', context)


def volunteer(request):
    userForm = UserRegisterForm(request.POST or None)
    volunteringForm = volunteersForm(request.POST or None)
    if request.method == 'POST':
        if userForm.is_valid() and volunteringForm.is_valid():
            user = userForm.save()
            user.save()
            profile = volunteringForm.save(commit=False)
            profile.user = user
            lati = profile.y
            longi = profile.x
            profile.geom = GEOSGeometry(
                'POINT(%s %s)' % (longi, lati), srid=4326)
            profile.save()
            messages.success(request, "Customer created successfully!")  # <-
            userForm = UserRegisterForm()
            volunteringForm = volunteersForm()
        else:
            messages.error(request, "Error with form!")  # <-

    context = {
        "userForm": userForm,
        "volunteringForm": volunteringForm
    }
    return render(request, 'app/volunteer.html', context)
