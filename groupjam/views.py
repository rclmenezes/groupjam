from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

def thread(request):
    c = RequestContext(request, {})
    return render_to_response('thread.html', c)

def home(request):
    c = RequestContext(request, {})
    return render_to_response('home.html', c)

def group(request):
    c = RequestContext(request, {})
    return render_to_response('group.html', c)