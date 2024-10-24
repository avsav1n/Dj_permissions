from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    '''Проверка прав
       Удалять и изменять могут только собственники и админы
    '''
    message = 'У Вас нет прав на удаление и изменение чужого заказа'
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.is_staff

