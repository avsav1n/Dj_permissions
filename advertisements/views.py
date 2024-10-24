from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrAdmin
from advertisements.serializers import (AdvertisementSerializer,
                                        FavoritesSerializer)


class AdvertisementViewSet(ModelViewSet):
    '''ViewSet для объявлений
    '''
    queryset = Advertisement.objects.order_by('-id')
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.queryset.exclude(status='DRAFT')
        return self.queryset.exclude(Q(status='DRAFT') & ~Q(creator=self.request.user))

    def get_permissions(self):
        '''Получение прав для действий.
           Получение информации методом GET доступно всем
        '''
        if self.action == 'list':
            return []
        return super().get_permissions()
    
    @action(detail=True, methods=['POST'], url_path='favorites')
    def add_to_favorites(self, request, pk=None):
        '''Добавление объявления в избранное.
        '''
        advertisement = self.queryset.get(pk=pk)
        ser = FavoritesSerializer(instance=advertisement, partial = True,
                                  data={}, context={'request': request})
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'], url_path='favorites')
    def get_favorites(self, request, pk=None):
        '''Получение информации об объявлениях в избранном.
        '''
        advertisements = self.queryset.filter(in_favorites=request.user)
        filtered_advertisements = self.filter_queryset(advertisements)
        ser = FavoritesSerializer(instance=filtered_advertisements, many=True)
        return Response(ser.data)
    
