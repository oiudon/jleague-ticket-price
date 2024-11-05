"""
本番環境管理サイト用設定ファイル

    * 本番環境で立ち上げる管理サイト用の設定ファイル
    * コマンド：Python manage.py runserver --settings config.production_admin
"""

from .settings import *

ROOT_URLCONF = "config.urls_admin"

# インストールアプリ
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # サードパーティアプリ
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "corsheaders",
    "django_filters",
    # Jリーグチケット価格アプリ
    "apiv1.apps.Apiv1Config",
    "jleague_ticket_price.apps.JleagueTicketPriceConfig",
    # 管理サイトのインポート・エクスポート機能
    "import_export",
    # # スケジューラ
    # "django_apscheduler",
    # admindocs
    "django.contrib.admindocs",
    # DRF-spectacular
    "drf_spectacular",
]
