import json

from django.http import HttpResponse
from django.shortcuts import render

import classifier
import populate_script
from analyser.models import CookiesList, Temp


def index(request):
    context_dict = {}
    obj = CookiesList.objects.get(owner='jack')
    context_dict['cookies'] = obj.cookies

    return render(request, 'analyser/index.html', context=context_dict)


def upload(request):
    test_owner = 'tom'
    CookiesList.objects.filter(owner=test_owner).delete()
    obj = CookiesList.objects.create()
    obj.owner = test_owner
    obj.cookies = json.loads(request.body.decode("utf-8"))
    obj.save()

    populate_script.populate(test_owner)
    classifier.classify()

    malicious_cookies = Temp.objects.filter(isMalicious=1).count()

    return HttpResponse(malicious_cookies)


def get_cookies_json(request):
    if request.is_ajax():
        json = CookiesList.objects.get(owner='jack')
    else:
        json = 'error'

    return HttpResponse(json, 'application/json')
