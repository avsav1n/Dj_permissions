from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    '''Serializer для пользователя
    '''
    class Meta:
        model = User
        fields = ('id', 'username')


class AdvertisementSerializer(serializers.ModelSerializer):
    '''Serializer для объявления
    '''
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        '''Метод для создания новых объявлений
        '''
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data: dict):
        '''Метод для валидации. Вызывается при создании и обновлении
        '''
        # TODO: добавьте требуемую валидацию

        max_ads = 5
        if self.context['request'].method == 'POST':
            ads_quantity = Advertisement.objects\
                .filter(creator=self.context['request'].user, status='OPEN').count()
            if ads_quantity + (0 if data.get('status', 'OPEN') != 'OPEN' else 1) > max_ads:
                raise ValidationError(f'У пользователя не может быть открыто более {max_ads} объявлений')
        return data


class FavoritesSerializer(AdvertisementSerializer):
    '''Serializer для избранных объявлений
    '''
    def update(self, instance, validated_data):
        instance.in_favorites.add(self.context['request'].user)
        return instance
    
    def validate(self, data: dict):
        if self.context['request'].user == self.instance.creator:
            raise ValidationError('Пользователь не может добавлять в '
                                  'избранное собственные объявления')
        if self.instance.status == 'DRAFT':
            raise ValidationError('Нельзя добавлять в избранное объявления со статусом DRAFT')
        return data
    

