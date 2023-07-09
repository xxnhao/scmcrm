from django.shortcuts import render,redirect
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from ..models import User


# Create your views here.

# 用户管理界面
def index(request, pIndex=1):
    # 用户列表页
    ob = User.objects
    oblist = ob.all()
    where = []

    key = request.GET.get("keyword",None)
    print(key)
    if key:
        oblist = oblist.filter(Q(nickname__contains=key))
        where.append('keyword=' + key)
        print(where)

    # 分页处理
    pIndex = int(pIndex)
    page = Paginator(oblist,10)  # 最大10条数据分页
    max_pages = page.num_pages
    if pIndex > max_pages:
        pIndex = max_pages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"userlist": list2,'plist': plist,'pIndex': pIndex,'max_pages': max_pages,'key': where}

    return render(request,"user/index.html",context)


def add(request):
    # 用户新增界面加载
    return render(request,"user/add.html")

def insert(request):
    # 用户新增界面执行数据库操作
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        # 将当前员工信息的密码做md5处理
        import hashlib,random
        md5 = hashlib.md5()
        n = random.randint(100000,999999)
        s = request.POST['password'] + str(n)  # 从表单中获取密码并添加干扰值
        md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
        ob.password_hash = md5.hexdigest()  # 获取md5值
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        return HttpResponse("用户：" + str(ob.nickname) + " 创建成功")

    except Exception as err:

        return HttpResponse("失败：" + str(err))


def delete(request,uid=0):
    """执行信息删除"""
    try:
        ob = User.objects.get(id=uid)
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
        ob = User.objects.get(id=uid)
        context = {'user': ob}
        return render(request,"user/edit.html",context)
    except Exception as err:
        print(err)
        context = {'show_popup': True,"success": "失败","popup_data": err}

    return render(request,"user/index.html",context)


def update(request,uid):
    '''执行信息编辑'''
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        # 修改的密码也要做加密处理
        import hashlib,random
        md5 = hashlib.md5()
        n = random.randint(100000,999999)
        s = request.POST['password'] + str(n)  # 从表单中获取密码并添加干扰值
        md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
        ob.password_hash = md5.hexdigest()  # 获取md5值
        ob.password_salt = n
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        return HttpResponse("用户：" + str(ob.nickname) + " 更新成功" )

    except Exception as err:

        return HttpResponse("失败：" + str(err))



