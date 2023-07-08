from django.db import models
from datetime import datetime
# Create your models here.

# 用户账号信息模型
class User(models.Model):
    username = models.CharField(max_length=50)    # 员工账号
    nickname = models.CharField(max_length=50)    # 用户名
    password_hash = models.CharField(max_length=100)  # 密码
    password_salt = models.CharField(max_length=50)    # 密码干扰值
    status = models.IntegerField(default=1)    # 状态:1正常/2禁用/
    create_at = models.DateTimeField(default=datetime.now)    # 创建时间
    update_at = models.DateTimeField(default=datetime.now)    # 修改时间
    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    class Meta:
        db_table = "user"  # 更改表名

class Customer(models.Model):
    cs_name = models.CharField(max_length=50)  # 客户名称
    cs_url = models.CharField(max_length=50)  # 客户url
    cs_username = models.CharField(max_length=100)  # 客户账号
    cs_password = models.CharField(max_length=50)  # 客户密码
    cs_status = models.IntegerField(default=1)  # 状态:1正常/2流失/
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 修改时间

    def toDict(self):
        return {'id': self.id,'cs_name': self.cs_name,'cs_url': self.cs_url,
                'cs_username': self.cs_username,'cs_password': self.cs_password,'cs_status': self.cs_status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    class Meta:
        db_table = "Customer"   # 更改表名