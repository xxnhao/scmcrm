from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db.models.functions import ExtractYear, ExtractMonth
from ..models import Customer, CustomerReport
from django.http import HttpResponse
from django.db.models import Q


def index(request,pIndex=1):
    # 客户列表
    ob = Customer.objects
    oblist = ob.all()

    # 客户门店数据
    cs_store = CustomerReport.objects

    # 筛选条件
    where = []
    key = request.GET.get("keyword", None)
    if key:
        oblist = oblist.filter(Q(cs_name__contains=key)|Q(cs_am__contains=key))
        where.append('keyword=' + key)

    # 汇总数据

    cs_store_list = []

    # 判断本月数据bydq_count
    current_year, current_month = date.today().year, date.today().month

    # 判断下月数据
    next_month = date.today().replace(day=28) + timedelta(days=4)
    next_month = next_month.replace(day=1)
    next_year, next_month = next_month.year, next_month.month

    for i in oblist:
        cs_count = cs_store.filter(cs_id=i.id).count()
        ps_count = cs_store.filter(cs_id=i.id, store_type='3').count()
        zy_count = cs_store.filter(cs_id=i.id, store_type='4').count()
        jm_count = cs_store.filter(cs_id=i.id, store_type='5').count()
        wx_count = cs_store.filter(cs_id=i.id, store_type='6').count()
        bydq_count = cs_store.filter(cs_id=i.id, store_ex_time__year=current_year, store_ex_time__month=current_month).count()
        xydq_count = cs_store.filter(cs_id=i.id, store_ex_time__year=next_year, store_ex_time__month=next_month).count()

        data = {
            'id': i.id,
            'cs_name': i.cs_name,
            'cs_am': i.cs_am,
            'cs_count': cs_count,
            'ps_count': ps_count,
            'zy_count': zy_count,
            'jm_count': jm_count,
            'wx_count': wx_count,
            'bydq_count': bydq_count,
            'xydq_count': xydq_count
        }

        cs_store_list.append(data)

        print(cs_store_list)

    pIndex = int(pIndex)
    page = Paginator(cs_store_list, 10)
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    cs_store_list = page.page(pIndex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {"CustomerReport_list": cs_store_list, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages,}
    return render(request,"Customer_checks/index.html",context)


def StoreDataUpdate(request, cs_id=0):

    print(cs_id)

    try:
        csdb = Customer.objects.get(id=cs_id)

        # 获取数据库中客户的url和账号密码
        url = csdb.cs_url
        username = csdb.cs_username
        pwd = csdb.cs_password
        cs_am = csdb.cs_am

    except Exception as err:

        print(err)

    # 更新先清空门店客户信息
    rdb = CustomerReport.objects.filter(cs_id=cs_id)
    rdb.delete()

    # 获取门店数据
    r = GetStoreData(url, username, pwd)

    print(r['total'])

    for vo in r['data']:
        rdb = CustomerReport()
        rdb.cs_id = cs_id
        rdb.cs_am = cs_am
        rdb.store_id = vo['sid']
        rdb.store_name = vo['shopname']
        rdb.store_type = vo['stype']  # 3=配送中心，4=直营店，5=加盟店，6=外销客户
        rdb.store_ex_time = vo['renewaltime']  # 到期时间
        if vo['renewaltime'] == '0000-00-00':
            rdb.store_ex_time = '2099-12-1'
        rdb.save()

    return HttpResponse(r)


def GetStoreData(url, username, pwd):

    import requests
    import hashlib
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # 登录网页
    url_login = url + "?do=check"

    print(url_login)

    # 密码需要MD5加密
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf-8'))
    pwd = md5.hexdigest()

    # 有一些固定密码
    if pwd == "acewill@321":
        pwd = 'fe9bd43565f5d435da0539793d93c0e9'
    if pwd == "gyljcgtdcpb@acewill.cn":
        pwd = "2142baf3b6e652c61ac34a9e29d19999"

    # 组装请求参数
    data = {
        'name': username,
        'pwd': '',
        'hide_pw': pwd
    }

    # 请求网址，并获取cookie 登录后的cookie
    response = requests.post(url_login, headers=headers, data=data)
    cookie = response.cookies.get('PHPSESSID')
    print("这是登录后的cookie：", cookie)

    # 继续请求，登录一个门店
    url_get_store = url + "logistics/?do=selectstore"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'PHPSESSID': cookie
    }

    data = {
        'lsid': "2",
    }
    response = requests.get(url_get_store, headers=headers, data=data)
    cookie = response.cookies.get('PHPSESSID')

    print("这是进入门店后的cookie：",cookie)

    url_get_storelist = url + "chainsales/head/shop/listshop?limit=1000"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'PHPSESSID': cookie
    }

    response = requests.get(url_get_storelist,headers=headers, data=data)

    print("这是获取到的门店列表：", response.json())

    return response.json()