from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, Row, Column, HTML
from datetime import date, timedelta
from .models import Tournament


class TournamentForm(forms.ModelForm):
    """大会登録・編集フォーム"""
    
    class Meta:
        model = Tournament
        fields = [
            'name', 'description', 'event_date', 'event_time', 'deadline_date',
            'venue_name', 'venue_address', 'prefecture', 'events', 'level',
            'fee', 'max_participants', 'event_details_url',
            'contact_name', 'contact_email', 'contact_phone'
        ]
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'event_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'venue_address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'events': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h4>基本情報</h4>'),
            'name',
            'description',
            
            HTML('<h4>日時・場所</h4>'),
            Row(
                Column('event_date', css_class='form-group col-md-6 mb-3'),
                Column('event_time', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'deadline_date',
            'venue_name',
            'venue_address',
            'prefecture',
            
            HTML('<h4>大会詳細</h4>'),
            'events',
            Row(
                Column('level', css_class='form-group col-md-6 mb-3'),
                Column('fee', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('max_participants', css_class='form-group col-md-6 mb-3'),
                Column('event_details_url', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            
            HTML('<h4>連絡先</h4>'),
            'contact_name',
            Row(
                Column('contact_email', css_class='form-group col-md-6 mb-3'),
                Column('contact_phone', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            
            Submit('submit', '保存', css_class='btn btn-primary btn-lg')
        )
        
        # フィールドのスタイリング
        for field in self.fields:
            if field not in ['event_date', 'deadline_date', 'event_time']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_deadline_date(self):
        deadline_date = self.cleaned_data.get('deadline_date')
        if deadline_date and deadline_date <= date.today():
            raise ValidationError('申込締切日は明日以降の日付を選択してください。')
        return deadline_date
    
    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date <= date.today():
            raise ValidationError('開催日は明日以降の日付を選択してください。')
        return event_date
    
    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('event_date')
        deadline_date = cleaned_data.get('deadline_date')
        
        if event_date and deadline_date:
            if deadline_date >= event_date:
                raise ValidationError('申込締切日は開催日より前の日付を選択してください。')
        
        return cleaned_data


class TournamentSearchForm(forms.Form):
    """大会検索フォーム"""
    
    PREFECTURE_CHOICES = [
        ('', '都道府県を選択'),
        ('北海道', '北海道'),
        ('青森県', '青森県'), ('岩手県', '岩手県'), ('宮城県', '宮城県'), ('秋田県', '秋田県'),
        ('山形県', '山形県'), ('福島県', '福島県'),
        ('茨城県', '茨城県'), ('栃木県', '栃木県'), ('群馬県', '群馬県'), ('埼玉県', '埼玉県'),
        ('千葉県', '千葉県'), ('東京都', '東京都'), ('神奈川県', '神奈川県'),
        ('新潟県', '新潟県'), ('富山県', '富山県'), ('石川県', '石川県'), ('福井県', '福井県'),
        ('山梨県', '山梨県'), ('長野県', '長野県'), ('岐阜県', '岐阜県'), ('静岡県', '静岡県'),
        ('愛知県', '愛知県'),
        ('三重県', '三重県'), ('滋賀県', '滋賀県'), ('京都府', '京都府'), ('大阪府', '大阪府'),
        ('兵庫県', '兵庫県'), ('奈良県', '奈良県'), ('和歌山県', '和歌山県'),
        ('鳥取県', '鳥取県'), ('島根県', '島根県'), ('岡山県', '岡山県'), ('広島県', '広島県'),
        ('山口県', '山口県'),
        ('徳島県', '徳島県'), ('香川県', '香川県'), ('愛媛県', '愛媛県'), ('高知県', '高知県'),
        ('福岡県', '福岡県'), ('佐賀県', '佐賀県'), ('長崎県', '長崎県'), ('熊本県', '熊本県'),
        ('大分県', '大分県'), ('宮崎県', '宮崎県'), ('鹿児島県', '鹿児島県'), ('沖縄県', '沖縄県'),
    ]
    
    keyword = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '大会名、会場名、種目などで検索'
        })
    )
    
    prefecture = forms.ChoiceField(
        choices=PREFECTURE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    level = forms.ChoiceField(
        choices=[('', 'レベルを選択')] + Tournament.LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='開催日（開始）'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='開催日（終了）'
    )
    
    fee_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '最大参加費（円）'
        }),
        label='参加費上限'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            'keyword',
            Row(
                Column('prefecture', css_class='form-group col-md-6 mb-3'),
                Column('level', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('date_from', css_class='form-group col-md-6 mb-3'),
                Column('date_to', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'fee_max',
            Submit('submit', '検索', css_class='btn btn-primary btn-lg w-100')
        )


class QuickSearchForm(forms.Form):
    """簡単検索フォーム（トップページ用）"""
    
    q = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '大会名、会場名、地域名で検索...'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = '/search/'
        self.helper.layout = Layout(
            Div(
                'q',
                Submit('submit', '検索', css_class='btn btn-primary btn-lg'),
                css_class='input-group input-group-lg'
            )
        )