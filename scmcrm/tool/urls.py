# 程序后台子路由
from django.urls import path
from .views import index, user, Customer

urlpatterns = (
    path("", index.index, name='index'),

    # 用户管理路由
    path('user/<int:pIndex>', user.index, name='userindex'),  #用户首页
    path('user/add', user.add, name='useradd'),   # 加载添加用户页面
    path('user/insert', user.insert, name='userinsert'),  # 加载添加用户页面
    path('user/delete/<int:uid>', user.delete, name='userdelete'),  # 删除用户
    path('user/edit/<int:uid>', user.edit, name='useredit'),  # 编辑用户
    path('user/update/<int:uid>', user.update, name='userupdate'),  # 编辑用户

    # 客户管理路由
    path('Customer/<int:pIndex>', Customer.index, name='Customerindex'),  # 客户首页
    path('Customer/add', Customer.add, name='Customeradd'),  # 加载添加客户页面
    path('Customer/insert', Customer.insert, name='Customerinsert'),  # 执行添加客户页面
    path('Customer/delete/<int:uid>', Customer.delete, name='Customerdelete'),  # 执行删除客户
    path('Customer/edit/<int:uid>', Customer.edit, name='Customeredit'),  # 修改客户页面
    path('Customer/update/<int:uid>', Customer.update, name='Customerupdate'),  # 修改客户页面
)
