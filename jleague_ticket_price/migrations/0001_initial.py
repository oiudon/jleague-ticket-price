# Generated by Django 3.2.25 on 2024-08-13 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='レコードID')),
                ('competition_name', models.CharField(max_length=50, unique=True, verbose_name='大会名')),
            ],
            options={
                'verbose_name': '3.大会マスタ',
                'verbose_name_plural': '3.大会マスタ',
                'db_table': 'm_competition',
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='レコードID')),
                ('league_name', models.CharField(max_length=50, unique=True, verbose_name='リーグ名')),
            ],
            options={
                'verbose_name': '6.リーグマスタ',
                'verbose_name_plural': '6.リーグマスタ',
                'db_table': 'm_league',
            },
        ),
        migrations.CreateModel(
            name='SeatCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='レコードID')),
                ('seat_category_name', models.CharField(max_length=50, verbose_name='座席カテゴリ名')),
            ],
            options={
                'verbose_name': '5.座席カテゴリマスタ',
                'verbose_name_plural': '5.座席カテゴリマスタ',
                'db_table': 'm_seat_category',
            },
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='レコードID')),
                ('stadium_name', models.CharField(max_length=50, unique=True, verbose_name='スタジアム名')),
            ],
            options={
                'verbose_name': '4.スタジアムマスタ',
                'verbose_name_plural': '4.スタジアムマスタ',
                'db_table': 'm_stadium',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='レコードID')),
                ('team_name', models.CharField(max_length=50, unique=True, verbose_name='チーム名')),
                ('team_code', models.CharField(max_length=50, unique=True, verbose_name='チームコード')),
                ('m_league', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jleague_ticket_price.league', verbose_name='リーグID')),
            ],
            options={
                'verbose_name': '2.チームマスタ',
                'verbose_name_plural': '2.チームマスタ',
                'db_table': 'm_team',
            },
        ),
        migrations.CreateModel(
            name='TicketPrice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='レコードID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日時')),
                ('match_datetime', models.DateTimeField(verbose_name='試合開催日時')),
                ('match_title', models.CharField(max_length=255, verbose_name='試合タイトル')),
                ('home_flag', models.BooleanField(default=True, verbose_name='ホームフラグ')),
                ('child_price', models.IntegerField(blank=True, null=True, verbose_name='小人価格')),
                ('adult_price', models.IntegerField(blank=True, null=True, verbose_name='大人価格')),
                ('member_price_flag', models.BooleanField(default=False, verbose_name='会員価格フラグ')),
                ('m_competition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jleague_ticket_price.competition', verbose_name='大会ID')),
                ('m_seat_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jleague_ticket_price.seatcategory', verbose_name='座席カテゴリID')),
                ('m_stadium', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jleague_ticket_price.stadium', verbose_name='スタジアムID')),
                ('m_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jleague_ticket_price.team', verbose_name='チームID')),
            ],
            options={
                'verbose_name': '1.チケット価格',
                'verbose_name_plural': '1.チケット価格',
                'db_table': 't_ticket_price',
            },
        ),
        migrations.AddField(
            model_name='seatcategory',
            name='m_stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='jleague_ticket_price.stadium', verbose_name='スタジアムID'),
        ),
        migrations.AddConstraint(
            model_name='seatcategory',
            constraint=models.UniqueConstraint(fields=('m_stadium', 'seat_category_name'), name='unique_seat_category'),
        ),
    ]
