from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, \
                        HttpResponseForbidden
from django.template import loader
import api.models as db


# Create your views here.
def test_url(request):
    template = loader.get_template("test_template.html")
    context = {"context": "Loes ipus marious fo irignus"}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def test_url2(request):
    template = loader.get_template("test_template.html")
    context = {"context": "Loes ipus marious fo irignus",
               "context2": "CONTEXT2 SI BETTER CONTEXT"}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def test(request, name=""):
    text = "Hello! " + name
    if request.GET.get("second_name"):
        text = "Hello! " + name + " " + request.GET.get("second_name")
    return HttpResponse(text)


def any(request):
    value_of_cookie = "value_of_cookie"
    max_age_in_sec = 120
    key_or_name = "cookie"
    text = "No cookie?"
    response = HttpResponseForbidden(text)
    response.set_cookie(key_or_name, value_of_cookie, max_age=max_age_in_sec,
                            expires=None, domain=None, secure=None, httponly=True,
                            samesite=None)
    if request.COOKIES.get(key_or_name):
        response = HttpResponseForbidden(request.COOKIES[key_or_name])
    return response


def index(request):
    return "Index page"