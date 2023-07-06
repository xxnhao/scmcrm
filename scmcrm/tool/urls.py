# 程序后台子路由
from django.urls import path
from . import views

urlpatterns = (
    path("",views.toolindex,name='toolindex'),

    path('user/',views.tooluserindex,name='Userindex'),
)
