# 程序总路由入口

from django.urls import path,include

urlpatterns = [
    path('',include('tool.urls')),
]
