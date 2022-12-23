from django import template
from django.db.models import Count, F

from news.models import Category, SkiCenters

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='world'):
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {"categories": categories, "arg1": arg1, "arg2": arg2}


@register.simple_tag(name='get_name_glc')
def get_name_glc():
    return SkiCenters.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_glc(arg1='Hello', arg2='world'):
    names_gls = SkiCenters.objects.annotate(Count('ski_name'))
    return {"gls": names_gls, "arg1": arg1, "arg2": arg2}

