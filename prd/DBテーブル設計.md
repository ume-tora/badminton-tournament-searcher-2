# DBテーブル設計

## 1. 設計概要
- ユーザー、大会、お気に入りの情報を管理するために、以下のテーブルを設計する。
- 各テーブルは、互いに関連付けられる（例：どのユーザーがどの大会を登録したか）。

## 2. テーブル定義

### 2.1. ユーザーテーブル (accounts_user)
- サイトを利用するユーザー（一般利用者、大会主催者、運営者）の情報を保存します。

| カラム名 (項目名)   | データ型     | 説明                                     |
| ----------------- | ---------- | ---------------------------------------- |
| `id` (主キー)       | `BigAutoField` | ユーザーを識別するためのユニークな番号 (自動で割り振られる) |
| `username`        | `CharField`  | ユーザー名                               |
| `email`           | `EmailField` | メールアドレス (ログイン時に使用)          |
| `password`        | `CharField`  | ハッシュ化（暗号化）されたパスワード       |
| `user_type`       | `CharField`  | ユーザー種別 ( 'general', 'organizer', 'admin' ) |
| `date_joined`     | `DateTimeField`| 登録日時                                 |
| `last_login`      | `DateTimeField`| 最終ログイン日時                         |

### 2.2. 大会テーブル (tournaments_tournament)
- 登録された大会の詳細情報を保存します。

| カラム名 (項目名)           | データ型        | 説明                                                     |
| ------------------------- | --------------- | -------------------------------------------------------- |
| `id` (主キー)               | `BigAutoField`    | 大会を識別するためのユニークな番号 (自動で割り振られる)      |
| `organizer` (外部キー)      | `ForeignKey`    | この大会を登録した主催者ユーザーのID (`ユーザーテーブル`と紐づく) |
| `name`                    | `CharField`     | 大会名                                                   |
| `event_date`              | `DateField`     | 開催日                                                   |
| `deadline_date`           | `DateField`     | 申込締切日                                               |
| `venue_name`              | `CharField`     | 開催場所・会場名                                         |
| `venue_address`           | `CharField`     | 会場の住所                                               |
| `event_details_url`       | `URLField`      | 大会要項や公式サイトのURL                                  |
| `fee`                     | `IntegerField`  | 参加費                                                   |
| `events`                  | `CharField`     | 開催種目（例: "男子シングルス, 女子ダブルス"）             |
| `is_scraped`              | `BooleanField`  | 運営者が自動収集した情報かどうかのフラグ (True/False)    |
| `created_at`              | `DateTimeField` | この情報が登録された日時                                 |
| `updated_at`              | `DateTimeField` | この情報が更新された日時                                 |

### 2.3. お気に入りテーブル (tournaments_favorite)
- どのユーザーが、どの大会をお気に入りに登録したかの関係性を保存します。

| カラム名 (項目名)     | データ型       | 説明                                               |
| ----------------- | -------------- | -------------------------------------------------- |
| `id` (主キー)       | `BigAutoField`   | お気に入り登録を識別するための番号 (自動で割り振られる)  |
| `user` (外部キー)   | `ForeignKey`   | お気に入り登録したユーザーのID (`ユーザーテーブル`と紐づく) |
| `tournament`(外部キー)| `ForeignKey`   | お気に入り登録された大会のID (`大会テーブル`と紐づく)   |
| `created_at`      | `DateTimeField`| お気に入りに登録された日時                         |