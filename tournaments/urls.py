from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    # 大会一覧・検索
    path('', views.TournamentListView.as_view(), name='tournament_list'),
    path('search/', views.TournamentSearchView.as_view(), name='tournament_search'),
    
    # 大会詳細
    path('tournament/<int:pk>/', views.TournamentDetailView.as_view(), name='tournament_detail'),
    
    # お気に入り機能
    path('tournament/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
    
    # 主催者向け機能
    path('create/', views.TournamentCreateView.as_view(), name='tournament_create'),
    path('tournament/<int:pk>/edit/', views.TournamentUpdateView.as_view(), name='tournament_edit'),
    path('tournament/<int:pk>/delete/', views.TournamentDeleteView.as_view(), name='tournament_delete'),
    path('my-tournaments/', views.OrganizerTournamentListView.as_view(), name='organizer_tournaments'),
    
    # カレンダー表示
    path('calendar/', views.TournamentCalendarView.as_view(), name='tournament_calendar'),
    
    # API エンドポイント（将来の拡張用）
    path('api/tournaments/', views.TournamentApiView.as_view(), name='tournament_api'),
]