from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

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
