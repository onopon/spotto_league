# SPOTTOのリーグ戦情報やユーザポイントの入力サービス

## 開発環境準備
### Pythonのversion
4.3.1

```
$ pyenv install 4.3.1
```

などによって、4.3.1をインストールする。

もし、これで

```
Ignoring ensurepip failure: pip 1.5.6 requires SSL/TLS
```

のようなエラーが出流場合は、

```
$ sudo apt install libssl1.0-dev
$ pyenv install 3.4.1
```

と行う。（mac, linuxでこの辺りのエラーは検出済み）

###  dbを用意
```
brew install mysql
mysql.server start
```

などで、

```
ホスト:localhost
ユーザ名：root
パスワード：なし
```

でmysqlにアクセスできる状態を作っておく。

mysqlにログインし、

```
create database spotto_dev
```

をし、spotto_dev DBを作成する。


### poetryのinstallを行う

```
poetry install
```

### tableのmigrate
詳しくはこの辺参照。

https://qiita.com/shirakiya/items/0114d51e9c189658002e

```
$poetry run python manage.py db migrate    # spotto_leagus/models 内のファイルの追加や変更を行うたびに叩いて、migration/versions 内のファイルを生成する
$poetry run python manage.py db upgrade    # mysqlへの反映が行われていない時に叩く
$poetry run python manage.py db downgrade  # mysqlの反映を巻き戻す時に叩く
```

### master dataの準備

LeaguePointを準備する。
```
$poetry run python -m spotto_league.scripts.add_league_point
```

### Adminユーザの準備

Adminユーザに昇格する場合は、下記のコマンドを実行する。

ex) onoponをAdminにする場合

```
$poetry run python -m spotto_league.scripts.add_role --login_name=onopon --role_type=1
```

### fmtファイルからファイルを生成

#### settings.py の生成

```
$ cp settings.py.fmt settings.py
```

本番環境の場合、 `ENV = "production"` とする。

#### instance/config/production.py の生成（production環境のみ）

```
$ instance/config/production.py.fmt instance/config/production.py
```

ROOT, PASSWORD, HOST, DBの値を書き換える。

### 開発環境の起こし方

下記で起動

```
$ export FLASK_APP=application.py
$ poetry run python -m flask run
```

Basic認証周りはinstance/config以下に書きます。
