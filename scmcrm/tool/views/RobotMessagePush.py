from django.http import HttpResponse
import json
import requests
from ..models import CustomerReport,User,Customer

def RobotMessagePush(request):

    #  获取用户列表
    us = User.objects.all()

    #   拼接markdown消息内容
    for i in us:
        print(i.nickname)
        text = "<font color=\"warning\">"+i.nickname+"</font>，您好,以下客户本月有门店即将到期，请及时处理！。\n"
        text2=""
        for key in json.loads(CollateData()):
            print(key['cs_am'], i.nickname)
            if (key['cs_am'] == i.nickname and int(key['bydq_count']) != 0):
                text2 = text2 + "> "+key['cs_name']+":<font color=\"comment\">本月到期数："+str(key['bydq_count'])+"-[点击查看详情](http://114.115.151.79:8080/StoreDueThisMonth/"+str(key['id'])+"/1)"+"</font>\n"

        if (text2 != ""):
            url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d03e20bb-c218-4652-b7f7-ca86e348620c'
            headers = {'Content-Type': 'application/json'}
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": text+text2
                }
            }
            print(data)
            response = requests.post(url,headers=headers,data=json.dumps(data))
    return HttpResponse(response)

def CollateData():

    from datetime import date, timedelta
    # 客户列表
    ob = Customer.objects
    oblist = ob.all()

    # 客户门店数据
    cs_store = CustomerReport.objects

    # 判断本月数据
    current_year, current_month = date.today().year, date.today().month

    # 判断下月数据
    next_month = date.today().replace(day=28) + timedelta(days=4)
    next_month = next_month.replace(day=1)
    next_year, next_month = next_month.year, next_month.month

    #
    cs_store_list = []
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




    return json.dumps(cs_store_list, ensure_ascii=False)