from django.conf.urls import url
from django.urls import path
from . import views
from Flickermeter.dash_apps.woriking_apps import Main


urlpatterns = [
    path('main/', views.ex, name='Flickermeter-main' ),
    path('info/', views.inf, name='Flickermeter-info' ),
]