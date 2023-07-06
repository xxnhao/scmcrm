from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def webindex(request):
    return HttpResponse("欢迎进入web前台管理系统")