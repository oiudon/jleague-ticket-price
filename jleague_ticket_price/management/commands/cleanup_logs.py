"""
ログ削除コマンド

    * 毎日定期実行するログ削除コマンドを定義している。(1週間以上前のログファイルを削除)
    * コマンド：python manage.py cleanup_logs
    * 現在は不使用。
"""

from django.core.management.base import BaseCommand

from jleague_ticket_price.utils.functions import cleanup_logs


class Command(BaseCommand):
    """ログ消去実行"""

    help = "1週間以上前のログファイルを削除"

    def handle(self, *args, **options):
        cleanup_logs()
