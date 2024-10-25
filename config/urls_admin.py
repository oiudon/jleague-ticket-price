from django.contrib import admin
from django.urls import path

# 管理サイト用URL
urlpatterns = [
    path("admin/", admin.site.urls),
]
