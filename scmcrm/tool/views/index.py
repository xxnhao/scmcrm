from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.


def index(request):
    # 首页
    return render(request,"index/index.html",{"data":"欢迎进入Tool，后台管理系统"})