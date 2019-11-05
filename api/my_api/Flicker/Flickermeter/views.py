from django.shortcuts import render
from django.http import HttpResponse
from .models import LightI
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response


def ex(request):
    context = {
        'title':'Analyser'
        }
    return render(request, 'Flickermeter/main.html',context)

def inf(request):
    context = {
        'title':'Info'
        }
    return render(request, 'Flickermeter/info.html',context)