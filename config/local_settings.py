"""
開発環境用設定ファイル

    * 開発環境用の設定を記述している
    * 開発環境は管理サイトが閲覧可能
    * 起動法①：python manage.py runserver --settings config.local_settings
    * 起動法②：export DJANGO_SETTINGS_MODULE=config.local_settings 実行後普通に runserver
"""

from .settings import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

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

# データベース設定
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "jleagueticket-db",
        "USER": "admin",
        "PASSWORD": "pass",
        "HOST": "localhost",
        "PORT": "5432",
        "TIME_ZONE": "Asia/Tokyo",
        "TEST": {
            "MIRROR": "default",
        },
    }
}

# ロギング設定
LOGGING = {
    # スキーマバージョンは「1」固定
    "version": 1,
    # 既に作成されているロガーを無効化しないための設定
    "disable_existing_loggers": False,
    # ログフォーマット
    "formatters": {
        # 開発用
        "development": {
            "format": "[{name}] {asctime} [{levelname}] {pathname}:{lineno:d} "
            "{message}",
            "style": "{",
        },
    },
    "handlers": {
        # コンソール出力用ハンドラ
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "development",
        },
        # ファイル出力用ハンドラ
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/Users/mac/Documents/Django/jleague-ticket-price/log/"
            + "app.log",
            "when": "midnight",  # 毎日深夜0時にローテーション
            "interval": 1,  # 1日単位
            "backupCount": 7,  # ログファイルのバックアップ数
            "formatter": "development",
        },
    },
    # # ルートロガー
    # "root": {
    #     "handlers": ["console", "file"],
    #     "level": "INFO",
    # },
    # その他のロガー
    "loggers": {
        # Django本体が出力するログ全般を扱うロガー
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        # jleague_ticket_priceアプリが出力するログを扱うロガー
        "jleague_ticket_price": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        # apiv1アプリが出力するログを扱うロガー
        "apiv1": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
}

# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # DRF-spectacular
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
