import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookies_analyser.settings")

import django
django.setup()
from analyser.models import CookiesList, Cookie


def populate(list_owner):
    cookies_list = load_cookies_list(list_owner)
    for cookie in cookies_list:
        store(cookie)
    print('Done!')


def load_cookies_list(list_owner):
    cookies_list = CookiesList.objects.get(owner=list_owner).cookies
    return cookies_list


def store(cookie):
    cookie_obj = Cookie.objects.create()
    cookie_obj.expirationDate = cookie.setdefault('expirationDate', 'Unknown')
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
    cookie_obj.save()


if __name__ == '__main__':
    print('Populating...')
    populate()