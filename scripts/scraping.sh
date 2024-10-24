#!/bin/bash

# Djangoプロジェクトのディレクトリに移動
cd /home/juser/jleague-ticket-price

# 仮想環境を有効化
source venv/bin/activate

# Djangoの管理コマンドを実行
python manage.py scraping