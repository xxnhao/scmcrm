
# 前台页面子路由
from django.urls import path,include
from . import views
urlpatterns = [
  #  path('admin/', admin.site.urls)
    path('',views.webindex,name="webindex"),
]
