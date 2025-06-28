from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import random

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
        
        # ユーザーデータを作成
        self.stdout.write('ユーザーデータを作成中...')
        self.create_users()
        
        # 大会データを作成
        self.stdout.write('大会データを作成中...')
        self.create_tournaments()
        
        # お気に入りデータを作成
        self.stdout.write('お気に入りデータを作成中...')
        self.create_favorites()
        
        self.stdout.write(
            self.style.SUCCESS('サンプルデータのロードが完了しました！')
        )
        
        # ロードされたデータの概要を表示
        self.show_summary()
    
    def create_users(self):
        """ユーザーを作成"""
        users_data = [
            {
                'username': 'tokyo_organizer',
                'email': 'tokyo@example.com',
                'first_name': '太郎',
                'last_name': '東京',
                'user_type': 'organizer',
                'password': 'organizer123'
            },
            {
                'username': 'osaka_organizer', 
                'email': 'osaka@example.com',
                'first_name': '花子',
                'last_name': '大阪',
                'user_type': 'organizer',
                'password': 'organizer123'
            },
            {
                'username': 'player_yamada',
                'email': 'yamada@example.com', 
                'first_name': '一郎',
                'last_name': '山田',
                'user_type': 'general',
                'password': 'player123'
            },
            {
                'username': 'player_tanaka',
                'email': 'tanaka@example.com',
                'first_name': '花子', 
                'last_name': '田中',
                'user_type': 'general',
                'password': 'player123'
            },
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'first_name': '管理',
                'last_name': '者',
                'user_type': 'admin',
                'password': 'admin123',
                'is_staff': True,
                'is_superuser': True
            }
        ]
        
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'  ✓ {user.username} を作成しました')
            else:
                self.stdout.write(f'  - {user.username} は既に存在します')
    
    def create_tournaments(self):
        """大会データを作成"""
        from tournaments.models import Tournament
        
        # 主催者を取得
        organizers = User.objects.filter(user_type='organizer')
        if not organizers.exists():
            self.stdout.write(self.style.ERROR('主催者ユーザーが見つかりません'))
            return
        
        tournaments_data = [
            {
                'name': '東京都バドミントン選手権大会',
                'venue_name': '東京体育館',
                'venue_address': '東京都渋谷区千駄ヶ谷1-17-1',
                'prefecture': '東京都',
                'level': 'open',
                'fee': 3000,
                'event_date': datetime.now().date() + timedelta(days=30),
                'deadline_date': datetime.now().date() + timedelta(days=15),
                'capacity': 128,
                'description': '東京都最大のバドミントン大会です。オープンクラスでどなたでも参加できます。',
                'organizer': organizers[0]
            },
            {
                'name': '大阪オープンバドミントン大会',
                'venue_name': '大阪市中央体育館',
                'venue_address': '大阪府大阪市港区田中3-1-40',
                'prefecture': '大阪府',
                'level': 'intermediate',
                'fee': 2500,
                'event_date': datetime.now().date() + timedelta(days=45),
                'deadline_date': datetime.now().date() + timedelta(days=25),
                'capacity': 96,
                'description': '関西地区最大級の中級者向け大会です。立地も良く交通アクセスも抜群です。',
                'organizer': organizers[1] if len(organizers) > 1 else organizers[0]
            },
            {
                'name': '初心者歓迎！春のバドミントン交流大会',
                'venue_name': '渋谷区総合スポーツセンター',
                'venue_address': '東京都渋谷区西原2-51-9',
                'prefecture': '東京都',
                'level': 'beginner',
                'fee': 1500,
                'event_date': datetime.now().date() + timedelta(days=21),
                'deadline_date': datetime.now().date() + timedelta(days=7),
                'capacity': 64,
                'description': 'バドミントンを始めたばかりの方、初心者の方大歓迎！素敵な仲間と出会える交流大会です。',
                'organizer': organizers[0]
            },
            {
                'name': '全国学生バドミントン選手権',
                'venue_name': '日本体育大学世田谷キャンパス',
                'venue_address': '東京都世田谷区深沢2-1-1',
                'prefecture': '東京都',
                'level': 'advanced',
                'fee': 4000,
                'event_date': datetime.now().date() + timedelta(days=60),
                'deadline_date': datetime.now().date() + timedelta(days=40),
                'capacity': 256,
                'description': '全国の学生バドミントンプレイヤーが集結する最高水準の大会です。',
                'organizer': organizers[0]
            },
            {
                'name': 'シニアバドミントン大会',
                'venue_name': '横浜武道館',
                'venue_address': '神奈川県横浜市中区翼原町1-1',
                'prefecture': '神奈川県',
                'level': 'open',
                'fee': 2000,
                'event_date': datetime.now().date() + timedelta(days=14),
                'deadline_date': datetime.now().date() + timedelta(days=3),
                'capacity': 80,
                'description': '45歳以上のシニアプレイヤーのための大会です。年齢を重ねても楽しめるバドミントンを！',
                'organizer': organizers[1] if len(organizers) > 1 else organizers[0]
            },
            {
                'name': 'ナイターバドミントンカップ',
                'venue_name': '千葉ポートアリーナ',
                'venue_address': '千葉県千葉市中央区中央港2-1',
                'prefecture': '千葉県',
                'level': 'intermediate',
                'fee': 2800,
                'event_date': datetime.now().date() + timedelta(days=28),
                'deadline_date': datetime.now().date() + timedelta(days=14),
                'capacity': 120,
                'description': '平日の夜間に開催されるユニークな大会です。仕事帰りに参加できます！',
                'organizer': organizers[0]
            },
            {
                'name': 'レディースバドミントンチャンピオンシップ',
                'venue_name': '品川女子学院体育館',
                'venue_address': '東京都品川区北品川5-17-18',
                'prefecture': '東京都',
                'level': 'intermediate',
                'fee': 2200,
                'event_date': datetime.now().date() + timedelta(days=35),
                'deadline_date': datetime.now().date() + timedelta(days=20),
                'capacity': 88,
                'description': '女性限定のバドミントン大会です。女性同士で楽しくプレイしましょう！',
                'organizer': organizers[1] if len(organizers) > 1 else organizers[0]
            },
            {
                'name': '関東学生リーグ決勝大会',
                'venue_name': '武蔵野総合体育館',
                'venue_address': '東京都武蔵野市境南町2-1-1',
                'prefecture': '東京都',
                'level': 'advanced',
                'fee': 3500,
                'event_date': datetime.now().date() + timedelta(days=50),
                'deadline_date': datetime.now().date() + timedelta(days=30),
                'capacity': 160,
                'description': '関東地区の大学リーグの雌雄を決める重要な大会です。高いレベルの試合が期待できます。',
                'organizer': organizers[0]
            }
        ]
        
        for tournament_data in tournaments_data:
            tournament, created = Tournament.objects.get_or_create(
                name=tournament_data['name'],
                defaults=tournament_data
            )
            if created:
                self.stdout.write(f'  ✓ {tournament.name} を作成しました')
            else:
                self.stdout.write(f'  - {tournament.name} は既に存在します')
    
    def create_favorites(self):
        """お気に入りデータを作成"""
        from tournaments.models import Tournament, Favorite
        
        # 一般ユーザーと大会を取得
        players = User.objects.filter(user_type='general')
        tournaments = Tournament.objects.all()
        
        if not players.exists() or not tournaments.exists():
            self.stdout.write(self.style.WARNING('ユーザーまたは大会が存在しません'))
            return
        
        # 各プレイヤーにランダムにお気に入りを作成
        for player in players:
            # 各プレイヤーに2-5個のお気に入りを作成
            favorite_count = random.randint(2, 5)
            favorite_tournaments = random.sample(list(tournaments), min(favorite_count, len(tournaments)))
            
            for tournament in favorite_tournaments:
                favorite, created = Favorite.objects.get_or_create(
                    user=player,
                    tournament=tournament
                )
                if created:
                    self.stdout.write(f'  ✓ {player.username} が {tournament.name} をお気に入りに追加')
    
    def show_summary(self):
        """ロードされたデータの概要を表示"""
        from tournaments.models import Tournament, Favorite
        
        user_count = User.objects.count()
        tournament_count = Tournament.objects.count()
        favorite_count = Favorite.objects.count()
        upcoming_count = Tournament.objects.filter(
            event_date__gte=datetime.now().date()
        ).count()
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('ロード完了サマリー'))
        self.stdout.write('=' * 50)
        self.stdout.write(f'👥 ユーザー数: {user_count}')
        self.stdout.write(f'🏆 大会数: {tournament_count}')
        self.stdout.write(f'🗓️ 開催予定大会: {upcoming_count}')
        self.stdout.write(f'❤️  お気に入り数: {favorite_count}')
        self.stdout.write('=' * 50)
        
        self.stdout.write('\n📝 テストアカウント情報:')
        self.stdout.write('  👥 管理者: admin / admin123')
        self.stdout.write('  🏆 主催者1: tokyo_organizer / organizer123')
        self.stdout.write('  🏆 主催者2: osaka_organizer / organizer123')
        self.stdout.write('  🏸 一般ユーザー1: player_yamada / player123')
        self.stdout.write('  🏸 一般ユーザー2: player_tanaka / player123')
        
        self.stdout.write('\n🏆 サンプル大会情報:')
        recent_tournaments = Tournament.objects.filter(
            event_date__gte=datetime.now().date()
        ).order_by('event_date')[:3]
        
        for i, tournament in enumerate(recent_tournaments, 1):
            self.stdout.write(f'  {i}. {tournament.name} ({tournament.event_date})')
        
        self.stdout.write('\n🚀 次のステップ:')
        self.stdout.write('  1. python manage.py runserver')
        self.stdout.write('  2. http://127.0.0.1:8000/ にアクセス')
        self.stdout.write('  3. 上記のアカウントでログインしてテスト')
        self.stdout.write('')