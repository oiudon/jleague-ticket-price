from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

admin.site.site_header = "管理サイト"
admin.site.site_title = "Jリーグチケット価格変動チェッカープロジェクト"
admin.site.index_title = "ホーム"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/", include("apiv1.urls")),
    re_path("", RedirectView.as_view(url="/")),
]
