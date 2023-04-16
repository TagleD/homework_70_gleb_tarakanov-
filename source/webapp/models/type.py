from django.db import models


class Type(models.Model):
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Тип задачи'
