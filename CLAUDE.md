# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a badminton tournament search website that aggregates tournament information across Japan. The platform serves three user types:
- **General users**: Search and favorite tournaments
- **Organizers**: Create and manage tournament listings
- **Admins**: Manage scraped data and site operations

## Technology Stack

- **Backend**: Python/Django
- **Frontend**: Django Templates + Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)
- **Web Scraping**: Beautiful Soup/Scrapy
- **Deployment**: Render or Heroku

## Development Commands

Since the project uses Django, these are the expected development commands once implemented:

```bash
# Environment setup
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Database operations
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser

# Development server
python manage.py runserver

# Testing
python manage.py test

# Scraping (custom management command)
python manage.py scrape_tournaments
```

## Application Architecture

The Django project follows a modular app structure:

### Core Apps
- **badminton_site/**: Main project settings and URL configuration
- **tournaments/**: Tournament data models, views, and templates
- **accounts/**: User authentication for all user types (general, organizer, admin)
- **scraping/**: Web scraping functionality with management commands

### Key Models
- **User**: Extended with `user_type` field ('general', 'organizer', 'admin')
- **Tournament**: Core tournament data with organizer relationship
- **Favorite**: Many-to-many relationship between users and tournaments

### Directory Structure
```
badminton_site/
├── manage.py
├── requirements.txt
├── badminton_site/          # Project settings
├── tournaments/             # Tournament functionality
├── accounts/                # User management
├── scraping/                # Web scraping
│   └── management/commands/
│       └── scrape_tournaments.py
├── static/                  # CSS, JS, images
└── templates/               # HTML templates
    ├── base.html
    ├── tournaments/
    └── accounts/
```

## Key Features to Implement

1. **Search & Filtering**: By keyword, region, date, event type
2. **User Authentication**: Role-based access (general/organizer/admin)
3. **Tournament CRUD**: Full management for organizers
4. **Favorites System**: Bookmark tournaments with deadline reminders
5. **Web Scraping**: Automated data collection from external sources
6. **Responsive Design**: Mobile-first Bootstrap implementation

## Development Notes

- Use Django's built-in admin for initial data management
- Implement custom User model extending AbstractUser for user_type field
- Web scraping should be implemented as Django management commands for scheduled execution
- Follow Django best practices for URL routing, template inheritance, and static file management
- Ensure responsive design using Bootstrap framework

## Gemini CLI 連携ガイド

### 目的
ユーザーが **「Geminiと相談しながら進めて」** （または同義語）と指示した場合、Claude は以降のタスクを **Gemini CLI** と協調しながら進める。
Gemini から得た回答はそのまま提示し、Claude 自身の解説・統合も付け加えることで、両エージェントの知見を融合する。

---

### トリガー
- 正規表現: `/Gemini.*相談しながら/`
- 例:
- 「Geminiと相談しながら進めて」
- 「この件、Geminiと話しつつやりましょう」

---

### 基本フロー
1. **PROMPT 生成**
Claude はユーザーの要件を 1 つのテキストにまとめ、環境変数 `$PROMPT` に格納する。

2. **Gemini CLI 呼び出し**
```bash
gemini <<EOF
$PROMPT
EOF
```