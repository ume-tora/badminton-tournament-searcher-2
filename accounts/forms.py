from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, Row, Column

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """ユーザー登録フォーム"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        initial='general',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    prefecture = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # 主催者用フィールド
    organization_name = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    organization_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'user_type',
            'phone_number', 'prefecture', 'organization_name', 'organization_website'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-3'),
                Column('password2', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'user_type',
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('prefecture', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Div(
                'organization_name',
                'organization_website',
                css_id='organizer-fields',
                css_class='organizer-only'
            ),
            Submit('submit', '登録', css_class='btn btn-primary btn-lg w-100')
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        organization_name = cleaned_data.get('organization_name')
        
        # 主催者の場合は団体名を必須にする
        if user_type == 'organizer' and not organization_name:
            raise forms.ValidationError('主催者として登録する場合は団体名が必要です。')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.prefecture = self.cleaned_data.get('prefecture', '')
        user.organization_name = self.cleaned_data.get('organization_name', '')
        user.organization_website = self.cleaned_data.get('organization_website', '')
        
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """ユーザーログインフォーム"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'ログイン', css_class='btn btn-primary btn-lg w-100')
        )
        
        # フィールドのスタイリング
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserProfileForm(forms.ModelForm):
    """ユーザープロフィール編集フォーム"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'prefecture', 'organization_name', 'organization_website'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'email',
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('prefecture', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'organization_name',
            'organization_website',
            Submit('submit', '更新', css_class='btn btn-primary')
        )
        
        # フィールドのスタイリング
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})