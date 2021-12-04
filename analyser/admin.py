from django.contrib import admin
from analyser.models import CookiesList, Cookie, Temp


class CookieAdmin(admin.ModelAdmin):
    list_display = ('isMalicious', 'domain', 'name', 'isMalicious', 'expirationDate', 'hostOnly', 'httpOnly', 'path', 'sameSite', 'secure', 'session', 'storeId', 'value')


admin.site.register(CookiesList)
admin.site.register(Cookie)
admin.site.register(Temp, CookieAdmin)