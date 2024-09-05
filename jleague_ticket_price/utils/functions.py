import re
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from django.db import transaction

from jleague_ticket_price.models import (
    Competition,
    SeatCategory,
    Stadium,
    Team,
    TicketPrice,
)

japan_timezone = pytz.timezone("Asia/Tokyo")

# チケット価格を確認したいチーム
team = Team.objects.get(team_name="ＦＣ町田ゼルビア")

# チケット価格を確認したいチームのチームコード
team_code = team.team_code

# JリーグチケットサイトベースURL
base_url = "https://www.jleague-ticket.jp"

# Jリーグチケットサイトを取得して解析
load_url = base_url + "/club/" + team_code + "/"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

# チケット販売中の試合の情報を取得
game_list = soup.find(class_="game-list")


@transaction.atomic
def ticket_price_scraping():
    for element in game_list.find_all("li"):
        # 大会名を取得
        competition_name = element.find(class_="comp-ttk").text.strip()

        # 大会名が大会マスタに未登録なら登録
        if not Competition.objects.filter(competition_name=competition_name).exists():
            competition = Competition.objects.create(competition_name=competition_name)
            print(f"未登録の大会名：{competition} を登録しました")
        else:
            competition = Competition.objects.get(competition_name=competition_name)

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
            stadium_name = element.find(class_="vs-box-vs-place").find("span").text

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

        for ticket_element in ticket_list.find_all(class_="seat-select-list-txt"):
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
