# wiki データのdump

wikiは最新のdumpを専用ダウンロードサイトに保存しているので、スクレイピングせずにこちらをダウンロードして使う。ただし、本文記事はxml圧縮ファイルのため、専用のpython parserを使って、解凍・テキストファイル変換を行う。以下その手順

（これらの環境は C:\Users\uhoku\wiki_dataに保存した）

1. wiki dumpのダウンロード
   
   [Index of /jawiki/latest/](https://dumps.wikimedia.org/jawiki/latest/)から、jawiki-latest-pages-articles.xml.bz2をダウンロードして、適当にフォルダーへコピー（解凍せず圧縮ファイルのままコピーする）

2. venvの設定
   
   上記ファイルをテキスト変換するためのpython ライブラリwikiextractorを実行するには、python3.1. でないと[エラーになる](https://teratail.com/questions/tmwejvhsc77w9d)。そのため、venvでバージョンの異なるpython環境を作り、wikiextractorをインストールする。以下は、venvの作り方
   
   1) バージョンを特定してpythonをインストール
      
      [pyhtonダウンロードサイト](https://pythonlinks.python.jp/ja/index.html)から特定のバージョンをダウンロードしてexeを実行ここではpython-3.10.5-amd64.exeを使った。3.10ならば問題ない模様。なお、インストーラーの途中でパスを自動登録するチェックボタンが現れるがこれは押さない！　押すと、anacondaよりもこのpythonが優先される。
   
   2) venvの作成
      
      適当なディレクトリに移動して、pythonのバージョン指定でvenvを作る。ディレクトリはどこでもいいが、1.で作成したデータのフォルダー上から作るとまとまっていてわかりやすい。手順は、[こちら](https://qiita.com/unaginokabayaki/items/81d7b2bf8a6bdaee37a9)の3.　venvで仮想環境を作る　に従う。acitivateするとvenv起動状態になり、プロンプトがvenv内をさすようになる。
   
   3) wikiextractor（エラー対応版）インストール
      
      上記のvenv activate状態で、wikiextractorをインストール。ただし、pipでインストールすると、実行途中でエラーになるので、以下の手順でgithubからインストールする。
      
      https://zenn.dev/haru330/articles/503c217c3cda1e
   
   4) wikiextractor でテキストファイルに変換
      
      venvプロンプト上で以下のとおり実行。カレントディレクトリは、jawiki-latest-pages-articles.xml.bz2の上に移す。1時間くらいかかる。詳細は上記3.のリンク
      
      wikiextractor jawiki-latest-pages-articles.xml.bz2.xml
   
   5) テキストファイルをmongodbに保尊
      
      上記のデータをjsonに変換し、mongodbに保存する。プログラムはwiki_scraping.py

3. wiki記事のカテゴリーラベル取得
   
   wiki dumpのなかで、sql形式のカテゴリーラベルデータ、とwebサービスでidとカテゴリーを対応付けるものの2通りがある。sqlのほうは中身を見たところカテゴリーではなかったので、以下2.を使うしかない
   
   1. wiki dumpからのカテゴリーデータ取得
      
      [Wikipediaの特定カテゴリ以下の記事だけを取得する（サブカテゴリの取得） #MySQL - Qiita](https://qiita.com/tekunikaruza_jp/items/93d3267a444acef470d9)
      
      トライしてみたdump データ
      
        jawiki-latest-categorylinks.sql,   jawiki-latest-category.sql
      
      spl形式なので、mySQLをインストールして、上記をrestoreする。utf8でないとエラーになるので、以下のようにrestoreする。
      
      mysql  --user=root --password=root --default-character-set=utf8 jawiki_category2 < jawiki-latest-category.sql
      
      このデータを取り出すと文字化ける。これを補正するには.decode(utf8)を使う。データベースの全文を読みだすサンプルは、wiki_retrieve_sql.py
   
   2. petscan ：カテゴリーを入力すると該当する記事idを表示するwebサービス
      
      [Wikipediaの特定カテゴリの記事のみを取得する - 薬剤師のプログラミング学習日記](https://www.yakupro.info/entry/programming-wikipedia-data)

4. AI事前学習でのバイアス問題
   
   どのようなバイアスが見られるかについての研究をサーベイするのは面白い
   
   [AIにおける留意点　バイアスと限界 #Python - Qiita](https://qiita.com/ka201504/items/729bc1f90c204957312f#3-%E6%A4%9C%E8%A8%BC%EF%BC%91)
   
   https://www.anlp.jp/proceedings/annual_meeting/2023/pdf_dir/A7-3.pdf

5. 東北大学日本語BERT
   
   v1,v2とも日本語wikiでpretrainedしている
   
   [Huggingface Transformers 入門 (34) -東北大学の乾研究室の日本語BERTモデルのv1とv2の比較｜npaka](https://note.com/npaka/n/nbbf6b38f4b46)

6. バイアスを試すプログラミング
   
   一般的なHuggingface Bert による穴埋めタスクなどのコーディングは以下を参照  

[10. Hugging Face の利用方法 &#8212; 実践データ科学](https://yamada-kd.github.io/binds-training/notebook/tensorflow_07.html)

https://jupyterbook.hnishi.com/language-models/fine_tune_jp_bert_part01.html

         pipleine関連

[【huggingface/transformers】Pipelinesの使い方 #Python - Qiita](https://qiita.com/maechanneler/items/a83702d7148be66f4416)

7. 分析の方向性
   
   日本語wikiの分析から、バイアスの原因を探し出す。例えば、単語と単語の共起確率(PMI)

7. 固有表現抽出の学習（参考）

　　[BERTによる日本語固有表現抽出 #bert - Qiita](https://qiita.com/age884/items/7b8d5c583e59e755aaf0)
