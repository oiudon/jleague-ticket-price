"""URLConf"""

# from apscheduler.schedulers.background import BackgroundScheduler
# from dateutil import tz
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# from jleague_ticket_price.utils.functions import cleanup_logs, ticket_price_scraping

admin.site.site_header = "管理サイト"
admin.site.site_title = "Jリーグチケット価格変動チェッカープロジェクト"
admin.site.index_title = "ホーム"

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/", include("apiv1.urls")),
    re_path("", RedirectView.as_view(url="/")),
]

# scheduler = BackgroundScheduler(timezone=tz.gettz("Asia/Tokyo"))
# scheduler.add_jobstore(DjangoJobStore(), "default")


# @register_job(
#     scheduler,
#     "cron",
#     hour=9,
#     minute=30,
#     id="daily_task",
#     # 複数ワーカーのタスク同時実行防止（意味なかった）
#     max_instances=1,
#     replace_existing=True,
# )
# def daily_task():
#     ticket_price_scraping()
#     cleanup_logs()


# register_events(scheduler)
# scheduler.start()
