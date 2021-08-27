# SPOTTOのリーグ戦情報やユーザポイントの入力サービス

## 開発環境準備
### Pythonのversion
3.7.3

```
$ pyenv install 3.7.3
```

などによって、4.3.1をインストールする。

もし、これで

```
Ignoring ensurepip failure: pip 1.5.6 requires SSL/TLS
```

のようなエラーが出る場合は、

```
$ sudo apt install libssl1.0-dev
$ pyenv install 3.7.3
```

と行う。（mac, linuxでこの辺りのエラーは検出済み）

mac bigsurで
```
 implicit declaration of function 'sendfile' is invalid in C99 [-Werror,-Wimplicit-function-declaration]
```
が出た人は、
```
CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include" LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib" pyenv install --patch 3.7.3 < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index\=1)
```
を実行したら治るかもしれない。。

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
create database spotto_dev;
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

Docker上でやる場合はこっち。
```
$docker-compose exec test-app python manage.py db migrate
$docker-compose exec test-app python manage.py db upgrade
$docker-compose exec test-app python manage.py db downgrade
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

#### instance/settings.py の生成

```
$ cp settings.py.fmt instance/settings.py
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
