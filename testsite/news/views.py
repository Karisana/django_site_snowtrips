from django.db.models import Max, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import News, Category
from .forms import NewsForm, UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
        else:
            messages.error(request, 'Регистрация НЕ прошла успешно.')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form} )


def login(request):
    return render(request, 'news/login.html')


def index(request):
    news = News.objects.order_by('-created_at')
    news_sorted_views = News.objects.annotate(Count("views")).order_by("-views")[:6]
    pagination = Paginator(news, 6)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    context = {
        'news': news,
        'title': 'Список новостей',
        'news_sorted_views': news_sorted_views,
        'page_obj': page_obj,
    }

    return render(request, 'news/news_list.html', context)


class NewsByCategory(ListView):
    model = News
    # template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2
    allow_empty = False  # не разрешаем показ пустых списков

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'


class RecommendedNews(ListView):
    model = News
    template_name = 'news/recom_news.html'
    context_object_name = 'recommended_news'

    def get_queryset(self):
        return News.objects.filter(recommended=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рекомендуемые новости ГЛЦ'
        return context


class MoreViews(ListView):
    model = News
    template_name = 'news/test.html'
    context_object_name = 'max_views_news'

    def get_queryset(self):
        return News.objects.aggregate(Max('views')).filter


def more_views(request):
    news_sorted_views = News.objects.annotate(Count("views")).order_by("-views")
    return render(request, 'news_list.html', {'news_sorted_views': news_sorted_views})




# def issue(request, news_id):
#     next = get_object_or_404(News, pk=news_id)
#     title = News.objects.filter(issue=issue)
#     # prev_issue = News.objects.filter(title=title).filter(pk__lt=issue.number)[0:1]
#     next = News.objects.filter(title=title, number__gt=next.number).order_by('pk').first()
#     return render(request, 'news/add_news.html', {'next': next})

#
# class PostListView(ListView):
#     model = News
#     template_name = 'news_item'
#     paginate_by = 5
#     queryset = News.objects.order_by('-created_at')


# Форма связанная с моделью:
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


# from django.shortcuts import render


# def view_news(request, news_id):
#     # news_item = get_object_or_404(News, pk=news_id)
#     news = News.objects.all()
#
#     news_item = news.filter(pk=news_id)
#     paginator = Paginator(news, 1)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'news/view_news.html', {'page_obj': page_obj, 'news_item': news_item, 'news':news})

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {'news': news, 'category': category}
#     return render(request, 'news/category.html', context)

# Форма не связанная с моделью:
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST,  request.FILES)
#         if form.is_valid():
#             news = News.objects.create(**form.cleaned_data)
#             return redirect(news)
#
#     else:
#         form = NewsForm() # не связана с данными. Если будут ошибки валидации, не надо будет пользователю снова все
#         # вводить. Нужно будет только исправить ошибки и отправить повторно.
#     return render(request, 'news/add_news.html', {'form': form})
#
