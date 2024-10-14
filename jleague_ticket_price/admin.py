from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Competition, League, SeatCategory, Stadium, Team, TicketPrice


# TicketPriceモデルに統合する為にModelResourceを継承したクラスを作成
class TicketPriceResource(resources.ModelResource):
    class Meta:
        model = TicketPrice


@admin.register(TicketPrice)
class TicketPriceAdmin(ImportExportModelAdmin):
    list_display = (
        "id",  # 1.レコードID
        "created_at",  # 2.登録日時
        "m_team",  # 3.チームID
        "m_competition",  # 4.大会ID
        "match_datetime",  # 5.試合開催日時
        "match_title",  # 6.試合タイトル
        "m_stadium",  # 7.スタジアムID
        "m_seat_category",  # 8.座席カテゴリID
        "format_price",  # 9.価格
    )
    list_display_links = ("id", "format_price")

    def format_price(self, obj):
        """価格フィールドのフォーマットを変更する"""
        if obj.price is not None:
            return "{:,d} 円".format(obj.price)

    # 価格フィールドのカラム名を指定
    format_price.short_description = "価格"
    # カラム名を押下時のソートを有効化
    format_price.admin_order_field = "price"

    # 初期表示時のソート項目を指定
    ordering = ("id",)

    # 簡易検索に使用するフィールドを指定
    search_fields = ("id", "match_datetime", "match_title")

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = TicketPriceResource


# Teamモデルに統合する為にModelResourceを継承したクラスを作成
class TeamResource(resources.ModelResource):
    class Meta:
        model = Team


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = (
        "id",  # 1.レコードID
        "team_name",  # 2.チーム名
        "team_code",  # 3.チームコード
        "m_league",  # 4.リーグID
    )

    # 初期表示時のソート項目を指定
    ordering = ("id",)

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = TeamResource


# Competitionモデルに統合する為にModelResourceを継承したクラスを作成
class CompetitionResource(resources.ModelResource):
    class Meta:
        model = Competition


@admin.register(Competition)
class CompetitionAdmin(ImportExportModelAdmin):
    list_display = (
        "id",  # 1.レコードID
        "competition_name",  # 2.大会名
    )

    # 初期表示時のソート項目を指定
    ordering = ("id",)

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = CompetitionResource


# Stadiumモデルに統合する為にModelResourceを継承したクラスを作成
class StadiumResource(resources.ModelResource):
    class Meta:
        model = Stadium


@admin.register(Stadium)
class StadiumAdmin(ImportExportModelAdmin):
    list_display = (
        "id",  # 1.レコードID
        "stadium_name",  # 2.スタジアム名
    )

    # 初期表示時のソート項目を指定
    ordering = ("id",)

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = StadiumResource


# SeatCategoryモデルに統合する為にModelResourceを継承したクラスを作成
class SeatCategoryResource(resources.ModelResource):
    class Meta:
        model = SeatCategory


@admin.register(SeatCategory)
class SeatCategoryAdmin(ImportExportModelAdmin):
    list_display = (
        "id",  # 1.レコードID
        "m_stadium",  # 2.スタジアムID
        "seat_category_name",  # 3.座席カテゴリ名
    )

    # 初期表示時のソート項目を指定
    ordering = ("id",)

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = SeatCategoryResource


# Leagueモデルに統合する為にModelResourceを継承したクラスを作成
class LeagueResource(resources.ModelResource):
    class Meta:
        model = League


@admin.register(League)
class LeagueAdmin(ImportExportModelAdmin):
    list_display = (
        "id",  # 1.レコードID
        "league_name",  # 2.リーグ名
    )

    # 初期表示時のソート項目を指定
    ordering = ("id",)

    # resource_classにModelResourceを継承したクラスを設定
    resource_class = LeagueResource
