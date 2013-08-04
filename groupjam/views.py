from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

def feed(request):
    c = RequestContext(request, {'selected': 'feed'})
    return render_to_response('feed.html', c)

def calendar(request):
    c = RequestContext(request, {'selected': 'calendar'})
    return render_to_response('calendar.html', c)

def box(request):
    c = RequestContext(request, {'selected': 'box'})
    return render_to_response('box.html', c)

def pictures(request):
    c = RequestContext(request, {'selected': 'pictures'})
    return render_to_response('pictures.html', c)

def settings(request):
    c = RequestContext(request, {'selected': 'settings'})
    return render_to_response('settings.html', c)

def splash(request):
    c = RequestContext(request, {})
    return render_to_response('splash.html', c)

def old(request):
    c = RequestContext(request, {})
    return render_to_response('home-old.html', c)