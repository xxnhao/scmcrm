# 程序后台子路由
from django.urls import path
from .views import index, user, Customer,Customer_checks

urlpatterns = (
    path("", index.index, name='index'),

    # 用户管理路由
    path('user/<int:pIndex>', user.index, name='user_index'),  #用户首页
    path('user/add', user.add, name='user_add'),   # 加载添加用户页面
    path('user/insert', user.insert, name='user_insert'),  # 加载添加用户页面
    path('user/delete/<int:uid>', user.delete, name='user_delete'),  # 删除用户
    path('user/edit/<int:uid>', user.edit, name='user_edit'),  # 编辑用户
    path('user/update/<int:uid>', user.update, name='user_update'),  # 编辑用户

    # 客户管理路由
    path('Customer/<int:pIndex>', Customer.index, name='Customer_index'),  # 客户首页
    path('Customer/add', Customer.add, name='Customer_add'),  # 加载添加客户页面
    path('Customer/insert', Customer.insert, name='Customer_insert'),  # 执行添加客户页面
    path('Customer/delete/<int:uid>', Customer.delete, name='Customer_delete'),  # 执行删除客户
    path('Customer/edit/<int:uid>', Customer.edit, name='Customer_edit'),  # 修改客户页面
    path('Customer/update/<int:uid>', Customer.update, name='Customer_update'),  # 修改客户页面

    # 客户门店查询路由
    path('Customer_checks/<int:pIndex>',Customer_checks.index,name='Customer_checks_index'),  # 客户首页
)
