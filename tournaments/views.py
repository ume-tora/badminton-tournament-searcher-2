from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date, timedelta
import json

from .models import Tournament, Favorite, TournamentImage
from .forms import TournamentForm, TournamentSearchForm


class TournamentListView(ListView):
    """大会一覧ビュー"""
    model = Tournament
    template_name = 'tournaments/tournament_list.html'
    context_object_name = 'tournaments'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Tournament.objects.filter(
            is_approved=True,
            is_active=True
        ).select_related('organizer').prefetch_related('favorited_by')
        
        # 検索パラメータの処理
        query = self.request.GET.get('q')
        prefecture = self.request.GET.get('prefecture')
        level = self.request.GET.get('level')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(venue_name__icontains=query) |
                Q(venue_address__icontains=query) |
                Q(events__icontains=query)
            )
        
        if prefecture:
            queryset = queryset.filter(prefecture=prefecture)
        
        if level:
            queryset = queryset.filter(level=level)
        
        if date_from:
            queryset = queryset.filter(event_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(event_date__lte=date_to)
        
        # デフォルトの並び順: 開催日の近い順
        return queryset.order_by('event_date', 'created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TournamentSearchForm(self.request.GET)
        context['title'] = 'バドミントン大会一覧'
        
        # 統計情報
        context['total_tournaments'] = Tournament.objects.filter(
            is_approved=True, is_active=True
        ).count()
        context['upcoming_tournaments'] = Tournament.objects.filter(
            is_approved=True, is_active=True, event_date__gte=date.today()
        ).count()
        
        return context


class TournamentDetailView(DetailView):
    """大会詳細ビュー"""
    model = Tournament
    template_name = 'tournaments/tournament_detail.html'
    context_object_name = 'tournament'
    
    def get_queryset(self):
        return Tournament.objects.filter(
            is_approved=True,
            is_active=True
        ).select_related('organizer').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        
        # お気に入り状態の確認
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                tournament=tournament
            ).exists()
        else:
            context['is_favorited'] = False
        
        # 関連する大会（同じ都道府県の今後の大会）
        context['related_tournaments'] = Tournament.objects.filter(
            prefecture=tournament.prefecture,
            is_approved=True,
            is_active=True,
            event_date__gte=date.today()
        ).exclude(pk=tournament.pk)[:6]
        
        return context


class TournamentSearchView(ListView):
    """大会検索ビュー"""
    model = Tournament
    template_name = 'tournaments/tournament_search.html'
    context_object_name = 'tournaments'
    paginate_by = 20
    
    def get_queryset(self):
        form = TournamentSearchForm(self.request.GET)
        queryset = Tournament.objects.filter(
            is_approved=True,
            is_active=True
        ).select_related('organizer')
        
        if form.is_valid():
            # 詳細検索ロジック
            if form.cleaned_data.get('keyword'):
                keyword = form.cleaned_data['keyword']
                queryset = queryset.filter(
                    Q(name__icontains=keyword) |
                    Q(venue_name__icontains=keyword) |
                    Q(events__icontains=keyword) |
                    Q(description__icontains=keyword)
                )
            
            if form.cleaned_data.get('prefecture'):
                queryset = queryset.filter(prefecture=form.cleaned_data['prefecture'])
            
            if form.cleaned_data.get('level'):
                queryset = queryset.filter(level=form.cleaned_data['level'])
            
            if form.cleaned_data.get('date_from'):
                queryset = queryset.filter(event_date__gte=form.cleaned_data['date_from'])
            
            if form.cleaned_data.get('date_to'):
                queryset = queryset.filter(event_date__lte=form.cleaned_data['date_to'])
            
            if form.cleaned_data.get('fee_max'):
                queryset = queryset.filter(fee__lte=form.cleaned_data['fee_max'])
        
        return queryset.order_by('event_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TournamentSearchForm(self.request.GET)
        context['title'] = '大会検索'
        return context


class TournamentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """大会作成ビュー（認証済み主催者のみ）"""
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/tournament_form.html'
    
    def test_func(self):
        return self.request.user.can_create_tournament()
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, '大会情報が登録されました。')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '大会登録'
        context['submit_text'] = '登録'
        return context


class TournamentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """大会編集ビュー"""
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/tournament_form.html'
    
    def test_func(self):
        tournament = self.get_object()
        return tournament.can_edit(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, '大会情報が更新されました。')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '大会編集'
        context['submit_text'] = '更新'
        return context


class TournamentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """大会削除ビュー"""
    model = Tournament
    template_name = 'tournaments/tournament_confirm_delete.html'
    success_url = reverse_lazy('tournaments:organizer_tournaments')
    
    def test_func(self):
        tournament = self.get_object()
        return tournament.can_delete(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '大会情報が削除されました。')
        return super().delete(request, *args, **kwargs)


class OrganizerTournamentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """主催者の大会一覧ビュー"""
    model = Tournament
    template_name = 'tournaments/organizer_tournament_list.html'
    context_object_name = 'tournaments'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.is_organizer()
    
    def get_queryset(self):
        return Tournament.objects.filter(
            organizer=self.request.user
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '私の大会一覧'
        return context


class FavoriteListView(LoginRequiredMixin, ListView):
    """お気に入り大会一覧ビュー"""
    model = Favorite
    template_name = 'tournaments/favorite_list.html'
    context_object_name = 'favorites'
    paginate_by = 15
    
    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('tournament__organizer').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'お気に入り大会'
        return context


class TournamentCalendarView(ListView):
    """カレンダー表示ビュー"""
    model = Tournament
    template_name = 'tournaments/tournament_calendar.html'
    
    def get_queryset(self):
        # 今月と来月の大会を取得
        today = date.today()
        next_month = today + timedelta(days=31)
        
        return Tournament.objects.filter(
            is_approved=True,
            is_active=True,
            event_date__gte=today,
            event_date__lte=next_month
        ).order_by('event_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '大会カレンダー'
        
        # カレンダー用のデータ整形
        tournaments = self.get_queryset()
        calendar_data = {}
        for tournament in tournaments:
            date_str = tournament.event_date.strftime('%Y-%m-%d')
            if date_str not in calendar_data:
                calendar_data[date_str] = []
            calendar_data[date_str].append(tournament)
        
        context['calendar_data'] = json.dumps(calendar_data, default=str)
        return context


@login_required
def toggle_favorite(request, pk):
    """お気に入りの追加/削除"""
    tournament = get_object_or_404(Tournament, pk=pk, is_approved=True, is_active=True)
    
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        tournament=tournament
    )
    
    if not created:
        favorite.delete()
        is_favorited = False
        message = 'お気に入りから削除しました。'
    else:
        is_favorited = True
        message = 'お気に入りに追加しました。'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_favorited': is_favorited,
            'message': message
        })
    
    messages.success(request, message)
    return redirect('tournaments:tournament_detail', pk=pk)


class TournamentApiView(ListView):
    """API用ビュー（JSON形式でデータを返す）"""
    model = Tournament
    
    def get(self, request, *args, **kwargs):
        tournaments = Tournament.objects.filter(
            is_approved=True,
            is_active=True
        ).values(
            'id', 'name', 'event_date', 'venue_name', 
            'prefecture', 'level', 'fee'
        )
        
        data = list(tournaments)
        return JsonResponse({
            'tournaments': data,
            'count': len(data)
        })