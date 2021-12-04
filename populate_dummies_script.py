import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookies_analyser.settings")

import django
django.setup()
from analyser.models import Cookie
import random

chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'

def populate():
    random_email(197)
    random_phone(162)
    random_name_and_password(109)
    print('Done!')


def random_email(count):
    for i in range(count):
        length = random.randint(6,14)
        domain_lenght = random.randint(3,8)
        name = ''.join(random.choice(chars) for m in range(length))
        domain = ''.join(random.choice(chars) for n in range(domain_lenght))
        email = name + '@' + domain + '.com'
        store(email)

def random_phone(count):
    prefix = ['phone=', 'tel=', 'TEL=']
    for i in range(count):
        length = random.randint(8,12)
        phone_prefix = ''.join(random.choice(prefix))
        phone_number = ''.join(random.choice(numbers) for m in range(length))
        phone = phone_prefix + phone_number
        store(phone)


def random_name_and_password(count):
    for i in range(count):
        name_length = random.randint(4,12)
        password_length = random.randint(8,18)
        name = ''.join(random.choice(letters) for m in range(name_length))
        password = ''.join(random.choice(chars) for n in range(password_length))
        value = 'name=' + name + '&passwd=' + password
        store(value)


def store(value):
    cookie_obj = Cookie.objects.create()
    cookie_obj.expirationDate = '12345678900'
    cookie_obj.domain = '.dummies.com'
    cookie_obj.hostOnly = False
    cookie_obj.httpOnly = False
    cookie_obj.name = 'dummy'
    cookie_obj.path = '/'
    cookie_obj.sameSite = 'unspecified'
    cookie_obj.secure = False
    cookie_obj.session = False
    cookie_obj.storeId = 0
    cookie_obj.value = value
    cookie_obj.isMalicious = 'True'
    cookie_obj.save()


if __name__ == '__main__':
    print('Populating Dummies...')
    populate()