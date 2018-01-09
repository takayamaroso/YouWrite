from django.contrib import admin

from .models import Article

#admin管理画面でさわれるようにする。
admin.site.register(Article)