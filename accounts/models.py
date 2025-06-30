from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    カスタムユーザーモデル
    3つのユーザータイプ（一般ユーザー、主催者、管理者）をサポート
    """
    
    USER_TYPE_CHOICES = [
        ('general', '一般ユーザー'),
        ('organizer', '大会主催者'),
        ('admin', '管理者'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='general',
        verbose_name='ユーザータイプ'
    )
    
    # 主催者の認証状態
    is_verified_organizer = models.BooleanField(
        default=False,
        verbose_name='主催者認証済み',
        help_text='運営者によって身元確認が完了した主催者かどうか'
    )
    
    # プロフィール情報
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='電話番号'
    )
    
    prefecture = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='都道府県'
    )
    
    # 主催者用追加情報
    organization_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='団体名',
        help_text='主催者の場合の団体名'
    )
    
    organization_website = models.URLField(
        blank=True,
        null=True,
        verbose_name='団体ウェブサイト'
    )
    
    # 法的同意記録
    privacy_policy_agreed = models.BooleanField(
        default=False,
        verbose_name='プライバシーポリシー同意',
        help_text='個人情報保護法に基づく同意記録'
    )
    
    privacy_policy_agreed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='プライバシーポリシー同意日時'
    )
    
    terms_agreed = models.BooleanField(
        default=False,
        verbose_name='利用規約同意',
        help_text='サービス利用規約への同意記録'
    )
    
    terms_agreed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='利用規約同意日時'
    )
    
    # データ削除要求記録
    data_deletion_requested = models.BooleanField(
        default=False,
        verbose_name='データ削除要求',
        help_text='GDPR対応：忘れられる権利の行使記録'
    )
    
    data_deletion_requested_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='データ削除要求日時'
    )

    # 管理用
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='登録日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
        db_table = 'accounts_user'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_organizer(self):
        """主催者かどうかを判定"""
        return self.user_type == 'organizer'
    
    def is_verified(self):
        """認証済み主催者かどうかを判定"""
        return self.is_organizer() and self.is_verified_organizer
    
    def can_create_tournament(self):
        """大会を作成できるかどうかを判定"""
        return self.is_verified()
    
    def get_display_name(self):
        """表示用の名前を取得"""
        if self.organization_name and self.is_organizer():
            return self.organization_name
        return self.username
    
    def has_valid_consent(self):
        """有効な同意があるかどうかを判定"""
        return self.privacy_policy_agreed and self.terms_agreed
    
    def request_data_deletion(self):
        """データ削除要求を記録（GDPR対応）"""
        from django.utils import timezone
        self.data_deletion_requested = True
        self.data_deletion_requested_at = timezone.now()
        self.save()