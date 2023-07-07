from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from ..models import User
# Create your views here.

# 用户管理界面
def index(request):
    # 用户列表页
    return render(request,"user/index.html",{"data":"欢迎进入Tool，后台管理系统"})

def add(request):
    # 用户新增界面加载
    return render(request, "user/add.html" )

def insert(request):
    # 用户新增界面执行数据库操作
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        #将当前员工信息的密码做md5处理
        import hashlib,random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n) #从表单中获取密码并添加干扰值
        md5.update(s.encode('utf-8')) #将要产生md5的子串放进去
        ob.password_hash = md5.hexdigest() #获取md5值
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功！", "url": "userindex"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败！", "url": "userindex"}
    return render(request, "info.html", context)
def edit(request):
    # 用户新增界面加载
    return render(request, "user/edit.html", {"data":"欢迎进入Tool，后台管理系统"})