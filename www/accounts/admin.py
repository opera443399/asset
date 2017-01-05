# coding=utf-8
# ----------------------------------
# @ 2017/1/4
# @ PC
# ----------------------------------

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Player

# Register your models here.

class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'Player'

class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
