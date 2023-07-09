from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from datetime import datetime
from ..models import Customer, User
from django.http import HttpResponse
from django.db.models import Q

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
    page = Paginator(oblist,10)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"Customerlist": list2, 'plist': plist,'pIndex': pIndex,'maxpages': maxpages, }
    return render(request,"Customer_checks/index.html",context)