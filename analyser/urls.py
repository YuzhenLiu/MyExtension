from django.urls import path
from analyser import views

app_name = 'analyser'
urlpatterns = [
    path('', views.index, name='index'),
]