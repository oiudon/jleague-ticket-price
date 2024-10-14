from django.core.management.base import BaseCommand

from jleague_ticket_price.utils.functions import cleanup_logs


class Command(BaseCommand):
    help = "1週間以上前のログファイルを削除"

    def handle(self, *args, **options):
        cleanup_logs()
