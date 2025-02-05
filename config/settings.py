"""
本番環境用設定ファイル

    * 本番環境用の設定を記述している
"""

from datetime import timedelta
from pathlib import Path

import environ

# from django.utils import timezone
# from django.utils.timezone import localtime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# もし.envファイルが存在したら設定を読み込む
environ.Env.read_env(BASE_DIR / "config/.env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

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
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # corsheaders
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "TIME_ZONE": "Asia/Tokyo",
        # "TEST": {
        #     "MIRROR": "default",  # テスト用DBは作成せず、デフォルトのDBを使用する
        # },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = "/var/www/jleague-ticket-price/static"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

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
            "filename": env("LOG_DIR") + "app.log",
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
}

# dj-rest-auth
REST_USE_JWT = True

# django-rest-framework-simplejwt
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
}

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
