from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    '''Статусы объявления
    '''
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    '''Объявление
    '''
    title = models.TextField('Название')
    description = models.TextField('Описание', default='')
    status = models.TextField('Статус', choices=AdvertisementStatusChoices.choices, 
                              default=AdvertisementStatusChoices.OPEN)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                verbose_name='Создатель')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    in_favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Favorites',
                                          related_name='+')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Favorites(models.Model):
    '''Избранное
    '''
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, 
                                      related_name='favorites', verbose_name='Объявления')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='+', verbose_name='Пользователь')
    
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint('user', 'advertisement', 
                                    name='user-advertisement-unique-constraint')
        ]