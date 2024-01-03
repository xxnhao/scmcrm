from django.shortcuts import render
from django.core.paginator import Paginator
from datetime import date, timedelta
from ..models import Customer, CustomerReport

def index(request, cs_id, pIndex=1):

    if request.method == 'GET':
        date = request.body.decode('utf-8')
        print(date)

    # 获取客户信息
    ob = Customer.objects.get(id= cs_id)

    # 单个客户门店数据
    cs_store_list = CustomerReport.objects.filter(cs_id= cs_id)

    # 分页处理
    pIndex = int(pIndex)
    page = Paginator(cs_store_list, 100)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    cs_store_list = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    # 发送页面数据
    context = {"customer_store_detail": cs_store_list, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'cs': ob, 'cs_id': cs_id,'url':'customer_store_detail'}
    print(context)
    return render(request,"Customer_checks/customer_store_detail.html", context)


def StoreDueThisMonth(request, cs_id, pIndex=1):
    # 获取客户名称
    ob = Customer.objects.get(id= cs_id)
    cs_name = ob.cs_name

    # 判断本月数据bydq_count
    current_year, current_month = date.today().year, date.today().month

    # 单个客户门店数据
    cs_store_list = CustomerReport.objects.filter(cs_id=cs_id, store_ex_time__year=current_year, store_ex_time__month=current_month)

    # 分页处理
    pIndex = int(pIndex)
    page = Paginator(cs_store_list, 100)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    cs_store_list = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

   # 发送页面数据
    context = {"customer_store_detail": cs_store_list, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'cs': ob, 'cs_id': cs_id,'url':'StoreDueThisMonth'}
    print(context)
    return render(request,"Customer_checks/customer_store_detail.html", context)

def StoreDueNextMonth(request, cs_id, pIndex=1):
    # 获取客户名称
    ob = Customer.objects.get(id= cs_id)
    cs_name = ob.cs_name

    # 判断下月数据
    next_month = date.today().replace(day=28) + timedelta(days=4)
    next_month = next_month.replace(day=1)
    next_year, next_month = next_month.year, next_month.month

    # 单个客户门店数据
    cs_store_list = CustomerReport.objects.filter(cs_id=cs_id, store_ex_time__year=next_year, store_ex_time__month=next_month)

    # 分页处理
    pIndex = int(pIndex)
    page = Paginator(cs_store_list, 100)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    cs_store_list = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息


    # 发送页面数据
    context = {"customer_store_detail": cs_store_list, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'cs': ob, 'cs_id': cs_id,'url':'StoreDueNextMonth'}
    print(context)
    return render(request,"Customer_checks/customer_store_detail.html", context)

