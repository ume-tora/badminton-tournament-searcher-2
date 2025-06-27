from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationView(CreateView):
    """ユーザー登録ビュー"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('tournaments:tournament_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        
        # 自動ログイン
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
            login(self.request, authenticated_user)
            messages.success(self.request, f'アカウントが作成されました。ようこそ、{user.get_display_name()}さん！')
            
            # 主催者の場合は認証待ちメッセージを表示
            if user.user_type == 'organizer':
                messages.info(
                    self.request, 
                    '主催者アカウントが作成されました。大会を作成するには運営者による認証が必要です。'
                )
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'アカウント登録'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    """ユーザープロフィール編集ビュー"""
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'プロフィールが更新されました。')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'プロフィール編集'
        return context


@login_required
def dashboard_view(request):
    """ユーザーダッシュボード"""
    user = request.user
    context = {
        'title': 'ダッシュボード',
        'user': user,
    }
    
    # ユーザータイプに応じてコンテキストを追加
    if user.is_organizer():
        # 主催者の場合は作成した大会数などを表示
        from tournaments.models import Tournament
        context['tournaments_created'] = Tournament.objects.filter(organizer=user).count()
        context['is_verified'] = user.is_verified_organizer
    else:
        # 一般ユーザーの場合はお気に入り大会数などを表示
        from tournaments.models import Favorite
        context['favorite_tournaments'] = Favorite.objects.filter(user=user).count()
    
    return render(request, 'accounts/dashboard.html', context)