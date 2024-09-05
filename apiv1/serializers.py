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
    """試合タイトルと日時だけを含むシリアライザ"""

    class Meta:
        # 対象のモデルクラスを指定
        model = TicketPrice
        # 利用するモデルのフィールドを指定
        fields = ["match_title", "match_datetime"]
        # 全フィールドを読み取り専用に設定
        read_only_fields = fields
