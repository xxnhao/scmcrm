from django.db import models
from django.utils import timezone

# 用户账号信息模型
class User(models.Model):
    username = models.CharField(max_length=50)    # 员工账号
    nickname = models.CharField(max_length=50)    # 用户名
    password_hash = models.CharField(max_length=100)  # 密码
    password_salt = models.CharField(max_length=50)    # 密码干扰值
    status = models.IntegerField(default=1)    # 状态:1正常/2禁用/
    create_at = models.DateTimeField(default=timezone.localtime)    # 创建时间
    update_at = models.DateTimeField(default=timezone.localtime)    # 修改时间
    class Meta:
        db_table = "user"  # 更改表名

class Customer(models.Model):
    cs_name = models.CharField(max_length=50)  # 客户名称
    cs_url = models.CharField(max_length=50)  # 客户url
    cs_username = models.CharField(max_length=100)  # 客户账号
    cs_password = models.CharField(max_length=50)  # 客户密码
    cs_AddrName = models.CharField(max_length=50, default="")  # 客户收件人
    cs_Address = models.CharField(max_length=200, default="")  # 客户地址
    cs_AddrPhone = models.CharField(max_length=50, default="")  # 客户联系电话
    cs_am = models.CharField(max_length=50, default="")  # 服务人员
    cs_status = models.IntegerField(default=1)  # 状态:1正常/2流失/
    update_at = models.DateTimeField(default=timezone.localtime)  # 修改时间
    class Meta:
        db_table = "Customer"   # 更改表名

class CustomerReport(models.Model):
    cs_id = models.CharField(max_length=50)  # 客户id
    cs_am = models.CharField(max_length=100)  # 客户负责人
    store_id = models.CharField(max_length=100)  # 门店ID
    store_name = models.CharField(max_length=50)  # 门店名称
    store_type = models.CharField(max_length=50,)  # 门店类型
    store_ex_time = models.DateField()  # 到期时间
    update_at = models.DateTimeField(default=timezone.localtime)  # 更新时间
    class Meta:
        db_table = "CustomerReport"  # 更改表名