# セキュリティキャンプ L-IVゼミ事前課題

## 応募課題に1問以上チャレンジしよう (全員)

https://www.ipa.go.jp/files/000090352.txt

## Dockerに慣れよう (全員)

慣れている人は大丈夫です。
`docker_training` のディレクトリを見てみてください。

## Pythonに慣れよう (全員)

Pythonに入門しておいてください。
CTFの簡単なCrypto問が解ける程度で十分です。
CryptoHack等で数問解いてみてください。

## POODLE Attackを知ろう (POODLEやる人)
```
Q1. POODLE Attackの攻撃方法を予め勉強しておいてください。
手を動かすと理解できる系の攻撃手法です。
`poodle` ディレクトリにサーバー用のファイルをおいておいたので、こちらで練習してください。

POODLEを知らない場合はできれば調べずに解いてみてください。解けたら気持ちいです。

Q2. Dockerの練習問題のOpenSSL環境構築に挑戦してみてください
```

キャンプ当日はこの処理を実際にSSLの通信に載せて攻撃を行います。
また、OpenSSLの膨大なソースコードのうち、どこにあってそれがどう修正されたのかを探しつつ、ソースコードレベルで最近の暗号化手法はどう変わっていっているのかを勉強する予定です。膨大な仕様やソースコードリーディング能力、デバッグ能力などが問われる根気のいる回になると思います。

かなり古いバージョンの脆弱性になりますが、CBCが危険だと言われる理由が垣間見える脆弱性で、今の暗号技術のトレンドを追いかける上で無視できないものだと思い取り上げました。一緒にがんばりましょう。

## 乱数予測を深ぼろう (乱数予測をやる人)

```
Q1. 「Mersenne Twister 予測」などで調べて、メルセンヌ・ツイスタの値を624個取得し予測する手法を勉強してください。
Q2. C言語のコードにある程度慣れておいてください。具体的には、phpのメルセンヌ・ツイスタのコードが目で追えると嬉しいです。
Q3. https://github.com/ambionics/mt_rand-reverse こちらのコードを実際に動かし、乱数の予測を試みてください。その際にoffsetの値をずらしながら検証し、復元に失敗するケースを探してみてください。
Q4. Q1がなぜ復元に失敗するのか考えてみてください。
Q5. https://github.com/kurenaif/kurenaif_valentine_problems/tree/main/three_values_twister これのフラグを取得してください
```

キャンプ当日は本来SecureRandomを利用するところを誤ってセキュアではないRandomを使ってしまった場合、実世界で本当に予測できるのか？にスコープを当てて様々な言語、フレームワークの乱数生成法、攻撃方法を調べる予定です。世の中にある攻撃手法を応用する力、現実的なユースケースを予想する力などが問われます。

自分自身動画にする上で、「現実世界ではどのような実装になっているのか？」ということに焦点をあてて各言語の実装を見に行ったりするのですが、言語ごとに実装に差があってとても面白いです。もしかすると横断で見ているとバグが見つかるかもしれないので、その時はコントリビュートしましょう！
