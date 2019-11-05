from django.urls import path
from . import views

urlpatterns = [
    path('', views.log, name='usercreate-login' ),
    path('register/', views.reg, name='usercreate-register' ),
    path('logout/', views.logo, name='usercreate-logout' ),
]