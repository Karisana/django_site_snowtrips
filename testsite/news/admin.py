from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'category','recommended', 'created_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

    fields = ('title',  'category','recommended', 'content','photo','get_photo', 'views','is_published','created_at',)
    readonly_fields = ('get_photo', 'views','created_at',)

    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width = "100px">')
        else:
            return 'Фото не загружено'

    # get_photo. = 'Миниатюра фото'
    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title  = 'Админка новостей'
admin.site.site_header  = 'Админка новостей'