from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.auth.hashers import make_password

User = get_user_model()


class Command(BaseCommand):
    """
    サンプルデータをロードするコマンド
    
    使用方法:
    python manage.py load_sample_data
    """
    
    help = 'サンプルデータ（ユーザー、大会、お気に入り）をロードします'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='既存のデータを削除してからロード'
        )
    
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(
                self.style.WARNING('既存のデータを削除しています...')
            )
            # 関連データを削除
            from tournaments.models import Favorite, Tournament
            Favorite.objects.all().delete()
            Tournament.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write('サンプルデータをロードしています...')
        
        # ユーザーデータをロード
        self.stdout.write('ユーザーデータをロード中...')
        call_command('loaddata', 'accounts/fixtures/initial_users.json')
        
        # パスワードを設定（fixtureではハッシュ化されたパスワードが使えないため）
        self.set_passwords()
        
        # 大会データをロード
        self.stdout.write('大会データをロード中...')
        call_command('loaddata', 'tournaments/fixtures/initial_tournaments.json')
        
        # お気に入りデータをロード
        self.stdout.write('お気に入りデータをロード中...')
        call_command('loaddata', 'tournaments/fixtures/initial_favorites.json')
        
        self.stdout.write(
            self.style.SUCCESS('サンプルデータのロードが完了しました！')
        )
        
        # ロードされたデータの概要を表示
        self.show_summary()
    
    def set_passwords(self):
        """ユーザーのパスワードを設定"""
        users_passwords = {
            'tokyo_organizer': 'organizer123',
            'osaka_organizer': 'organizer123',
            'player_yamada': 'player123',
            'player_tanaka': 'player123',
            'admin': 'admin123'
        }
        
        for username, password in users_passwords.items():
            try:
                user = User.objects.get(username=username)
                user.password = make_password(password)
                user.save()
                self.stdout.write(
                    f'  ✓ {username} のパスワードを設定しました'
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  ✗ ユーザー {username} が見つかりません')
                )
    
    def show_summary(self):
        """ロードされたデータの概要を表示"""
        from tournaments.models import Tournament, Favorite
        
        user_count = User.objects.count()
        tournament_count = Tournament.objects.count()
        favorite_count = Favorite.objects.count()
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('ロード完了サマリー'))
        self.stdout.write('=' * 50)
        self.stdout.write(f'👥 ユーザー数: {user_count}')
        self.stdout.write(f'🏆 大会数: {tournament_count}')
        self.stdout.write(f'❤️  お気に入り数: {favorite_count}')
        self.stdout.write('=' * 50)
        
        self.stdout.write('\n📝 テストアカウント情報:')
        self.stdout.write('  管理者: admin / admin123')
        self.stdout.write('  主催者1: tokyo_organizer / organizer123')
        self.stdout.write('  主催者2: osaka_organizer / organizer123')
        self.stdout.write('  一般ユーザー1: player_yamada / player123')
        self.stdout.write('  一般ユーザー2: player_tanaka / player123')
        
        self.stdout.write('\n🚀 次のステップ:')
        self.stdout.write('  1. python manage.py runserver')
        self.stdout.write('  2. http://127.0.0.1:8000/ にアクセス')
        self.stdout.write('  3. 上記のアカウントでログインしてテスト')
        self.stdout.write('')