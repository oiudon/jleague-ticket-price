"""
開発環境管理サイト用設定ファイル

    * 開発環境で立ち上げる管理サイト用の設定ファイル
    * コマンド：python manage.py runserver --settings config.local_admin
"""

from .local_settings import *

ROOT_URLCONF = "config.urls_admin"
