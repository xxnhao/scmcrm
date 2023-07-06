from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

def toolindex(request):
    return render(request,"index/index.html",{"data":"欢迎进入Tool，后台管理系统"})


def tooluserindex(request):
    return render(request,"user/index.html",{"data":"欢迎进入Tool，后台管理系统"})