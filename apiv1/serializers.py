from rest_framework import serializers

from jleague_ticket_price.models import TicketPrice


class TicketPriceSerializer(serializers.ModelSerializer):
    """1.チケット価格モデル用のシリアライザ"""

    # 関連先のモデルから取得するフィールドを指定
    team_name = serializers.ReadOnlyField(source="m_team.team_name")
    competition_name = serializers.ReadOnlyField(
        source="m_competition.competition_name"
    )
    stadium_name = serializers.ReadOnlyField(source="m_stadium.stadium_name")
    seat_category_name = serializers.ReadOnlyField(
        source="m_seat_category.seat_category_name"
    )

    class Meta:
        # 対象のモデルクラスを指定
        model = TicketPrice
        # 利用するモデルのフィールドを指定
        fields = [
            "id",
            "created_at",
            "team_name",
            "competition_name",
            "match_datetime",
            "match_title",
            "stadium_name",
            "seat_category_name",
            "price",
        ]
        # 全フィールドを読み取り専用に設定
        read_only_fields = fields


class MatchTitleDatetimeSerializer(serializers.ModelSerializer):
    """試合タイトルと日時、大会名、スタジアム名だけを含むシリアライザ"""

    # 関連先のモデル m_competition の competition_name を取得
    competition_name = serializers.ReadOnlyField(
        source="m_competition.competition_name"
    )

    # 関連先のモデル m_stadium の stadium_name を取得
    stadium_name = serializers.ReadOnlyField(source="m_stadium.stadium_name")

    class Meta:
        # 対象のモデルクラスを指定
        model = TicketPrice
        # 利用するモデルのフィールドを指定
        fields = ["match_title", "match_datetime", "competition_name", "stadium_name"]
        # 全フィールドを読み取り専用に設定
        read_only_fields = fields


class TicketYearSerializer(serializers.Serializer):
    """試合の年を取得するシリアライザ"""

    match_year = serializers.IntegerField()

    class Meta:
        fields = ["match_year"]


class SeatCategorySerializer(serializers.ModelSerializer):
    """選択された試合の座席カテゴリのリストを取得するシリアライザ"""

    # 関連先のモデル m_seat_category の seat_category_name を取得
    seat_category_name = serializers.ReadOnlyField(
        source="m_seat_category.seat_category_name"
    )

    class Meta:
        # 対象のモデルクラスを指定
        model = TicketPrice
        # 利用するモデルのフィールドを指定
        fields = ["seat_category_name"]
        # 全フィールドを読み取り専用に設定
        read_only_fields = fields


class TeamListSerializer(serializers.ModelSerializer):
    """選択した年のチームを取得するシリアライザ"""

    # 関連先のモデルから取得するフィールドを指定
    team_name = serializers.ReadOnlyField(source="m_team.team_name")

    class Meta:
        # 対象のモデルクラスを指定
        model = TicketPrice
        # 利用するモデルのフィールドを指定
        fields = [
            "team_name",
        ]
        # 全フィールドを読み取り専用に設定
        read_only_fields = fields
