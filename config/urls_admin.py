"""
管理サイト用URLConf

    * 本番環境で管理サイトへのアクセス分断するために切り出した管理サイトURLConf
"""

from django.contrib import admin
from django.urls import path

# 管理サイト用URL
urlpatterns = [
    path("admin/", admin.site.urls),
]
