
# 前台页面子路由
from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import path,include
from . import views
urlpatterns = [
  #  path('admin/', admin.site.urls)
    path('',views.webindex,name="webindex"),
]
