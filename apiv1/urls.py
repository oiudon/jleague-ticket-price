from django.urls import path

from apiv1 import views

app_name = "apiv1"
urlpatterns = [
    # 1.チケット価格モデルの取得（一覧）
    path("ticketprices/", views.TicketPriceListAPIView.as_view()),
    # 試合タイトルと日時だけを取得
    path("matchtitledatetime/", views.MatchTitleDatetimeListAPIView.as_view()),
]
