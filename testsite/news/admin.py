from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category, SkiCenters, GroupsTrips, Groups


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'recommended', 'created_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

    fields = (
        'title', 'category', 'recommended', 'content', 'photo', 'get_photo', 'views', 'is_published', 'created_at',)
    readonly_fields = ('get_photo', 'views', 'created_at',)

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


class SkiCentersAdmin(admin.ModelAdmin):
    list_display = ('id', 'ski_name', 'ski_info')
    list_display_links = ('id', 'ski_name')
    search_fields = ('ski_name', 'ski_info')


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip_title', 'trip_link')
    list_display_links = ('id', 'trip_title')
    search_fields = ('trip_title', 'trip_date')


class GroupsTripsAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'trip_price', 'trip_place', 'trip_name_group')
    search_fields = ('date_start',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SkiCenters, SkiCentersAdmin)
admin.site.register(Groups, GroupsAdmin)
admin.site.register(GroupsTrips, GroupsTripsAdmin)

admin.site.site_title = 'Админка новостей'
admin.site.site_header = 'Админка новостей'
