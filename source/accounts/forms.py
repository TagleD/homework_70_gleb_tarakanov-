from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Логин'
    )
    password = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.PasswordInput
    )


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        strip=False,
        required=True,
        widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        strip=False,
        required=True,
        widget=forms.PasswordInput
    )
    email = forms.EmailField(
        required=True,
        error_messages={'invalid': 'Введите почту вида email@mail.com'},
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Введите ваш уникальный Nickname',
            'password': 'Придумайте пароль',
            'password_confirm': 'Повторите ввод пароля',
            'first_name': 'Введите ваше имя',
            'last_name': 'Введите вашу фамилию',
            'email': 'Введите вашу почту'
        }

    def clean(self):
        cleaned_data = super().clean()

        # Проверка на совпадение паролей
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')

        # # Проверка на наличие ввода имени или фамилии
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not (first_name or last_name):
            raise forms.ValidationError('Вам нужно ввести хотя бы имя или фамилию!')

    # Метод save() нужен для хэширования паролей
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
