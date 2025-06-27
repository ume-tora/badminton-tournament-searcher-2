# バドミントン大会サーチサイト

## 1. 概要
このプロジェクトは、日本の全国のバドミントン大会情報を集約し、プレイヤーや主催者のための情報プラットフォームを提供するWebアプリケーションです。プレイヤーは自分に合った大会を簡単に検索でき、主催者は大会情報を広く告知することができます。

## 2. 機能一覧
### ユーザー（選手・愛好家）向け機能
- アカウント登録、ログイン機能
- 大会情報のキーワード、地域、日付、種目による検索・絞り込み機能
- 大会詳細情報の閲覧
- 気になる大会のお気に入り登録機能
- 申込締切のリマインダー機能

### 大会主催者向け機能
- 主催者用アカウント登録、ログイン機能
- 大会情報の登録、編集、削除（CRUD）機能

### サイト運営者向け機能
- 外部サイトからの大会情報の自動収集（スクレイピング）機能
- 収集したデータの管理・承認機能

## 3. 技術スタック
- **バックエンド**: Python / Django
- **フロントエンド**: Django Template / Bootstrap
- **データベース**: PostgreSQL (本番) / SQLite (開発)
- **スクレイピング**: Beautiful Soup / Scrapy
- **インフラ**: Render / Heroku

## 4. 環境構築手順
1.  **リポジトリのクローン**
    ```bash
    git clone [https://github.com/your_username/badminton_site.git](https://github.com/your_username/badminton_site.git)
    cd badminton_site
    ```

2.  **仮想環境の作成と有効化**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **必要なライブラリのインストール**
    ```bash
    pip install -r requirements.txt
    ```

4.  **環境変数ファイルの設定**
    - `.env.example` をコピーして `.env` ファイルを作成し、データベースの接続情報などを記述します。

5.  **データベースのマイグレーション**
    - データベースにテーブルを作成します。
    ```bash
    python manage.py migrate
    ```

6.  **開発用サーバーの起動**
    ```bash
    python manage.py runserver
    ```
    - サーバーが起動したら、ブラウザで `http://127.0.0.1:8000/` にアクセスしてください。