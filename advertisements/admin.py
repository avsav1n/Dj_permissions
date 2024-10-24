from django.contrib import admin
from django.db import models

# Register your models here.
from advertisements.models import Advertisement, Favorites


class FavoritesInline(admin.TabularInline):
    model = Favorites
    extra = 0

@admin.action(description='Change status to OPEN')
def change_status_to_open(modeladmin, request, queryset):
    queryset.update(status='OPEN')

@admin.action(description='Change status to CLOSED')
def change_status_to_closed(modeladmin, request, queryset):
    queryset.update(status='CLOSED')


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'creator',
                  'status', 'created_at', 'favorites_column']
    list_display_links = ['title']
    inlines = [FavoritesInline]
    actions = [change_status_to_open, change_status_to_closed]
    list_filter = ['status']
    
    @admin.display(description='Количество в избранных')
    def favorites_column(self, obj):
        return obj.relations

    def get_queryset(self, request):
        return Advertisement.objects.annotate(relations=models.Count('favorites'))

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ['user', 'advertisement', 'advertisement__id', 'advertisement__status']
    list_filter = ['user']