from django.contrib import admin
from analyser.models import CookiesList, Cookie


class CookieAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name', 'expirationDate', 'hostOnly', 'httpOnly', 'path', 'sameSite', 'secure', 'session', 'storeId', 'value')


admin.site.register(CookiesList)
admin.site.register(Cookie, CookieAdmin)