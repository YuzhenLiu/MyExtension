import json

from django.http import HttpResponse
from django.shortcuts import render

import ml
from analyser.models import CookiesList


def index(request):
    context_dict = {}
    obj = CookiesList.objects.get(owner='jack')
    context_dict['cookies'] = obj.cookies

    return render(request, 'analyser/index.html', context=context_dict)


def upload(request):
    test_owner = 'test'
    obj = CookiesList.objects.create()
    obj.owner = test_owner
    obj.cookies = json.loads(request.body.decode("utf-8"))
    obj.save()

    ml.populate(test_owner)

    return HttpResponse("succeed!")


def get_cookies_json(request):
    if request.is_ajax():
        json = CookiesList.objects.get(owner='jack')
    else:
        json = 'error'

    return HttpResponse(json, 'application/json')
