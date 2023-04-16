from django.db import models
from django.utils import timezone


# Create your models here.


class Task(models.Model):
    title = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Заголовок"
    )
    description = models.TextField(
        max_length=3000,
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    status = models.ForeignKey(
        'webapp.Status',
        related_name='statuses',
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    type = models.ManyToManyField(
        to='webapp.Type',
        related_name='types',
        blank=True
    )
    project = models.ForeignKey(
        'webapp.Project',
        related_name='projects',
        on_delete=models.PROTECT,
        verbose_name='Проект',
        default=1
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        null=False,
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время",
        null=True
    )

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.title} - {self.description}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задача'
