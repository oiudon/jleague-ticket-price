"""
スクレイピングコマンド

    * 毎日定期実行するチケット価格のスクレイピングコマンドを定義している。
    * コマンド：python manage.py scraping
"""

from django.core.management.base import BaseCommand

from jleague_ticket_price.utils.functions import ticket_price_scraping


class Command(BaseCommand):
    """スクレイピング実行"""

    help = "スクレイピング実行コマンド"

    def handle(self, *args, **options):
        ticket_price_scraping()
