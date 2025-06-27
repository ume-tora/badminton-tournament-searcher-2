from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MinValueValidator
from datetime import date

User = get_user_model()


class Tournament(models.Model):
    """大会情報モデル"""
    
    # イベント種目の選択肢
    EVENT_CHOICES = [
        ('MS', '男子シングルス'),
        ('WS', '女子シングルス'),
        ('MD', '男子ダブルス'),
        ('WD', '女子ダブルス'),
        ('XD', 'ミックスダブルス'),
    ]
    
    # 大会レベルの選択肢
    LEVEL_CHOICES = [
        ('beginner', '初心者'),
        ('intermediate', '中級者'),
        ('advanced', '上級者'),
        ('open', 'オープン'),
    ]
    
    # 基本情報
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_tournaments',
        verbose_name='主催者'
    )
    
    name = models.CharField(
        max_length=200,
        verbose_name='大会名'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='大会概要'
    )
    
    # 日時・場所情報
    event_date = models.DateField(
        verbose_name='開催日'
    )
    
    event_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name='開始時間'
    )
    
    deadline_date = models.DateField(
        verbose_name='申込締切日'
    )
    
    venue_name = models.CharField(
        max_length=200,
        verbose_name='会場名'
    )
    
    venue_address = models.CharField(
        max_length=300,
        verbose_name='会場住所'
    )
    
    prefecture = models.CharField(
        max_length=20,
        verbose_name='都道府県',
        db_index=True  # 検索用インデックス
    )
    
    # 大会詳細
    event_details_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='大会要項URL'
    )
    
    fee = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='参加費',
        help_text='円'
    )
    
    max_participants = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='定員',
        help_text='人'
    )
    
    events = models.CharField(
        max_length=500,
        verbose_name='開催種目',
        help_text='例: 男子シングルス, 女子ダブルス'
    )
    
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='open',
        verbose_name='大会レベル',
        db_index=True  # 検索用インデックス
    )
    
    # 連絡先情報
    contact_name = models.CharField(
        max_length=100,
        verbose_name='連絡先担当者'
    )
    
    contact_email = models.EmailField(
        verbose_name='連絡先メールアドレス'
    )
    
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='連絡先電話番号'
    )
    
    # 管理用フィールド
    is_scraped = models.BooleanField(
        default=False,
        verbose_name='自動収集データ',
        help_text='スクレイピングで自動収集されたデータかどうか'
    )
    
    is_approved = models.BooleanField(
        default=True,
        verbose_name='承認済み',
        help_text='運営者によって承認されたかどうか'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='アクティブ'
    )
    
    # 日時情報
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='登録日時',
        db_index=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新日時'
    )
    
    class Meta:
        verbose_name = '大会'
        verbose_name_plural = '大会'
        db_table = 'tournaments_tournament'
        ordering = ['event_date', 'created_at']
        indexes = [
            models.Index(fields=['event_date']),
            models.Index(fields=['prefecture']),
            models.Index(fields=['level']),
            models.Index(fields=['is_approved', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.event_date})"
    
    def get_absolute_url(self):
        return reverse('tournaments:tournament_detail', kwargs={'pk': self.pk})
    
    def is_registration_open(self):
        """申込受付中かどうかを判定"""
        return date.today() <= self.deadline_date
    
    def is_upcoming(self):
        """開催予定かどうかを判定"""
        return date.today() <= self.event_date
    
    def days_until_deadline(self):
        """申込締切まての日数を取得"""
        if self.is_registration_open():
            return (self.deadline_date - date.today()).days
        return 0
    
    def days_until_event(self):
        """開催日までの日数を取得"""
        if self.is_upcoming():
            return (self.event_date - date.today()).days
        return 0
    
    def get_events_list(self):
        """開催種目をリストで取得"""
        return [event.strip() for event in self.events.split(',') if event.strip()]
    
    def can_edit(self, user):
        """編集権限があるかどうかを判定"""
        return user == self.organizer or user.is_staff
    
    def can_delete(self, user):
        """削除権限があるかどうかを判定"""
        return user == self.organizer or user.is_staff


class Favorite(models.Model):
    """お気に入り大会モデル"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='ユーザー'
    )
    
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='大会'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='お気に入り登録日'
    )
    
    class Meta:
        verbose_name = 'お気に入り'
        verbose_name_plural = 'お気に入り'
        db_table = 'tournaments_favorite'
        unique_together = ('user', 'tournament')  # 同じユーザーが同じ大会を重複してお気に入りできない
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tournament.name}"


class TournamentImage(models.Model):
    """大会画像モデル（将来の拡張用）"""
    
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='大会'
    )
    
    image = models.ImageField(
        upload_to='tournament_images/',
        verbose_name='画像'
    )
    
    caption = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='キャプション'
    )
    
    is_main = models.BooleanField(
        default=False,
        verbose_name='メイン画像'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='登録日時'
    )
    
    class Meta:
        verbose_name = '大会画像'
        verbose_name_plural = '大会画像'
        db_table = 'tournaments_tournamentimage'
        ordering = ['-is_main', '-created_at']
    
    def __str__(self):
        return f"{self.tournament.name} - {self.caption or '画像'}"