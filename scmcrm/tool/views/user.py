from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

# 用户管理界面
def tooluserindex(request):
    # 用户列表页
    return render(request,"user/index.html",{"data":"欢迎进入Tool，后台管理系统"})
def tooluseradd(request):
    # 用户新增界面加载
    return render(request,"user/add.html",{"data":"欢迎进入Tool，后台管理系统"})
def tooluserinsert(request):
    # 用户新增界面执行数据库操作
    return render(request,"user/add.html",{"data":"欢迎进入Tool，后台管理系统"})

# -------------
def tooluseredit(request):
    # 用户新增界面加载
    return render(request,"user/edit.html",{"data":"欢迎进入Tool，后台管理系统"})