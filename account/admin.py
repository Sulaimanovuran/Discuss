from django.contrib import admin

from account.models import MyUser





class MyUser2(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'avatar']


admin.site.register(MyUser, MyUser2)
