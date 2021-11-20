from django.urls import path
from analyser import views

app_name = 'analyser'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('get_cookies_json/', views.get_cookies_json, name='get_cookies_json')
]