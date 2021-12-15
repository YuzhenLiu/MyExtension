import json

from django.http import HttpResponse
from django.shortcuts import render

import classifier
import populate_script
from analyser.models import CookiesList, Temp
test_owner = 'tester'


def index(request):
    context_dict = {}
    obj = CookiesList.objects.get(owner=test_owner)
    context_dict['cookies'] = obj.cookies

    return render(request, 'analyser/index.html', context=context_dict)


def upload(request):
    CookiesList.objects.filter(owner=test_owner).delete()
    obj = CookiesList.objects.create()
    obj.owner = test_owner
    obj.cookies = json.loads(request.body.decode("utf-8"))
    obj.url = request.headers.get('Site-Url')
    obj.domain = request.headers.get('Site-Domain')
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

def report(request):
    context_dict = {}
    context_dict['url'] = CookiesList.objects.get(owner=test_owner).url
    context_dict['session_cookies'] = Temp.objects.filter(expirationDate='Session')
    context_dict['stored_cookies'] = Temp.objects.exclude(expirationDate='Session')
    context_dict['third_party_cookies'] = Temp.objects.filter(isThirdPartyCookie=1)
    context_dict['malicious_cookies'] = Temp.objects.filter(isMalicious=1)

    return render(request, 'analyser/report.html', context=context_dict)