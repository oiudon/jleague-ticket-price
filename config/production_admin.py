"""
本番環境管理サイト用設定ファイル

    * 本番環境で立ち上げる管理サイト用の設定ファイル
    * コマンド：Python manage.py runserver --settings config.production_admin
"""

from .settings import *

ROOT_URLCONF = "config.urls_admin"
