from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    description = models.TextField(
        max_length=3000,
        null=False,
        blank=False,
        verbose_name='Описание'
    )
    user = models.ManyToManyField(
        to=User,
        related_name='projects'
    )
    started_at = models.DateField(
        verbose_name='Время создания',
        null=False
    )
    ended_at = models.DateField(
        null=True,
        default=None,
        verbose_name='Время завершения'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проект'
        permissions = [
            ('add_user_project', 'Добавить пользователя в проект'),
            ('delete_user_project', 'Удалить пользователя из проекта')
        ]
