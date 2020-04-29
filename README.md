# born2remote-thon🐟

## サービス概要
42のあの教室を模したWebサイト

## 目的
* オフラインのメリットをリモートでも実現したい
  * リモートでは実現しづらい"peer on the right/left"のいる環境を
    * ”隣の人に聞く”を可能にする
    * 課題には直接関係のない有益な情報共有
    * 話したことがない人との会話

* オンラインであることを強みにしたい
  * 他の人のコードを見ることで学びを共有する
  * 自分のコードを公開することでより良いコードを目指せる
  * 気軽に質問できる環境を作ることで問題解決のスピードを短縮

## 課題


## 仕様
Webサイトの３つの機能
1. クラスター (42の教室のような部屋）
2. 力作コード館 （自分の書いた珠玉のコードを紹介できる場所）
3. 気軽な質問箱　(課題について気軽に質問を投稿できる場所）
----------

1. クラスター
  - クラスター
    - 席をクリックすることで着席する
    - 隣の席の人をクリックすることでその人とのリアルタイムチャットに移行
    - 通話の選択も可能（Discordの新規公開ボイスチャンネルに移遷）
    - クラスターにいる人の課題の進捗（レベル）が確認できる

  - 雑談スペース
    - 席をクリックすることで着席する
    - Discordの新規公開ボイスチャンネルに移遷し通話開始

2. 力作コード館
  * 自分の自慢のコードを展示する
  * 課題に関するコードはその課題を完全クリアした人のみが閲覧可
  * 提出期限が過ぎた課題や再提出が不可能な課題に関しては挑戦した課題のみ閲覧できる

3. 気軽な質問箱
  * 掲示板のような、気軽に質問のできる機能
  * 課題ごとにまとまっている


## 言語・フレームワーク

* Python

## プロトタイプ
[Figma](https://www.figma.com/file/DTt1wiHu2qGHKMjCDVmINYKx/thon)

## 役割分担
29(水)12:00までを目安に  
- Web構成：rfukuda、ydoi
- 42API：mfunyu、tkawahar
- DiscordAPIとその他：ksuzuki、yyabumot

## Flask API
1, 作業フォルダ作成
```
$ git clone https://github.com/42Tokyo/born2remote-thon.git
$ cd born2remote-thon
```

2, セットアップ
```
$ cp .env-sample .env
```
.envファイルを各自の環境に合わせて編集


```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

3, MySQL セットアップ
```
$ deactivate
$ mysql -u root -p
```
パスワードを入力

```
mysql> CREATE DATABASE [任意のデータベース名];
mysql> exit
```

```
$ mysql -u root [作ったデータベース名] -p < 42hackathon.sql;
```
パスワードを入力

4, 起動
```
仮想環境に入り、
$ python3 app.py
```
http://127.0.0.1:5000/api/codeworks でテストデータを確認
