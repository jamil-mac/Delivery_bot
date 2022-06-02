from django.contrib import admin
from django.utils.safestring import mark_safe

from backend.models import CategoryModel, MealModel, UserModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(MealModel)
class MealModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'real_price']
    search_fields = ['name', 'real_price']
    list_filter = ['name', 'real_price']
    readonly_fields = ['real_price']


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'tg_id', 'contact']
    search_fields = ['name', 'tg_id', 'contact']
    list_filter = ['name', 'tg_id', 'contact']

