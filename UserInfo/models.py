from django.db import models


# 用户信息表
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.EmailField(null=True)
    username_role = models.CharField(max_length=32)
    regTime = models.DateTimeField(null=True)
    userState = models.BooleanField(null=True)


# 角色表
class Role(models.Model):
    role_name = models.CharField(max_length=32)


# 用户资料ID表
class UserSoft(models.Model):
    soft = models.CharField(max_length=32, null=False)
    username = models.CharField(max_length=32)
