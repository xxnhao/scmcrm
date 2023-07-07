# 程序后台子路由
from django.urls import path
from .views import index
from .views import user

urlpatterns = (
    path("", index.index, name='index'),

    # 用户管理路由
    path('user/<int:pIndex>', user.index, name='userindex'),
    path('user/add', user.add, name='useradd'),   # 加载添加用户页面
    path('user/insert', user.insert, name='userinsert'),  # 加载添加用户页面
    path('user/edit', user.edit, name='useredit'),

)
