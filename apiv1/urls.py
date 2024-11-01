"""DRF用URLConf"""

from django.urls import path

from apiv1 import views

app_name = "apiv1"
urlpatterns = [
    # 1.チケット価格モデルの取得（一覧）
    path("ticket-prices/", views.TicketPriceListAPIView.as_view()),
    # 試合タイトルと日時だけを取得
    path("match-title-datetime/", views.MatchTitleDatetimeListAPIView.as_view()),
    # 試合の年の一覧を取得
    path("ticket-years/", views.TicketYearListAPIView.as_view()),
    # 座席カテゴリを取得
    path("seat-categories/", views.SeatCategoryListAPIView.as_view()),
    # 試合の年のチーム一覧を取得
    path("teams/", views.TeamListAPIView.as_view()),
]
