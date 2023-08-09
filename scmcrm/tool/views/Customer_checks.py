from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from datetime import date, timedelta
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

# 获取单个门店信息
def StoreDataUpdate(cs_id=0):
    try:
        # 获取数据库中客户的url和账号密码
        csdb = Customer.objects.get(id=cs_id)
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
        elif vo['renewaltime'] == None:
            rdb.store_ex_time = '2099-12-1'

        rdb.save()

    return HttpResponse(r)

# 获取门店信息接口
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
    hide_pw = md5.hexdigest()

    # 有一些固定密码
    if pwd == "acewill@321":
        hide_pw = 'fe9bd43565f5d435da0539793d93c0e9'
    if pwd == "gyljcgtdcpb@acewill.cn":
        hide_pw = "2142baf3b6e652c61ac34a9e29d19999"

    # 组装请求参数：用户名，密码，加密后的密码
    data = {
        'name': username,
        'pwd': pwd,
        'hide_pw': hide_pw
    }

    # 请求网址，并获取cookie 登录后的cookie
    response = requests.post(url_login, headers=headers, data=data)
    cookie = response.cookies
    print("这是登录后的cookie：", cookie.get)
    print("登录后的返回：：",response.text)

    # 继续请求，进入一个门店
    url_get_store = url + "logistics/?do=selectstore"
    data = {
        'lsid': "2",
    }
    response = requests.post(url_get_store, cookies=cookie, headers=headers, data=data)
    print("这是进入门店后的cookie：", response.cookies.get)
    print("进入门店后返回：", response.text)

    # 进入门店查询功能，老版本需要
    url_get_tablename = url + "chainsales/head/shop?tablename=sys_user_func"
    requests.get(url_get_tablename, cookies=cookie, headers=headers, data=data)
    print("这是进入门店后的cookie：", cookie.get)
    print("进入门店查询后的返回：", response.text)

    # 获取门店数据
    url_get_storelist = url + "chainsales/head/shop/listshop?limit=1000"
    response = requests.get(url_get_storelist, cookies=cookie, headers=headers, data=data)
    print("这是获取到的门店列表：", response.json())

    return response.json()


#  批量获取门店信息
