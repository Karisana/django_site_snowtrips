from django import template
from django.db.models import Count

from news.models import Category, News
register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    # news = Category.objects.annotate(Count('title'))
    cat1 = Category.objects.get(pk=1)
    cat1.news_set.count()
    # cat1.news_set.exists()
    # print(cat1.news_set.exists())
    # print(Category.objects.all())
    return Category.objects.all()

