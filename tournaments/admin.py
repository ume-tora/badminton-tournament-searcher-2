from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Tournament, Favorite, TournamentImage


class TournamentImageInline(admin.TabularInline):
    """大会画像のインライン編集"""
    model = TournamentImage
    extra = 1
    readonly_fields = ['created_at']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """大会モデルの管理画面設定"""
    
    list_display = [
        'name', 'organizer', 'event_date', 'prefecture', 'level',
        'fee', 'is_approved', 'is_active', 'registration_status', 'created_at'
    ]
    
    list_filter = [
        'is_approved', 'is_active', 'is_scraped', 'level', 'prefecture',
        'event_date', 'created_at'
    ]
    
    search_fields = [
        'name', 'venue_name', 'venue_address', 'organizer__username',
        'organizer__organization_name', 'events'
    ]
    
    readonly_fields = [
        'created_at', 'updated_at', 'registration_status', 'event_status'
    ]
    
    ordering = ['-created_at']
    
    date_hierarchy = 'event_date'
    
    inlines = [TournamentImageInline]
    
    fieldsets = (
        ('基本情報', {
            'fields': ('organizer', 'name', 'description')
        }),
        ('日時・場所', {
            'fields': ('event_date', 'event_time', 'deadline_date', 
                      'venue_name', 'venue_address', 'prefecture')
        }),
        ('大会詳細', {
            'fields': ('events', 'level', 'fee', 'max_participants', 'event_details_url')
        }),
        ('連絡先', {
            'fields': ('contact_name', 'contact_email', 'contact_phone')
        }),
        ('管理', {
            'fields': ('is_scraped', 'is_approved', 'is_active'),
            'classes': ('collapse',)
        }),
        ('ステータス', {
            'fields': ('registration_status', 'event_status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_tournaments', 'deactivate_tournaments', 'activate_tournaments']
    
    def registration_status(self, obj):
        """申込受付状況の表示"""
        if obj.is_registration_open():
            days = obj.days_until_deadline()
            if days == 0:
                return format_html('<span style="color: orange;">本日締切</span>')
            elif days <= 3:
                return format_html('<span style="color: red;">あと{}日</span>', days)
            else:
                return format_html('<span style="color: green;">受付中（あと{}日）</span>', days)
        else:
            return format_html('<span style="color: gray;">締切済み</span>')
    registration_status.short_description = '申込状況'
    
    def event_status(self, obj):
        """開催状況の表示"""
        if obj.is_upcoming():
            days = obj.days_until_event()
            if days == 0:
                return format_html('<span style="color: blue;">本日開催</span>')
            elif days <= 7:
                return format_html('<span style="color: orange;">あと{}日</span>', days)
            else:
                return format_html('<span style="color: green;">開催予定（あと{}日）</span>', days)
        else:
            return format_html('<span style="color: gray;">開催済み</span>')
    event_status.short_description = '開催状況'
    
    def approve_tournaments(self, request, queryset):
        """選択した大会を承認する"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated}件の大会を承認しました。')
    approve_tournaments.short_description = '選択した大会を承認する'
    
    def deactivate_tournaments(self, request, queryset):
        """選択した大会を非アクティブにする"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated}件の大会を非アクティブにしました。')
    deactivate_tournaments.short_description = '選択した大会を非アクティブにする'
    
    def activate_tournaments(self, request, queryset):
        """選択した大会をアクティブにする"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated}件の大会をアクティブにしました。')
    activate_tournaments.short_description = '選択した大会をアクティブにする'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """お気に入りモデルの管理画面設定"""
    
    list_display = ['user', 'tournament', 'tournament_date', 'created_at']
    list_filter = ['created_at', 'tournament__event_date']
    search_fields = [
        'user__username', 'tournament__name', 'user__email'
    ]
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def tournament_date(self, obj):
        """大会開催日の表示"""
        return obj.tournament.event_date
    tournament_date.short_description = '大会開催日'
    tournament_date.admin_order_field = 'tournament__event_date'


@admin.register(TournamentImage)
class TournamentImageAdmin(admin.ModelAdmin):
    """大会画像モデルの管理画面設定"""
    
    list_display = ['tournament', 'caption', 'is_main', 'image_preview', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['tournament__name', 'caption']
    readonly_fields = ['created_at', 'image_preview']
    ordering = ['-created_at']
    
    def image_preview(self, obj):
        """画像プレビューの表示"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "画像なし"
    image_preview.short_description = 'プレビュー'


# Admin サイトのカスタマイズ
admin.site.site_header = 'バドミントン大会サーチサイト 管理画面'
admin.site.site_title = 'バドミントン大会サーチ'
admin.site.index_title = 'サイト管理'