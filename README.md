# バドミントン大会サーチサイト

全国のバドミントン大会情報を検索・管理できるWebアプリケーションです。

## 🏆 機能概要

### ユーザー向け機能
- **大会検索**: キーワード、地域、レベル、開催日で絞り込み検索
- **大会詳細**: 開催日時、会場、参加費、種目等の詳細情報表示
- **お気に入り**: 気になる大会をブックマーク
- **カレンダー表示**: 月間の大会スケジュール表示

### 主催者向け機能
- **大会登録**: 詳細な大会情報の登録・編集・削除
- **主催者認証**: 運営者による身元確認システム
- **大会管理**: 作成した大会の一覧・管理機能

### 運営者向け機能
- **データ管理**: 大会情報の承認・管理
- **ユーザー管理**: 主催者の認証・管理
- **自動収集**: 法的リスクを軽減した公的機関からのデータ収集

## 🛠 技術スタック

- **Backend**: Python 3.12 + Django 4.2
- **Frontend**: Bootstrap 5 + JavaScript
- **Database**: SQLite (開発) / PostgreSQL (本番)
- **UI Framework**: Django Templates + Crispy Forms
- **スタイリング**: Bootstrap 5 + カスタムCSS

## 📋 セットアップ

### 前提条件
- Python 3.8以上
- pip
- Git

### インストール

1. **リポジトリのクローン**
```bash
git clone https://github.com/ume-tora/badminton-tournament-searcher-2.git
cd badminton-tournament-searcher-2
```

2. **仮想環境の作成と有効化**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

4. **環境変数の設定**
```bash
cp .env.example .env
# .envファイルを編集して適切な値を設定
```

5. **データベースのセットアップ**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **開発サーバーの起動**
```bash
python manage.py runserver
```

7. **ブラウザでアクセス**
```
http://127.0.0.1:8000/
```

## 🏗 プロジェクト構造

```
badminton_site/
├── manage.py                 # Django管理コマンド
├── requirements.txt          # 依存関係
├── .env.example             # 環境変数テンプレート
├── badminton_site/          # プロジェクト設定
│   ├── settings.py          # Django設定
│   ├── urls.py              # メインURL設定
│   └── wsgi.py              # WSGIアプリケーション
├── accounts/                # ユーザー管理アプリ
│   ├── models.py            # カスタムUserモデル
│   ├── views.py             # 認証・プロフィール管理
│   ├── forms.py             # ユーザー登録フォーム
│   └── urls.py              # 認証関連URL
├── tournaments/             # 大会管理アプリ
│   ├── models.py            # 大会・お気に入りモデル
│   ├── views.py             # 大会CRUD・検索
│   ├── forms.py             # 大会登録・検索フォーム
│   └── urls.py              # 大会関連URL
├── scraping/                # データ収集アプリ
│   └── management/commands/ # 管理コマンド
│       └── scrape_tournaments.py
├── templates/               # HTMLテンプレート
│   ├── base.html            # ベーステンプレート
│   ├── accounts/            # 認証関連テンプレート
│   └── tournaments/         # 大会関連テンプレート
└── static/                  # 静的ファイル
    ├── css/style.css        # カスタムCSS
    └── js/main.js           # JavaScript
```

## 🔐 セキュリティ

- **認証**: Django標準の認証システム
- **CSRF保護**: 全フォームでCSRFトークン使用
- **XSS対策**: テンプレートでの自動エスケープ
- **SQLインジェクション対策**: DjangoORMの使用
- **パスワードハッシュ化**: Django標準のハッシュ化
- **HTTPS**: 本番環境での強制HTTPS化

## ⚖️ 法的配慮

- **著作権配慮**: 公的機関の公開情報のみを対象
- **個人情報保護**: 個人情報の適切な管理と保護
- **robots.txt遵守**: スクレイピング時のルール遵守
- **利用規約**: サイト利用に関する明確な規約

## 🚀 デプロイ

### Render (推奨)
1. Renderアカウント作成
2. GitHubリポジトリ連携
3. 環境変数設定
4. 自動デプロイ

### Heroku
1. Herokuアカウント作成
2. Heroku CLIインストール
3. アプリケーション作成・デプロイ

## 📝 開発ガイド

### 管理コマンド
```bash
# データベースマイグレーション
python manage.py makemigrations
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser

# 静的ファイル収集
python manage.py collectstatic

# 大会情報自動収集（法的リスク軽減型）
python manage.py scrape_tournaments --dry-run
```

### テスト実行
```bash
python manage.py test
```

## 🤝 コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 📞 サポート

- 🐛 バグレポート: [Issues](https://github.com/ume-tora/badminton-tournament-searcher-2/issues)
- 💡 機能リクエスト: [Issues](https://github.com/ume-tora/badminton-tournament-searcher-2/issues)
- 📧 その他のお問い合わせ: [Contact](mailto:your-email@example.com)

## 🙏 謝辞

- 全国のバドミントン協会の皆様
- オープンソースコミュニティ
- Django開発チーム
- Bootstrap開発チーム

---

**🏸 バドミントン愛好者の皆様が素晴らしい大会と出会えることを願っています！**