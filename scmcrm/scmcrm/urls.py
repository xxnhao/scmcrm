# 程序总路由入口
from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import path,include

urlpatterns = [
    path('',include('tool.urls')),

    re_path('^static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),

]
