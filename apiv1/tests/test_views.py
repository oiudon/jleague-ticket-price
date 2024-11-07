"""
DRFビューのユニットテスト

    * コマンド(全てのテスト)：python manage.py test --settings config.local_settings
    * コマンド(DRFビューのみ)：python manage.py test apiv1.tests.test_views --settings config.local_settings
"""

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestTicketPriceListAPIView(APITestCase):
    """TicketPriceListAPIViewのテスト"""

    def setUp(self):
        # APIClient のインスタンスを作成
        self.client = APIClient()
        # テストするエンドポイントの URL を指定
        self.url = "/api/v1/ticket-prices/"

    def test_get_success(self):
        """
        「/api/v1/ticket-prices/」への GET リクエストをすると、
        登録日とチケット価格の一覧を返すことを検証
        """

        # クエリパラメータを含む GET リクエストをシミュレート
        response = self.client.get(
            self.url,
            {
                "team_name": "ＦＣ町田ゼルビア",
                "match_datetime": "2024-09-21T19:00",
                "match_title": "vs 北海道コンサドーレ札幌",
                "seat_category_name": "ゼルビアサポーターズシート",
            },
            format="json",  # JSON 形式のレスポンスを期待
        )

        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスのJSONデータを取得
        data = response.json()

        # 各アイテムが "created_at" と "price" キーを持つことを検証
        for item in data:
            self.assertIn("created_at", item)
            self.assertIn("price", item)


class TestMatchTitleDatetimeListAPIView(APITestCase):
    """MatchTitleDatetimeListAPIViewのテスト"""

    def setUp(self):
        # APIClient のインスタンスを作成
        self.client = APIClient()
        # テストするエンドポイントの URL を指定
        self.url = "/api/v1/match-title-datetime/"

    def test_get_success(self):
        """
        「/api/v1/match-title-datetime/」への GET リクエストをすると、
        試合タイトルと日時、大会名、スタジアム名を返すことを検証
        """

        # クエリパラメータを含む GET リクエストをシミュレート
        response = self.client.get(
            self.url,
            {
                "year": "2024",
                "team_name": "ＦＣ町田ゼルビア",
            },
            format="json",  # JSON 形式のレスポンスを期待
        )

        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスのJSONデータを取得
        data = response.json()

        # 各アイテムが "match_title" と "match_datetime" 、
        # "competition_name" 、"stadium_name" キーを持つことを検証
        for item in data:
            self.assertIn("match_title", item)
            self.assertIn("match_datetime", item)
            self.assertIn("competition_name", item)
            self.assertIn("stadium_name", item)


class TestTicketYearListAPIView(APITestCase):
    """TicketYearListAPIViewのテスト"""

    def setUp(self):
        # APIClient のインスタンスを作成
        self.client = APIClient()
        # テストするエンドポイントの URL を指定
        self.url = "/api/v1/ticket-years/"

    def test_get_success(self):
        """
        「/api/v1/ticket-years/」への GET リクエストをすると、
        試合の年の一覧を返すことを検証
        """

        # クエリパラメータを含む GET リクエストをシミュレート
        response = self.client.get(
            self.url,
            format="json",  # JSON 形式のレスポンスを期待
        )

        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスのJSONデータを取得
        data = response.json()

        # 各アイテムが "match_year" キーを持つことを検証
        for item in data:
            self.assertIn("match_year", item)


class TestSeatCategoryListAPIView(APITestCase):
    """SeatCategoryListAPIViewのテスト"""

    def setUp(self):
        # APIClient のインスタンスを作成
        self.client = APIClient()
        # テストするエンドポイントの URL を指定
        self.url = "/api/v1/seat-categories/"

    def test_get_success(self):
        """
        「/api/v1/seat-categories/」への GET リクエストをすると、
        選択された試合の座席カテゴリのリストを返すことを検証
        """

        # クエリパラメータを含む GET リクエストをシミュレート
        response = self.client.get(
            self.url,
            {
                "match_datetime": "2024-09-21T19:00",
                "match_title": "vs 北海道コンサドーレ札幌",
            },
            format="json",  # JSON 形式のレスポンスを期待
        )

        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスのJSONデータを取得
        data = response.json()

        # 各アイテムが "seat_category_name" キーを持つことを検証
        for item in data:
            self.assertIn("seat_category_name", item)


class TestTeamListAPIView(APITestCase):
    """TeamListAPIViewのテスト"""

    def setUp(self):
        # APIClient のインスタンスを作成
        self.client = APIClient()
        # テストするエンドポイントの URL を指定
        self.url = "/api/v1/teams/"

    def test_get_success(self):
        """
        「/api/v1/teams/」への GET リクエストをすると、
        選択された年のチームのリストを返すことを検証
        """

        # クエリパラメータを含む GET リクエストをシミュレート
        response = self.client.get(
            self.url,
            {
                "year": "2024",
            },
            format="json",  # JSON 形式のレスポンスを期待
        )

        # ステータスコードが200であることを確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスのJSONデータを取得
        data = response.json()

        # 各アイテムが "team_name" キーを持つことを検証
        for item in data:
            self.assertIn("team_name", item)
