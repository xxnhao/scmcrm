# 程序后台子路由
from django.urls import path
from .views import index
from .views import user

urlpatterns = (
    path("", index.index, name='index'),
    path('user/', user.index, name='userindex'),
    path('user/add', user.add, name='useradd'),   # 加载添加用户页面
    path('user/insert', user.insert, name='userinsert'),  # 加载添加用户页面
    path('user/edit', user.edit, name='useredit'),

)
