from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

def home(request):
    c = RequestContext(request, {})
    return render_to_response('index.html', c)