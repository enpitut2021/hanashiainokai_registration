# シケタイ: Webハブ
シケタイの入り口ページ。Discordサーバーに参加したり、カレンダーから勉強会の登録／参加を行えます

## ローカル環境での実行の仕方
1. `pip install django`
2. `python manage.py runserver`
3. webブラウザで「http://localhost:8000/app/login 」でログイン画面に遷移

## heroku環境へのdeployの仕方

`main`ブランチの実装が常にlocal環境でもheroku本番環境でも動く状態を保つために以下のような手順を踏む

1. `sub1,…`など別のブランチで新しく追加したい機能を実装する
2. localhostで動くことを確認する
3. PRを作成し`main`ブランチにマージさせる.
4. この時点で https://hanashiainokairegistration.herokuapp.com/login に自動的にdeployされる。
5. heroku本番環境で問題が発生した場合は https://dashboard.heroku.com/apps/hanashiainokairegistration/activity からビルドログを読んで解決する。

