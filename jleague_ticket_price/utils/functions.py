import logging
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

import environ
import pytz
import requests
from bs4 import BeautifulSoup
from django.db import transaction

from jleague_ticket_price.models import (
    Competition,
    League,
    SeatCategory,
    Stadium,
    Team,
    TicketPrice,
)

logger = logging.getLogger(__name__)

japan_timezone = pytz.timezone("Asia/Tokyo")


@transaction.atomic
def ticket_price_scraping():
    logger.info("チケット価格スクレイピング開始")

    # Jリーグチケットサイトを取得して解析
    base_url = "https://www.jleague-ticket.jp"
    html = requests.get(base_url)
    soup = BeautifulSoup(html.content, "html.parser")

    # チーム一覧を取得
    ji_teams = soup.find(class_="js-matchheight")

    # リーグ名を取得
    league_name = soup.find(class_="top-club-j1").text.strip().split("(")[0]
    # リーグ名がリーグマスタに未登録なら登録
    if not League.objects.filter(league_name=league_name).exists():
        league = League.objects.create(league_name=league_name)
        print(f"未登録のリーグ名：{league} を登録しました")
    else:
        league = League.objects.get(league_name=league_name)

    for element in ji_teams.find_all("li"):
        # チームコードを抽出
        team_code_url = element.find("a")["href"]
        team_code = team_code_url.split("/")[2]

        # チーム名を取得
        team_url = base_url + team_code_url
        html = requests.get(team_url)
        soup = BeautifulSoup(html.content, "html.parser")

        team_name = soup.find("title").text.strip().split(" | ")[0]
        print("---------" + team_name + "---------")

        # チケット販売中の試合の情報を取得
        game_list = soup.find(class_="game-list")

        # チーム名がチームマスタに未登録なら登録
        if not Team.objects.filter(team_name=team_name, team_code=team_code).exists():
            team = Team.objects.create(
                team_name=team_name, team_code=team_code, m_league=league
            )
            print(f"未登録のチーム名：{team} を登録しました")
        else:
            team = Team.objects.get(team_name=team_name, team_code=team_code)
            # 所属リーグが異なっている場合更新
            if team.m_league != league:
                team.m_league = league
                team.save()
                print(f"チーム名：{team} の所属リーグを更新しました")

        # チケット価格を取得
        try:
            for element in game_list.find_all("li"):
                # 大会名を取得
                competition_name = element.find(class_="comp-ttk").text.strip()

                # 大会名が大会マスタに未登録なら登録
                if not Competition.objects.filter(
                    competition_name=competition_name
                ).exists():
                    competition = Competition.objects.create(
                        competition_name=competition_name
                    )
                    print(f"未登録の大会名：{competition} を登録しました")
                else:
                    competition = Competition.objects.get(
                        competition_name=competition_name
                    )

                # 試合開催日時を取得
                day = element.find(class_="vs-box-info-day").text
                time = element.find(class_="vs-box-info-time").text

                datetime_str = f"2024/{day} {time}"
                match_datetime = japan_timezone.localize(
                    datetime.strptime(datetime_str, "%Y/%m/%d %H:%M")
                )

                # 試合タイトルを取得
                try:
                    match_title = "vs " + element.find(class_="team-name").text
                except AttributeError as e:
                    match_title = element.find(class_="vs-box-vs-place").find("p").text

                # スタジアム名を取得
                try:
                    stadium_name = element.find(class_="vs-box-place").find("span").text
                except AttributeError as e:
                    stadium_name = (
                        element.find(class_="vs-box-vs-place").find("span").text
                    )

                # スタジアム名がスタジアムマスタに未登録なら登録
                if not Stadium.objects.filter(stadium_name=stadium_name).exists():
                    stadium = Stadium.objects.create(stadium_name=stadium_name)
                    print(f"未登録のスタジアム名：{stadium} を登録しました")
                else:
                    stadium = Stadium.objects.get(stadium_name=stadium_name)

                # チケット価格情報を取得
                ticket_url = base_url + element.find(class_="ticket-status")["href"]

                # チケット情報を取得して解析
                ticket_html = requests.get(ticket_url)
                ticket_soup = BeautifulSoup(ticket_html.content, "html.parser")
                ticket_list = ticket_soup.find(class_="seat-select-list")

                for ticket_element in ticket_list.find_all(
                    class_="seat-select-list-txt"
                ):
                    # 座席カテゴリ名を取得
                    seat_category_name = ticket_element.find("h4").text

                    # チケット価格を取得
                    price = ticket_element.find("p").text
                    if not price:
                        continue

                    matches = re.findall(r"\d+", price)
                    price = int(matches[-1])

                    # 座席カテゴリ名が座席カテゴリマスタに未登録なら登録
                    if not SeatCategory.objects.filter(
                        m_stadium=stadium, seat_category_name=seat_category_name
                    ).exists():
                        seat_category = SeatCategory.objects.create(
                            m_stadium=stadium, seat_category_name=seat_category_name
                        )
                        print(f"未登録の座席カテゴリ名：{seat_category} を登録しました")
                    else:
                        seat_category = SeatCategory.objects.get(
                            m_stadium=stadium, seat_category_name=seat_category_name
                        )

                    # チケット価格を登録（登録済みならスキップ）
                    if not TicketPrice.objects.filter(
                        created_at=datetime.today().date(),
                        match_title=match_title,
                        m_seat_category=seat_category,
                    ).exists():
                        ticket_price = TicketPrice.objects.create(
                            created_at=datetime.today().date(),
                            m_team=team,
                            m_competition=competition,
                            match_datetime=match_datetime,
                            match_title=match_title,
                            m_stadium=stadium,
                            m_seat_category=seat_category,
                            price=price,
                        )
                        print(
                            f"{str(match_datetime)} {match_title} {seat_category}チケット価格：{ticket_price} を登録しました"
                        )
                    else:
                        ticket_price = TicketPrice.objects.get(
                            created_at=datetime.today().date(),
                            match_title=match_title,
                            m_seat_category=seat_category,
                        )
                        print(
                            f"{str(match_datetime)} {match_title} {seat_category}チケット価格：{ticket_price} は登録済みです"
                        )
        except AttributeError as e:
            continue

    logger.info("チケット価格スクレイピング完了")


def cleanup_logs():
    logger.info("ログ削除処理開始")

    BASE_DIR = Path(__file__).resolve().parent.parent
    env = environ.Env()
    # もし.envファイルが存在したら設定を読み込む
    environ.Env.read_env(BASE_DIR / "config/.env")

    # ログファイルのディレクトリ
    log_dir = env("LOG_DIR")
    # 保持期間を1週間に設定
    retention_period = timedelta(days=7)
    now = time.time()
    if not os.path.exists(log_dir):
        logger.error(f"Log directory {log_dir} does not exist.")
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
                print(f"Deleted log file: {file_path}")
            else:
                print(f"Retaining log file: {file_path}")

    logger.info("ログ削除処理完了")
