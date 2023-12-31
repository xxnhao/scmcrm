from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from datetime import datetime
from ..models import Customer, User
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

# 用户管理界面
def index(request, pIndex=1):
    # 用户列表页
    ob = Customer.objects
    oblist = ob.all()
    where = []

    key = request.GET.get("keyword",None)
    if key:
        oblist = oblist.filter(Q(cs_name__contains=key)|Q(cs_am__contains=key))
        where.append('keyword=' + key)

    pIndex = int(pIndex)
    page = Paginator(oblist,100)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    title = ['客户id','客户名称','客户登录地址','客户状态','登录账号','登录密码','客户负责人','更新时间','操作']
    context = {"title":title, "Customerlist": list2, 'plist': plist,'pIndex': pIndex,'maxpages': maxpages, }
    return render(request,"Customer/index.html",context)
def add(request):
    # 用户新增界面加载

    # 取用户表数据
    uob = User.objects
    uoblist = uob.all()
    context = {"uoblist": uoblist}
    return render(request, "Customer/add.html", context)

def insert(request):
    # 用户新增界面执行数据库操作
    try:
        ob = Customer()
        ob.cs_name = request.POST['cs_name']
        ob.cs_url = request.POST['cs_url']
        ob.cs_username = request.POST['cs_username']
        ob.cs_password = request.POST['cs_password']
        ob.cs_am = request.POST['cs_am']
        ob.cs_status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        return HttpResponse("客户：" + str(ob.cs_username) + " 添加成功！")

    except Exception as err:

        return HttpResponse("失败：" + str(err))

def delete(request,uid=0):
    """执行信息删除"""
    try:
        ob = Customer.objects.get(id=uid)
        ob.delete()
        #   ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #   ob.save()
        context = {"show_popup": True,"success": "成功","popup_data": "用户：" + str(ob) + "删除成功！"}
    except Exception as err:
        print(err)
        context = {'show_popup': True,"success": "失败","popup_data": err}
    #    return render(request,"user/index.html",context)
    return redirect(request.META.get('HTTP_REFERER'),context)
def edit(request,uid=0):
    '''加载信息编辑表单'''
    try:
        # 取用户表数据
        uob = User.objects
        uoblist = uob.all()

        # 获取客户表数据
        ob = Customer.objects.get(id=uid)
        context = {'Customer': ob, "uoblist": uoblist}
        return render(request,"Customer/edit.html",context)
    except Exception as err:
        print(err)
        context = {'show_popup': True,"success": "失败","popup_data": err}

    return render(request,"Customer/index.html",context)
def update(request,uid):
    '''执行信息编辑'''
    try:
        ob = Customer.objects.get(id=uid)
        ob.cs_name = request.POST['cs_name']
        ob.cs_url = request.POST['cs_url']
        ob.cs_username = request.POST['cs_username']
        ob.cs_password = request.POST['cs_password']
        ob.cs_am = request.POST['cs_am']
        ob.cs_AddrName = request.POST['cs_AddrName']
        ob.cs_Address = request.POST['cs_Address']
        ob.cs_AddrPhone = request.POST['cs_AddrPhone']
        ob.cs_status = request.POST['status']  # 1：正常  2：流失
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        return HttpResponse("客户：" + str(ob.cs_name) + " 更新成功" )

    except Exception as err:

        return HttpResponse("失败：" + str(err))