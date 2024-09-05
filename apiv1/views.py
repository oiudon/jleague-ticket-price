from django_filters import rest_framework as filters
from rest_framework import generics

from jleague_ticket_price.models import TicketPrice

from .serializers import MatchTitleDatetimeSerializer, TicketPriceSerializer


class TicketPriceFilter(filters.FilterSet):
    """チケット価格用フィルターセットクラス"""

    year = filters.CharFilter(method="filter_by_year")

    class Meta:
        model = TicketPrice
        fields = []

    def filter_by_year(self, queryset, name, value):
        # "2024年" のような値から年だけを抽出
        year = value[:4]
        # 試合開催日付が指定された年のものをフィルタリング
        return (
            queryset.filter(match_datetime__year=year)
            .values("match_title", "match_datetime")
            .distinct()
        )


class TicketPriceListAPIView(generics.ListAPIView):
    """1.チケット価格モデルの取得（一覧）APIクラス"""

    queryset = TicketPrice.objects.all()
    serializer_class = TicketPriceSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = "__all__"


class MatchTitleDatetimeListAPIView(generics.ListAPIView):
    """試合タイトルと日時だけを取得するAPIクラス"""

    serializer_class = MatchTitleDatetimeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TicketPriceFilter

    def get_queryset(self):
        queryset = TicketPrice.objects.all()
        filtered_queryset = self.filter_queryset(queryset)
        return filtered_queryset.values("match_title", "match_datetime").distinct()
