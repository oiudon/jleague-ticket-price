"""モデル"""

from django.db import models


class League(models.Model):
    """
    6.リーグマスタ

    外部キー：
        * なし
    """

    class Meta:
        # テーブル名
        db_table = "m_league"
        # 管理サイトで使用するテーブル名
        verbose_name = verbose_name_plural = "6.リーグマスタ"

    # 1.レコードID
    id = models.AutoField(verbose_name="レコードID", primary_key=True)
    # 2.リーグ名
    league_name = models.CharField(verbose_name="リーグ名", max_length=50, unique=True)

    def __str__(self):
        return self.league_name


class Team(models.Model):
    """
    2.チームマスタ

    外部キー：
        * 6.リーグマスタ
    """

    class Meta:
        # テーブル名
        db_table = "m_team"
        # 管理サイトで使用するテーブル名
        verbose_name = verbose_name_plural = "2.チームマスタ"

    # 1.レコードID
    id = models.AutoField(verbose_name="レコードID", primary_key=True)
    # 2.チーム名
    team_name = models.CharField(verbose_name="チーム名", max_length=50, unique=True)
    # 3.チームコード
    team_code = models.CharField(
        verbose_name="チームコード", max_length=50, unique=True
    )
    # 4.リーグID
    m_league = models.ForeignKey(
        League, verbose_name="リーグID", on_delete=models.PROTECT
    )

    def __str__(self):
        return self.team_name


class Competition(models.Model):
    """
    3.大会マスタ

    外部キー：
        * なし
    """

    class Meta:
        # テーブル名
        db_table = "m_competition"
        # 管理サイトで使用するテーブル名
        verbose_name = verbose_name_plural = "3.大会マスタ"

    # 1.レコードID
    id = models.AutoField(verbose_name="レコードID", primary_key=True)
    # 2.大会名
    competition_name = models.CharField(
        verbose_name="大会名", max_length=50, unique=True
    )

    def __str__(self):
        return self.competition_name


class Stadium(models.Model):
    """
    4.スタジアムマスタ

    外部キー：
        * なし
    """

    class Meta:
        # テーブル名
        db_table = "m_stadium"
        # 管理サイトで使用するテーブル名
        verbose_name = verbose_name_plural = "4.スタジアムマスタ"

    # 1.レコードID
    id = models.AutoField(verbose_name="レコードID", primary_key=True)
    # 2.スタジアム名
    stadium_name = models.CharField(
        verbose_name="スタジアム名", max_length=50, unique=True
    )

    def __str__(self):
        return self.stadium_name


class SeatCategory(models.Model):
    """
    5.座席カテゴリマスタ

    外部キー：
        * 4.スタジアムマスタ
    """

    class Meta:
        # テーブル名
        db_table = "m_seat_category"
        # 管理サイトで使用するテーブル名
        verbose_name = verbose_name_plural = "5.座席カテゴリマスタ"
        constraints = [
            # スタジアムIDと座席カテゴリ名でユニーク制約
            models.UniqueConstraint(
                fields=["m_stadium", "seat_category_name"], name="unique_seat_category"
            )
        ]

    # 1.レコードID
    id = models.AutoField(verbose_name="レコードID", primary_key=True)
    # 2.スタジアムID
    m_stadium = models.ForeignKey(
        Stadium, verbose_name="スタジアムID", on_delete=models.PROTECT
    )
    # 3.座席カテゴリ名
    seat_category_name = models.CharField(verbose_name="座席カテゴリ名", max_length=50)

    def __str__(self):
        return self.seat_category_name


class TicketPrice(models.Model):
    """
    1.チケット価格

    外部キー：
        * 2.チームマスタ
        * 3.大会マスタ
        * 4.スタジアムマスタ
        * 5.座席カテゴリマスタ
    """

    class Meta:
        # テーブル名
        db_table = "t_ticket_price"
        # 管理サイトで使用するテーブル名
        verbose_name = verbose_name_plural = "1.チケット価格"

    # 1.レコードID
    id = models.AutoField(verbose_name="レコードID", primary_key=True)
    # 2.登録日
    created_at = models.DateField(verbose_name="登録日", auto_now_add=True)
    # 3.チームID
    m_team = models.ForeignKey(Team, verbose_name="チームID", on_delete=models.PROTECT)
    # 4.大会ID
    m_competition = models.ForeignKey(
        Competition, verbose_name="大会ID", on_delete=models.PROTECT
    )
    # 5.試合開催日時
    match_datetime = models.DateTimeField(verbose_name="試合開催日時")
    # 6.試合タイトル
    match_title = models.CharField(verbose_name="試合タイトル", max_length=255)
    # 7.スタジアムID
    m_stadium = models.ForeignKey(
        Stadium, verbose_name="スタジアムID", on_delete=models.PROTECT
    )
    # 8.座席カテゴリID
    m_seat_category = models.ForeignKey(
        SeatCategory, verbose_name="座席カテゴリID", on_delete=models.PROTECT
    )
    # 9.価格
    price = models.IntegerField(verbose_name="価格", null=True, blank=True)

    def __str__(self):
        return str(self.price) + "円"
