from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
from ..models import User
# Create your views here.

# 用户管理界面
def index(request, pIndex=1):
    # 用户列表页
    ob = User.objects
    oblist = ob.all()
    pIndex = int (pIndex)
    page = Paginator(oblist,10)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"userlist": list2,'plist': plist,'pIndex': pIndex,'maxpages': maxpages,}

    return render(request,"user/index.html",context)
def add(request):
    # 用户新增界面加载
    return render(request, "user/add.html" )

def insert(request):
    # 用户新增界面执行数据库操作
    try:

        # 创建用户前先判断用户是否存在
        f = User.objects
        if f.filter(username=request.POST['username']).count() >= 1:
            context = {"messages": True,"success": "失败","data": "用户名已存在"}
            return render(request,"user/add.html",context)

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
        context = {"messages": True, "success": "成功", "data": "用户：" + request.POST['username'] + "创建成功！"}
    except Exception as err:
        print(err)
        context = {"messages": True, "success": "失败", "data": err}
    return render(request, "user/add.html", context)
def edit(request):
    # 用户新增界面加载
    return render(request, "user/edit.html", {"data":"欢迎进入Tool，后台管理系统"})