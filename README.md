# SPOTTOのリーグ戦情報やユーザポイントの入力サービス

## 開発環境準備
### Pythonのversion
4.3.1

###  dbを用意
brew install mysql
mysql.server start
などで、
ホスト:localhost
ユーザ名：root
パスワード：なし
でmysqlにアクセスできる状態を作っておく。
mysqlにログインし、
create database spotto_dev
をし、spotto_dev DBを作成する。


### tableのmigrate
詳しくはこの辺参照。
https://qiita.com/shirakiya/items/0114d51e9c189658002e
poetry run python manage.py db migrate    # spotto_leagus/models 内のファイルの追加や変更を行うたびに叩いて、migration/versions 内のファイルを生成する
poetry run python manage.py db upgrade    # mysqlへの反映が行われていない時に叩く
poetry run python manage.py db downgrade  # mysqlの反映を巻き戻す時に叩く


### 開発環境の起こし方
下記で起動
$ export FLASK_APP=application.py
$ poetry run python -m flask run

Basic認証周りはinstance/config以下に書きます。
