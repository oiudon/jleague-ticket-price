# Generated by Django 3.2.25 on 2024-08-29 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jleague_ticket_price', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketprice',
            old_name='child_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='ticketprice',
            name='adult_price',
        ),
        migrations.RemoveField(
            model_name='ticketprice',
            name='home_flag',
        ),
        migrations.RemoveField(
            model_name='ticketprice',
            name='member_price_flag',
        ),
        migrations.AlterField(
            model_name='ticketprice',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='登録日'),
        ),
    ]
