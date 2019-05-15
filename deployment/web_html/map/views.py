"""
====== COMP90024 TEAM 16 ======

889545   Yu Liu          yul22       yul22@student.unimelb.edu.au
875095   Jize Dong       jized       jized@student.unimelb.edu.au
911764   Minsheng Wang   minshengw   minshengw@student.unimelb.edu.au
890742   Minglun Zhang   minglunz    minglunz@student.unimelb.edu.au
905084   Xingping Ding   xingpingd   xingpingd@student.unimelb.edu.au

"""

import os
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
import couchdb
import json
from django.http import HttpResponse


# from couchdb import Server
# from couchdb.client import ResourceNotFound

# server = couchdb.Server('http://root:Couchdbmima@127.0.0.1:5984')
# restResource = server['map']


def index(request):
    return render(request, 'map/index.html')


def wrath(request):
    return render(request, 'map/wrath.html')


# RESTful api
def sentiment_by_suburbs(request):
    with open('map/static/map/res/melbourne_suburbs.geojson') as f:
        data = json.load(f)
        return HttpResponse(json.dumps(data), content_type='application/json')


# RESTful api
def sentiment_by_hours(request):
    with open('map/static/map/res/pride_pro.json') as f:
        data = json.load(f)
        return HttpResponse(json.dumps(data), content_type='application/json')


# RESTful api
def sentiment_by_weekdays(request):
    with open('map/static/map/res/wrath_pro.json') as f:
        data = json.load(f)
        return HttpResponse(json.dumps(data), content_type='application/json')


def word_cloud(request):
    with open('map/static/map/res/hot_topics_50.json') as f:
        data = json.load(f)
        return HttpResponse(json.dumps(data), content_type='application/json')


def hashtags(request):
    return render(request, 'map/hashtags.html')


def pride(request):
    return render(request, 'map/pride.html')


def aurin(request):
    return render(request, 'map/aurin.html')


def aboutUs(request):
    return render(request, 'map/aboutUs.html')


def report(request):
    return render(request, 'map/report.html')
