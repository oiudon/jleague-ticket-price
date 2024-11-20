"""
汎用関数のユニットテスト

    * コマンド(全てのテスト)：python manage.py test --settings config.local_settings
    * コマンド(汎用関数のみ)：python manage.py test apiv1.tests.test_views --settings config.local_settings
"""

from django.test import TestCase

from jleague_ticket_price.utils.functions import ticket_price_scraping


class TestTicketPriceScraping(TestCase):
    """scraping関数のテスト"""

    # テスト用DBに使用するFixtureファイルを指定
    fixtures = ["jleague_ticket_price/fixtures/example_fixture.json"]

    def test_scraping_success(self):
        """
        チケット価格スクレイピングが最後まで完了することを検証

            * スクレイピング関数が True 返せば成功
        """

        result = ticket_price_scraping()

        self.assertTrue(result)


# class TestCleanupLogs(TestCase):

#     def test_cleanup_logs_success(self):
#         """
#         ログ削除関数が最後まで完了することを検証

#             * ログ削除関数が True 返せば成功
#         """

#         result = cleanup_logs()

#         self.assertTrue(result)
