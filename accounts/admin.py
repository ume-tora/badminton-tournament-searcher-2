from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """カスタムユーザーモデル用の管理画面設定"""
    
    list_display = [
        'username', 'email', 'user_type', 'is_verified_organizer', 
        'organization_name', 'is_active', 'date_joined'
    ]
    
    list_filter = [
        'user_type', 'is_verified_organizer', 'is_active', 
        'is_staff', 'prefecture', 'date_joined'
    ]
    
    search_fields = ['username', 'email', 'organization_name', 'first_name', 'last_name']
    
    ordering = ['-date_joined']
    
    # フィールドセットの設定
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('追加情報'), {
            'fields': (
                'user_type', 'is_verified_organizer', 'phone_number', 
                'prefecture', 'organization_name', 'organization_website'
            )
        }),
        (_('日時情報'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # 新規作成時のフィールド
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('追加情報'), {
            'fields': ('user_type', 'email', 'phone_number', 'prefecture')
        }),
    )
    
    # 読み取り専用フィールド
    readonly_fields = ['created_at', 'updated_at']
    
    # 主催者認証のアクション
    actions = ['approve_organizers', 'unapprove_organizers']
    
    def approve_organizers(self, request, queryset):
        """選択した主催者を認証済みにする"""
        organizers = queryset.filter(user_type='organizer')
        updated = organizers.update(is_verified_organizer=True)
        self.message_user(
            request,
            f'{updated}人の主催者を認証済みにしました。'
        )
    approve_organizers.short_description = '選択した主催者を認証済みにする'
    
    def unapprove_organizers(self, request, queryset):
        """選択した主催者の認証を取り消す"""
        organizers = queryset.filter(user_type='organizer')
        updated = organizers.update(is_verified_organizer=False)
        self.message_user(
            request,
            f'{updated}人の主催者の認証を取り消しました。'
        )
    unapprove_organizers.short_description = '選択した主催者の認証を取り消す'