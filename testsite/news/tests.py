import bs4
from django.test import TestCase
from bs4 import BeautifulSoup
import requests

def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    return root.text.split('\n')


url = 'https://vk.com/zalesom.trip?w=wall-49741741_3728'
text = get_text(url)

values = ['', ' ', ]

new_text = [value for value in text if value not in values]


max_string = max(new_text, key=len)
print(max_string)



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
