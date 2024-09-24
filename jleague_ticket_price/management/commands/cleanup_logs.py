import os
import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Deletes log files older than one week"

    def handle(self, *args, **kwargs):
        # ログファイルのディレクトリ
        log_dir = "/Users/mac/Documents/Django/jleague-ticket-price/log/"
        # 保持期間を1週間に設定
        retention_period = timedelta(days=7)
        now = time.time()

        if not os.path.exists(log_dir):
            self.stdout.write(
                self.style.ERROR(f"Log directory {log_dir} does not exist.")
            )
            return

        # ログディレクトリ内のファイルをチェック
        for filename in os.listdir(log_dir):
            file_path = os.path.join(log_dir, filename)

            # ファイルかつログファイル（適切にフィルタリング可能）
            if os.path.isfile(file_path) and filename.endswith(".log"):
                # ファイルの最終変更時刻を取得
                file_age = now - os.path.getmtime(file_path)
                # ファイルの年齢が7日を超えている場合、削除
                if file_age > retention_period.total_seconds():
                    os.remove(file_path)
                    self.stdout.write(
                        self.style.SUCCESS(f"Deleted log file: {file_path}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Retaining log file: {file_path}")
                    )
