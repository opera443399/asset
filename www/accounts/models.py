# coding=utf-8
# ----------------------------------
# @ 2017/3/20
# @ PC
# ----------------------------------

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='avatars/default.png', blank=True)
    gender = models.CharField(max_length=20, default='Secret')
    nickname = models.CharField(max_length=40, default='New Player')

    def __str__(self):
        return "{0}'s Profile".format(self.user.username)
