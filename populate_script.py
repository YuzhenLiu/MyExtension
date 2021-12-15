import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookies_analyser.settings")

import django
django.setup()
from analyser.models import CookiesList, Temp
destination = Temp


def populate(list_owner):
    destination.objects.all().delete()
    cookies_data = load_cookies_data(list_owner)
    cookies = cookies_data[0]
    domain = cookies_data[1]

    for cookie in cookies:
        if domain in cookie['domain']:
            store(cookie, 0)
        else:
            store(cookie, 1)
    destination.objects.order_by('domain')
    print('Done!')


def load_cookies_data(list_owner):
    cookies_list = CookiesList.objects.get(owner=list_owner).cookies
    domain = CookiesList.objects.get(owner=list_owner).domain
    return cookies_list, domain


def store(cookie, type):
    cookie_obj = destination.objects.create()
    cookie_obj.expirationDate = cookie.setdefault('expirationDate', 'Session')
    cookie_obj.domain = cookie['domain']
    cookie_obj.hostOnly = cookie['hostOnly']
    cookie_obj.httpOnly = cookie['httpOnly']
    cookie_obj.name = cookie['name']
    cookie_obj.path = cookie['path']
    cookie_obj.sameSite = cookie['sameSite']
    cookie_obj.secure = cookie['secure']
    cookie_obj.session = cookie['session']
    cookie_obj.storeId = cookie['storeId']
    cookie_obj.value = cookie['value']
    cookie_obj.isMalicious = -1
    cookie_obj.isThirdPartyCookie = type
    cookie_obj.save()


if __name__ == '__main__':
    print('Populating...')
    populate()