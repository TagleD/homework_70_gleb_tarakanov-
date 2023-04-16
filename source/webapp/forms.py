from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, MinLengthValidator
from django.forms import Textarea
from webapp.models import Task, Project


class CustomLengthValidator(BaseValidator):
    def __init__(self, limit_value=50):
        message = ('Максимальная длина заголовка %(limit_value)s. Вы ввели %(show_value)s символов.')
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return value > limit_value

    def clean(self, value):
        return len(value)


# Проверка на цифру в начале строки
def find_number_left(string):
    try:
        int(string[0])
    except ValueError:
        return
    raise ValidationError('Нельзя начинать с цифры!')


# Проверка регистра первого символа строки
def first_char_upper(string):
    res = (string[0]).isupper()
    if not res:
        raise ValidationError('Нельзя начинать с нижнего регистра!')


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        validators=(
            MinLengthValidator(
                limit_value=2,
                message='Минимальная длина заголовка - 2!'
            ),
            CustomLengthValidator(),
            find_number_left
        ),
        label='Заголовок задачи'
    )
    description = forms.CharField(
        max_length=3000,
        label='Описание задачи',
        widget=Textarea,
        validators=(first_char_upper,)
    )

    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'status', 'type')
        labels = {
            'title': 'Заголовок задачи',
            'description': 'Описание задачи',
            'project': 'Выберите проект',
            'status': 'Статус',
            'type': 'Тип'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise ValidationError('Заголовок должен быть длинее 2-ух символов')
        return title


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'started_at', 'ended_at')
        labels = {
            'name': 'Название проекта',
            'description': 'Описание проекта',
            'started_at': 'Дата начала',
            'ended_at': 'Дата конца'
        }


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'type')
        labels = {
            'title': 'Заголовок задачи',
            'description': 'Описание задачи',
            'status': 'Статус',
            'type': 'Тип'
        }


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')


class ProjectAddUserForm(forms.ModelForm):
    def __init__(self, project_id, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.project = Project.objects.get(pk=project_id)
        user_pk_list = []
        for user in self.project.user.all():
            user_pk_list.append(user.pk)
        self.fields['user'].queryset = User.objects.all().exclude(pk__in=user_pk_list)

    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label='Выберите пользователя из списка доступных'
    )

    class Meta:
        model = Project
        fields = []


class ProjectDeleteUserForm(forms.ModelForm):
    def __init__(self, project_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = Project.objects.get(pk=project_id)
        self.fields['user'].queryset = self.project.user.all()

    user = forms.ModelChoiceField(
        queryset=Project.objects.none(),
        label='Выберите пользователя из списка доступных'
    )

    class Meta:
        model = Project
        fields = []
