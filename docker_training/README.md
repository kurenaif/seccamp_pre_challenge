# L-IVゼミでDockerに関してできてほしいこと

## このゼミの前にできていてほしいこと

1. コンテナ上でコードをビルドし、サーバーを起動する
2. docker-composeを使って複数コンテナを立て、コンテナ間で通信を行う

上記２つを確かめるための課題を出題します。
自明だなと思った問題に関しては飛ばしてもらって大丈夫です。

### Step1: Dockerをインストールして実行してみよう

macであれば `brew` , debian系であれば `apt` で入ります。
Windowsの場合は少し厄介なので、以下のページや適当にググってでてくるインストール方法などを参考に導入してください。
なにか詰まった場合はお気軽に連絡ください。
https://docs.docker.com/get-docker/

以下コマンドを実行し、うまく動いていれば大丈夫です。ubuntuの場合はsudoが必要な場合もあります。

```
docker run hello-world
```

### Step2: Docker上でPythonを動かしてみよう

以下のページを参考に、Docker上でPythonを動かしてみてください。

https://hub.docker.com/_/python

このページに書かれているように以下のように書けば環境構築可能です。

```Dockerfile
FROM python:3

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./server.py" ]
```

```py
import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
```

そして以下のコマンドでコンテナをbuildし、

```sh
docker build -t seccamp_pre_step2 .
```

以下のコマンドで8000番ポートでアクセスできるようになります。 `-p 8000:8000` の部分を変えるとポートを変更できます。

```sh
docker run -it -d -p 8000:8000 --name seccamp_pre_step2 seccamp_pre_step2
```

### Step3: Dockerfileを書いてみよう

次はPythonが動くDockerfileを作ってみましょう

まずは手始めにdebianを動かしてみます。

```Dockerfile
FROM debian:10

CMD ["/bin/bash"]
```

以下のコマンドでshellが立ち上がるので、遊んでみてください。

```sh
docker run -it --rm --name seccamp_pre_step3 seccamp_pre_step3
```

では、Pythonで同じようにサーバーを立ててみましょう。せっかくなので次は暗号の講義らしいコードを動かしてみましょう。お手軽CBC Padding Oracleですね。もし興味があればフラグを獲得してみてください。

docker上に `vim` を入れてもいいですし、 `docker cp` コマンドで転送しても良いでしょう。
このとき手順書に「ファイルをサーバー上に置いた」という作業もメモしておきましょう。

```python
import os
import http.server as s
from urllib.parse import urlparse
from urllib.parse import parse_qs

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

import base64 
FLAG = b'kurenaifCTF{CBC_PADDING_ORACLE}'
# key = get_random_bytes(16)
key = b'\x07\xf4\xc7/\x0f\x14_\xad\x0f\xa5\xb3\x8d\x01.\xca\x9b'

class MyHandler(s.BaseHTTPRequestHandler):
    def do_GET(self):

        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        flag_cipher = cipher.encrypt(pad(FLAG, AES.block_size))
        body = b'cipher = ' + base64.urlsafe_b64encode(flag_cipher)
        print(base64.urlsafe_b64encode(flag_cipher))

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if 'c' in params:
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            req_cipher = params['c'][0].encode('utf-8')
            
            req_cipher += b'=' * (-len(req_cipher) % 4)
            m = cipher.decrypt(base64.urlsafe_b64decode(req_cipher))
            try:
                unpad(m, AES.block_size)
                body = b'ok'
            except:
                body = b'error'

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)

host = '0.0.0.0'
port = 8000
httpd = s.HTTPServer((host, port), MyHandler)
httpd.serve_forever()
```

動かすためにどんなコマンドが必要でしょうか？ `apt update` を忘れないように気をつけましょう。今手順書は以下のようになっているかなと思います。

```sh
# サーバー上にsource.pyを置く
apt update
apt install python3 python3-pip
pip3 install pycryptodome
python3 source.py
```

これを `Dockerfile` に落とし込むとこんな感じになります。

```Dockerfile
FROM debian:10

# これは悪い例です！でも一度動かしてみてください！

WORKDIR /
COPY source.py  /source.py

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install pycryptodome

CMD ["python3", 'source.py']
```

そして以下でサーバーを起動することができます。

```sh
docker build -t seccamp_pre_step3 .
docker run -it --rm -p 8000:8000 --name seccamp_pre_step3 seccamp_pre_step3
```

そして

```
curl localhost:8000
```

をすると、サーバーが動くはずです。

とりあえず動く `Dockerfile` としては大丈夫です。次はもう少し良くしましょう。

### Step4: Dockerのキャッシュを意識しよう

先程書いたDockerfileの何が行けないのでしょうか？
それはソースコードを変えるとわかります。

一度ソースコードを変えて(コメント追加など非本質の変更で大丈夫です。)、ふたたび

```
docker build -t seccamp_pre_step3 .
```

をしてみましょう。
再び `apt update` などが走ってしまい 不快です。
では、以下のようなDockerfileでビルド→ソースコードを変えてビルドと二回やってみましょう。

```Dockerfile
FROM debian:10

WORKDIR /

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install pycryptodome

COPY source.py  /source.py

CMD ["python3", 'source.py']
```

次は `apt update` などが走らなかったのではないでしょうか？ このようにDockerは、Dockerfileを上から順番に実行し変更がなければキャッシュしたものを使うような仕組みになっています。なので、

* 上に書くもの: 後続のコマンドに必要なもの、あまり変わらないもの
* 下に書くもの: 変化が大きいもの

といったようDockerfileを書き上げるといい感じです。なかなか上に書くか下に書くか悩ましいものがあり、難しいです。

### Step5: docker-composeを使ってDocker間で通信しよう

今回の講義ではもしかすると複数コンテナを使うことになるかもしれません。そうなった場合[docker-compose](https://docs.docker.jp/compose/toc.html) が便利です。
インストール方法は各々ググってもらうとして、 `docker-compose.yml` に以下のようなファイルを書くと clientは 'http://server:8000' で先程のように通信できるようになります。

```
version: '3'
services:
    server: 
        build: ./server
    client:
        build: ./client
```

実際にどのようになっているかはstep5のディレクトリ構成を見てみてください。

以下のコマンドで２つのコンテナを立ち上げることができます。

```
docker-compose up --build
```

`docker ps` コマンドで コンテナのIDを確認します。

```sh
$ docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED              STATUS                          PORTS     NAMES
clientのID   step5_client      "sleep infinity"         4 seconds ago        Up 3 seconds                              step5_client_1
serverのID   step5_server      "/usr/bin/python3 so…"   37 seconds ago       Up 3 seconds                              step5_server_1
```

そして `docker exec` でコンテナの中に入ります。

```
docker exec -it clientのID /bin/bash
```

その中で

```
curl server:8000
```

とすると先程のレスポンスが帰ってくるはずです。
これでクライアントサイドもコンテナに閉じ込めることができました。

わかってほしいコマンドはこんな感じです。Dockerの機能の一部しか紹介できていないので、もし興味があれば続きは公式ドキュメントを読んでみてください。

### 卒業試験(任意, POODLEする人はぜひ)

古いOpenSSLのサーバーを立ち上げてください。バージョンは `1.0.2k` で、最終的に発行したいコマンドが以下になります。
オレオレ証明書の発行の必要がありますが、ローカルで生成して COPYするか、Docker内で生成するかはおまかせします。
なにか困ったことがあったり、辛くなったりした場合はお気軽にご連絡ください。

```sh
openssl s_server -debug -msg -accept ポート番号 -cert 証明書.crt -key 秘密鍵.key
```
