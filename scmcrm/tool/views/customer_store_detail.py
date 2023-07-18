from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db.models.functions import ExtractYear, ExtractMonth
from ..models import Customer, CustomerReport
from django.http import HttpResponse
from django.db.models import Q


def index(request, cs_id, pIndex=1):
    # 获取客户名称
    ob = Customer.objects.get(id= cs_id)
    cs_name = ob.cs_name

    # 单个客户门店数据
    cs_store_list = CustomerReport.objects.filter(cs_id= cs_id)

    # 分页处理
    pIndex = int(pIndex)
    page = Paginator(cs_store_list, 10)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    cs_store_list = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息


    # 发送页面数据
    context = {"customer_store_detail": cs_store_list, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'cs_name': cs_name, 'cs_id': cs_id}
    return render(request,"Customer_checks/customer_store_detail.html", context)
