from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import News, Category
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', ' john5', 'paul6', 'george7']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html/', {"page_obj": page_objects})


class HomeNews(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    # template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    allow_empty = False  # разрешаем показ пустых списков

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    login_url = '/admin/'

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

# def index(request):
#     news = News.objects.order_by('-created_at')  # сортировка новостей в обратном порядке
#     categories = Category.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#
#     return render(request, 'news/index.html', context)

# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

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
