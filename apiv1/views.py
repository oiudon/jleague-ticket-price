"""DRF用ビュー"""

from django.db.models.functions import ExtractYear
from django_filters import rest_framework as filters
from rest_framework import generics

from jleague_ticket_price.models import TicketPrice

from .serializers import (
    MatchTitleDatetimeSerializer,
    SeatCategorySerializer,
    TeamListSerializer,
    TicketPriceSerializer,
    TicketYearSerializer,
)


class TicketPriceFilter(filters.FilterSet):
    """
    チケット価格用フィルターセットクラス

        * URLのクエリパラメータで絞り込むフィルター
        * year、seat_category_name、team_nameで絞り込み可能
    """

    # 年だけで抽出するフィルター
    year = filters.CharFilter(method="filter_by_year")
    # 関連先のseat_category_nameで抽出するフィルター
    seat_category_name = filters.CharFilter(
        field_name="m_seat_category__seat_category_name", lookup_expr="exact"
    )
    # 関連先の team_name で抽出するフィルターを追加
    team_name = filters.CharFilter(field_name="m_team__team_name", lookup_expr="exact")

    class Meta:
        # フィルターに使用するモデルを指定
        model = TicketPrice
        # フィルターに使用するフィールドを指定
        fields = {
            "match_title": ["exact", "icontains"],
            "price": ["exact", "gte", "lte"],  # 価格フィルタ（完全一致、以上、以下）
            "m_competition": ["exact"],  # 大会名
            "m_stadium": ["exact"],  # スタジアム
            "m_team": ["exact"],  # チーム
            "match_datetime": ["exact", "year__gte", "year__lte"],  # 日時フィルタ
        }

    def filter_by_year(self, queryset, name, value):
        """
        クエリパラメータ"year"からで受け取った値で絞り込む

            * "2024年"を受け取ったら、"2024"部分のみ抽出して、年で絞り込む

        Args:
            value: クエリパラメータ（year）
        Returns:
            yearで抽出されたチケット価格モデル一覧
        """

        # "2024年" のような値から年だけを抽出
        year = value[:4]
        # 試合開催日付が指定された年のものをフィルタリング
        return queryset.filter(match_datetime__year=year)


class TicketPriceListAPIView(generics.ListAPIView):
    """
    1.チケット価格モデルの取得（一覧）APIクラス

        * created_at と price のみ取得する
        * TicketPriceFilterを使用
        * URL："api/v1/ticket-prices/"
    """

    # created_at と price のみ取得
    queryset = queryset = TicketPrice.objects.values("created_at", "price")
    serializer_class = TicketPriceSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TicketPriceFilter


class MatchTitleDatetimeListAPIView(generics.ListAPIView):
    """
    試合タイトルと日時、大会名、スタジアム名だけを取得するAPIクラス

        * 試合タイトルと日時、大会名、スタジアム名の一意な結果を取得する
        * TicketPriceFilterを使用
        * URL："api/v1/match-title-datetime/"
    """

    serializer_class = MatchTitleDatetimeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TicketPriceFilter

    def get_queryset(self):
        """
        試合タイトルと日時、大会名、スタジアム名の一意な結果を取得

        Args:
            self
        Returns:
            試合タイトルと日時、大会名、スタジアム名の一意な結果
        """
        queryset = TicketPrice.objects.select_related("m_competition", "m_stadium")
        return (
            self.filter_queryset(queryset)
            .distinct(
                "match_title",
                "match_datetime",
                "m_competition__competition_name",
                "m_stadium__stadium_name",
            )
            .order_by("match_datetime")
        )


class TicketYearListAPIView(generics.ListAPIView):
    """
    試合の年の一覧を取得するビュー

        * チケット価格一覧からmatch_datetimeの年の値を一意に抽出する
        * URL："api/v1/ticket-years/"
    """

    serializer_class = TicketYearSerializer

    def get_queryset(self):
        """
        match_datetimeの年を抽出し、重複を排除したクエリセットを作成

        Args:
            self
        Returns:
            チケット価格一覧から抽出したmatch_datetimeの年の一意な値
        """
        return TicketPrice.objects.annotate(
            match_year=ExtractYear("match_datetime")
        ).distinct("match_year")


class SeatCategoryListAPIView(generics.ListAPIView):
    """
    選択された試合の座席カテゴリのリストを取得するAPIクラス

        * 選択された試合の座席カテゴリのリストを取得する
        * URL："api/v1/seat-categories/"
    """

    serializer_class = SeatCategorySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = "__all__"

    def get_queryset(self):
        """
        選択した試合の座席カテゴリの一意な結果を取得

        Args:
            self
        Returns:
            選択した試合の座席カテゴリの一意な結果
        """
        queryset = TicketPrice.objects.select_related("m_seat_category")
        return self.filter_queryset(queryset).distinct(
            "m_seat_category__seat_category_name",
        )


class TeamListAPIView(generics.ListAPIView):
    """
    選択された年のチームのリストを取得するAPIクラス

        * 選択された年のチームのリストを取得する
        * TicketPriceFilterを使用
        * URL："api/v1/teams/"
    """

    serializer_class = TeamListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TicketPriceFilter

    def get_queryset(self):
        """
        選択された年のチームのリストを一意な結果で取得

        Args:
            self
        Returns:
            選択された年のチームのリストの一意な結果
        """
        queryset = TicketPrice.objects.select_related("m_team")
        return self.filter_queryset(queryset).distinct(
            "m_team__team_name",
        )
