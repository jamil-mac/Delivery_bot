from django.contrib import admin
from django.utils.safestring import mark_safe

from backend.models import CategoryModel, MealModel, UserModel, OrderModel, CommentModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(MealModel)
class MealModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'thumb', 'real_price', 'discount']
    search_fields = ['name', 'real_price', 'discount']
    list_filter = ['name', 'real_price', 'discount']
    readonly_fields = ['real_price']

    def thumb(self, obj):
        return mark_safe("<img src='{}'  width='100' />".format(obj.image.url))


# @admin.register(UserModel)
# class UserModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'tg_id', 'contact']
#     search_fields = ['name', 'tg_id', 'contact']
#     list_filter = ['name', 'tg_id', 'contact']


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
    list_filter = ['user']


class CommentInline(admin.TabularInline):
    model = CommentModel
    extra = 1


class UserModelAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]


admin.site.register(CommentModel)

admin.site.register(UserModel, UserModelAdmin)
