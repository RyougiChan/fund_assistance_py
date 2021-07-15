import json

from django.db import models

from analysis.lib.utils import md5_digest


class Chives(models.Model):
    """韭菜账户"""
    id = models.AutoField(primary_key=True)
    # 登录名(仅大小写字母、数字、_)
    login_name = models.CharField(max_length=16)
    # 支持任意字符
    nickname = models.CharField(max_length=32)
    # 加密盐值
    salt = models.CharField(max_length=32)
    # 登录密码(加密后)
    login_password = models.CharField(max_length=64)

    objects = models.Manager()

    def match_password(self, login_password):
        """验证密码"""
        return self.login_password == md5_digest(login_password + self.salt)

    def __str__(self):
        return self.login_name
