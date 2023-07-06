# 程序后台子路由
from django.urls import path
from .views import index
from .views import user

urlpatterns = (
    path("",index.toolindex,name='toolindex'),
    path('user/',user.tooluserindex,name='Userindex'),
    path('user/add',user.tooluseradd,name='tooluseradd'),#加载添加用户页面
    path('user/insert',user.tooluserinsert,name='tooluserinsert'),#加载添加用户页面
    path('user/edit',user.tooluseredit,name='tooluseredit'),

)
