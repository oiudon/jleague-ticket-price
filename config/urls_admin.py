"""
管理サイト用URLConf

    * 本番環境で管理サイトへのアクセス分断するために切り出した管理サイトURLConf
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# 管理サイト用URL追加
urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/", include("apiv1.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI 形式の API ドキュメント画面
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc 形式の API ドキュメント画面
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    re_path("", RedirectView.as_view(url="/")),
]
