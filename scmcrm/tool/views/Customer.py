from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import datetime
from ..models import Customer
# Create your views here.

# 用户管理界面
def index(request, pIndex=1):
    # 用户列表页
    ob = Customer.objects
    oblist = ob.all()
    pIndex = int(pIndex)
    page = Paginator(oblist,10)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"Customerlist": list2, 'plist': plist,'pIndex': pIndex,'maxpages': maxpages,}
    return render(request,"Customer/index.html",context)
def add(request):
    # 用户新增界面加载
    return render(request, "Customer/add.html" )

def insert(request):
    # 用户新增界面执行数据库操作
    try:
        ob = Customer()
        ob.cs_name = request.POST['cs_name']
        ob.cs_url = request.POST['cs_url']
        ob.cs_username = request.POST['cs_username']
        ob.cs_password = request.POST['cs_password']
        ob.cs_status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"show_popup": True, "success": "成功", "popup_data": "用户：" + request.POST['cs_username'] + "创建成功！"}
    except Exception as err:
        print(err)
        context = {"show_popup": True, "success": "失败", "popup_data": err}

    return render(request, "Customer/add.html", context)

def edit(request):
    # 用户新增界面加载
    return render(request, "Customer/edit.html", {"data":"欢迎进入Tool，后台管理系统"})